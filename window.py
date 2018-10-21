import numpy as np
from tkinter import *
import tkinter.ttk as ttk


class Window:

    CANVAS_OFFSET = 5
    CELL_SIZE = 15

    def __init__(self, greed_size):
        self.root = Tk()
        self.greed_size = greed_size
        self.canvas_frame = ttk.Frame(self.root)
        self.canvas = Canvas(self.canvas_frame, height=800, width=800)
        self.canvas.pack()
        self.canvas_frame.pack(side=LEFT)

        # self.control_frame = ttk.Frame(self.root)
        # self.run_button = ttk.Button(self.control_frame, text="Start", command=self.visualize_colony)
        # self.run_button.pack(side=TOP)
        # self.control_frame.pack(side=RIGHT)
        # self.pheromone_map_text = []

    def render_simulation_situation(self, simulation_situation):
        self.grid = self.draw_grid(self.greed_size)
        colors = ['olive drab', 'brown3', 'blue4', 'orange', 'maroon', 'tomato']
        for task, color in zip(simulation_situation, colors):
            self.draw_label(task.agent_pos, shape='rect', color='green')
            self.draw_label(task.load_pos, shape='rect', color='red')
            self.draw_label(task.destination_pos, shape='circ', color='blue')
            self.draw_path(path=task.path, color=color)

    def visualize_path_search(self, colony_pos, target_pos, path):
        self.grid = self.draw_grid(self.greed_size)
        self.draw_label(colony_pos, shape='rect', color='green')
        self.draw_label(target_pos, shape='rect', color='red')
        self.draw_path(path, color='black')

    def draw_label(self, pos, shape, color):
        p1_x = pos[0] * Window.CELL_SIZE + Window.CANVAS_OFFSET
        p1_y = pos[1] * Window.CELL_SIZE + Window.CANVAS_OFFSET
        p2_x = p1_x + Window.CELL_SIZE
        p2_y = p1_y + Window.CELL_SIZE
        if shape == 'rect':
            self.canvas.create_rectangle(p1_x, p1_y, p2_x, p2_y, fill=color)
        elif shape == 'circ':
            self.canvas.create_oval(p1_x, p1_y, p2_x, p2_y, fill=color)

    def draw_pheromone_map(self, pheromone_map):
        n_rows = pheromone_map.n_rows
        n_cols = pheromone_map.n_cols
        for i in range(n_rows):
            x = i * 20 + 5
            for j in range(n_cols):
                y = j * 20 + 5
                average = np.average(pheromone_map.map[i][j])
                self.canvas.create_text(x, y,
                                        font=("Purisa", 6),
                                        anchor=W,
                                        text=str(round(average, 3)),
                                        angle=-45)

    def draw_path(self, path, color):
        iter_to = len(path) - 1

        for i in range(iter_to):
            p1 = path[i].pos
            p2 = path[i+1].pos
            half_cell = Window.CELL_SIZE / 2
            p1_x_center = p1[0] * Window.CELL_SIZE + Window.CANVAS_OFFSET + half_cell
            p1_y_center = p1[1] * Window.CELL_SIZE + Window.CANVAS_OFFSET + half_cell
            p2_x_center = p2[0] * Window.CELL_SIZE + Window.CANVAS_OFFSET + half_cell
            p2_y_center = p2[1] * Window.CELL_SIZE + Window.CANVAS_OFFSET + half_cell

            self.canvas.create_line(p1_x_center,
                                    p1_y_center,
                                    p2_x_center,
                                    p2_y_center,
                                    arrow=LAST,
                                    fill=color)

    def draw_grid(self, greed_size):
        grid = []
        for i in range(greed_size[0]):
            x = i * Window.CELL_SIZE + Window.CANVAS_OFFSET
            for j in range(greed_size[1]):
                y = j * Window.CELL_SIZE + Window.CANVAS_OFFSET
                grid.append(self.canvas.create_rectangle(x, y,
                                                         x + Window.CELL_SIZE,
                                                         y + Window.CELL_SIZE,
                                                         outline='gray'))
        return grid

    def run(self):
        self.root.mainloop()
