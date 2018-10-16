import numpy as np
from tkinter import *
import tkinter.ttk as ttk


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
