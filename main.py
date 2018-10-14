import numpy as np
from enum import Enum
import random 
from tkinter import *
import tkinter.ttk as ttk


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def succ(self):
        v = self.value + 1
        if v > 3:
            return Direction(0)
        return Direction(v)

    def pred(self):
        v = self.value - 1
        if v < 0:
            return Direction(3)
        return Direction(v)
    
    @classmethod
    def to_list(cls):
        if not hasattr(cls, 'directions'):
            cls.directions = list(Direction)
        return cls.directions


class Transition:

    def __init__(self, pos, direction, probability):
        self.pos = pos
        self.direction = direction
        self.probability = probability


class Motion:

    def __init__(self, pheromone_map, ant, direction_distr, pheromone_importance=0.5, length_importance=0.5):
        self.ant = ant
        self.path = [Transition(pos=ant.pos, direction=ant.direction, probability=1)]
        self.direction_distr = direction_distr
        self.pheromone_importance = pheromone_importance
        self.length_importance = length_importance
        self.pheromone_map = pheromone_map

    def length_probability(self, cur_direction, new_direction):
        if cur_direction == new_direction:
            return self.direction_distr[0]
        if cur_direction.succ() == new_direction or cur_direction.pred() == new_direction:
            return self.direction_distr[1]
        return self.direction_distr[2]

    def transition_probability(self, new_direction):
        pheromones = self.pheromone_map.map[self.ant.pos]
        l_p = self.length_probability(self.ant.direction, new_direction)
        prob_numerator = (pheromones[new_direction.value] ** self.pheromone_importance) * (l_p ** self.length_importance)
        prob_denominator = 0
        for direction in Direction.to_list():
            l_p = self.length_probability(direction, new_direction)
            prob_denominator += (pheromones[direction.value] ** self.pheromone_importance) * (l_p ** self.length_importance)
        return prob_numerator / prob_denominator

    def suggest_direction(self):
        prob_accum = 0
        probabilities = np.array([self.transition_probability(direction) for direction in Direction.to_list()])
        prob_sum = np.sum(probabilities)
        r = random.uniform(0, prob_sum)
        for i, prob in enumerate(probabilities):
            prob_accum += prob
            if prob_accum > r:
                return Direction.to_list()[i], prob
    
    def next_position(self, direction):
        cur_pos = self.ant.pos
        if direction == Direction.UP:
            return cur_pos[0]-1, cur_pos[1]
        if direction == Direction.RIGHT:
            return cur_pos[0], cur_pos[1]+1
        if direction == Direction.DOWN:
            return cur_pos[0]+1, cur_pos[1]
        if direction == Direction.LEFT:
            return cur_pos[0], cur_pos[1]-1
    
    def move(self):
        next_direction, probability = self.suggest_direction()
        next_position = self.next_position(next_direction)
        self.ant.direction = next_direction
        self.ant.pos = next_position
        self.path.append(Transition(pos=next_position, direction=next_direction, probability=probability))
        return next_position

    def return_to_colony(self, best_len):
        self.pheromone_map.update_pheromone_path(self.path, best_len)
        self.path = []
        self.ant.pos = self.ant.colony_pos


class Ant:
    def __init__(self, colony_pos=(0, 0), direction=Direction.DOWN):
        self.colony_pos = colony_pos
        self.pos = colony_pos
        self.direction = direction
        self.motion = None


class Colony:

    def __init__(self, pheromone_map, pos=(0, 0), size=100):
        self.pos = pos
        self.pheromone_map = pheromone_map
        self.ants = []
        for i in range(size):
            ant = Ant(colony_pos=pos, direction=random.choice(Direction.to_list()))
            ant.motion = Motion(pheromone_map=pheromone_map, ant=ant,
                                direction_distr=[0.7, 0.2, 0.1],
                                pheromone_importance=0.9)
            self.ants.append(ant)
    
    def find_target(self, target_pos, max_iter, render_map, way_no):
        best_way = None
        n_iter = 0
        way_counter = 0
        while n_iter < max_iter:
            iter_ways = []
            self.pheromone_map.pheromone_evaporation()
            for ant in self.ants:
                new_pos = ant.motion.move()
                if new_pos == target_pos:
                    iter_ways.append(ant.motion.path)
                    if best_way is None:
                        best_way = ant.motion.path
                    ant.motion.return_to_colony(len(best_way))
                    # if way_no == way_counter:
                    #     render_map()
                    #     return best_way, n_iter
                    way_counter += 1
                    # print("ways: {0}, best way length: {1}, iter: {2}".format(way_counter, len(best_way), n_iter))
            n_iter += 1
            if not iter_ways:
                continue
            pretendent = min(iter_ways, key=len)
            if best_way is None or len(best_way) > len(pretendent):
                best_way = pretendent

        return best_way, n_iter


