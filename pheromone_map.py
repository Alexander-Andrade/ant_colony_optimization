from direction import Direction
import numpy as np


class PheromoneMap:

    def __init__(self, n_rows, n_cols, pheromone_min=0.03, evaporation_speed=0.002, update_coef=5, cell_connectivity=4):
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
            self.map[path[i].pos][next_point.direction.value] += (best_len / path_len) * self.update_coef * next_point.probability