class PheromoneMap:

    def __init__(self, n_rows, n_cols, pheromone_min, evaporation_speed=0.01, update_coef=1, cell_connectivity=4):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.cell_connectivity = cell_connectivity
        self.pheromone_min = pheromone_min
        self.update_coef = update_coef
        self.evaporation_speed = evaporation_speed
        self.map = self.generate_pheromone_map()

    def set_pheromone_borders(self, pheromone_map):
        # pheromones[:,0] - first column
        pheromone_map[:, 0][:, Direction.LEFT.value] = 0
        # pheromones[:,N_ROWS-1] -fight column
        pheromone_map[:, self.n_cols - 1][:, Direction.RIGHT.value] = 0
        # first row
        pheromone_map[0][:, Direction.UP.value] = 0
        # last row
        pheromone_map[self.n_rows - 1][:, Direction.DOWN.value] = 0
        return pheromone_map

    def generate_pheromone_map(self):
        pheromones = np.full((self.n_rows, self.n_cols, self.cell_connectivity), self.pheromone_min, dtype=float)
        return self.set_pheromone_borders(pheromones)

    def pheromone_evaporation(self):
        self.map = np.where(self.map > self.pheromone_min, (1 - self.evaporation_speed) * self.map, self.pheromone_min)
        self.set_pheromone_borders(self.map)

    def update_pheromone_path(self, path, best_len):
        path_len = len(path)
        iter_to = path_len - 1
        for i in range(iter_to):
            next_point = path[i+1]
            self.map[path[i].pos][next_point.direction.value] += (best_len / path_len) * self.update_coef


class Window:

    CANVAS_OFFSET = 5
    CELL_SIZE = 15

    def __init__(self, colony):
        self.root = Tk()
        self.colony = colony

        self.canvas_frame = ttk.Frame(self.root)
        self.canvas = Canvas(self.canvas_frame, height=800, width=800)
        self.canvas.pack()
        self.grid = self.draw_grid()
        self.path = []
        self.target = None
        self.canvas_frame.pack(side=LEFT)

        self.control_frame = ttk.Frame(self.root)
        self.run_button = ttk.Button(self.control_frame, text="Start", command=self.visualize_colony)
        self.run_button.pack(side=TOP)
        self.control_frame.pack(side=RIGHT)
        #self.root.geometry("800x720")
        self.pheromone_map_text = []

    def visualize_colony(self):
        path, n_iter = self.colony.find_target(target_pos=(20, 20), max_iter=1000,
                                               render_map=self.draw_pheromone_map,
                                               way_no=20)
        self.draw_colony_pos((0, 0))
        self.draw_target((20, 20))
        if path is not None:
            self.draw_path(path)
            # self.draw_pheromone_map()

    def draw_colony_pos(self, colony_pos):
        p1_x = colony_pos[0] * Window.CELL_SIZE + Window.CANVAS_OFFSET
        p1_y = colony_pos[1] * Window.CELL_SIZE + Window.CANVAS_OFFSET
        p2_x = p1_x + Window.CELL_SIZE
        p2_y = p1_y + Window.CELL_SIZE
        self.target = self.canvas.create_rectangle(p1_x, p1_y, p2_x, p2_y, fill='blue')

    def draw_target(self, target_pos):
        p1_x = target_pos[0] * Window.CELL_SIZE + Window.CANVAS_OFFSET
        p1_y = target_pos[1] * Window.CELL_SIZE + Window.CANVAS_OFFSET
        p2_x = p1_x + Window.CELL_SIZE
        p2_y = p1_y + Window.CELL_SIZE
        self.target = self.canvas.create_oval(p1_x, p1_y, p2_x, p2_y, fill='red')

    def draw_pheromone_map(self):
        n_rows = self.colony.pheromone_map.n_rows
        n_cols = self.colony.pheromone_map.n_cols
        if self.pheromone_map_text:
            for tag in self.pheromone_map_text:
                self.canvas.delete(tag)
                self.pheromone_map_text = []
        for i in range(n_rows):
            x = i * 20 + 5
            for j in range(n_cols):
                y = j * 20 + 5
                average = np.average(self.colony.pheromone_map.map[i][j])
                self.pheromone_map_text.append(self.canvas.create_text(x, y,
                                            font=("Purisa", 6),
                                            anchor=W,
                                            text=str(round(average, 3)),
                                            angle=-45))

    def draw_path(self, path):
        iter_to = len(path) - 1

        for i in range(iter_to):
            p1 = path[i].pos
            p2 = path[i+1].pos
            half_cell = Window.CELL_SIZE / 2
            p1_x_center = p1[0] * Window.CELL_SIZE + Window.CANVAS_OFFSET + half_cell
            p1_y_center = p1[1] * Window.CELL_SIZE + Window.CANVAS_OFFSET + half_cell
            p2_x_center = p2[0] * Window.CELL_SIZE + Window.CANVAS_OFFSET + half_cell
            p2_y_center = p2[1] * Window.CELL_SIZE + Window.CANVAS_OFFSET + half_cell
            self.path.append(
                self.canvas.create_line(p1_x_center,
                                        p1_y_center,
                                        p2_x_center,
                                        p2_y_center,
                                        arrow=LAST))

    def draw_grid(self):
        n_rows = self.colony.pheromone_map.n_rows
        n_cols = self.colony.pheromone_map.n_cols
        grid = []
        for i in range(n_rows):
            x = i * Window.CELL_SIZE + Window.CANVAS_OFFSET
            for j in range(n_cols):
                y = j * Window.CELL_SIZE + Window.CANVAS_OFFSET
                grid.append(self.canvas.create_rectangle(x, y,
                                                         x + Window.CELL_SIZE,
                                                         y + Window.CELL_SIZE,
                                                         outline='gray'))
        return grid

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    pheromone_map = PheromoneMap(n_rows=40, n_cols=40,
                                 pheromone_min=0.03,
                                 evaporation_speed=0.002,
                                 update_coef=5)
    colony = Colony(size=100, pheromone_map=pheromone_map)
    window = Window(colony=colony)
    window.run()
