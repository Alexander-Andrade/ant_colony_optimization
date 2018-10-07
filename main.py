import numpy as np
from enum import Enum
import random 


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

    def __init__(self, pheromone_map, ant, probability_distr, pheromone_importance=0.5, length_importance=0.5):
        self.ant = ant
        self.path = []
        self.probability_distr = probability_distr
        self.pheromone_importance = pheromone_importance
        self.length_importance = length_importance
        self.pheromone_map = pheromone_map

    def length_probability(self, cur_direction, new_direction):
        if cur_direction == new_direction:
            return self.probability_distr[0]
        if cur_direction.succ() == new_direction or cur_direction.pred() == new_direction:
            return self.probability_distr[1]
        return self.probability_distr[2]

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
        direction, probability = self.suggest_direction()
        self.path.append(Transition(pos=self.ant.pos, direction=direction, probability=probability))
        next_position = self.next_position(direction)
        self.ant.direction = direction
        self.ant.pos = next_position
        return next_position

    def return_to_colony(self):
        self.pheromone_map.update_pheramone_path()
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
            ant = Ant(pos=pos, direction=random.choice(Direction.to_list()))
            ant.motion = Motion(pheromone_map=pheromone_map, ant=ant)
            self.ants.append(ant)
    
    def find_target(self, target_pos, max_iter):
        best_way = None
        n_iter = 0
        
        while n_iter < max_iter:
            iter_ways = []
            self.pheromone_map.pheromone_evaporation()
            for ant in self.ants:
                new_pos = ant.motion.move()
                if new_pos == target_pos:
                    iter_ways.append(ant.motion.path)
                    ant.motion.return_to_colony()
            pretendent = min(iter_ways, key=len)
            if best_way is None or len(best_way) > len(pretendent):
                best_way = pretendent
            n_iter += 1
        
        return best_way, n_iter


class PheromoneMap:

    def __init__(self, n_rows, n_cols, pheromone_min, evaporation_speed=0.01, cell_connectivity=4):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.cell_connectivity = cell_connectivity
        self.pheromone_min = pheromone_min
        self.evaporation_speed = evaporation_speed
        self.map = self.generate_pheromone_map()

    def generate_pheromone_map(self):
        pheromones = np.full((self.n_rows, self.n_cols, self.cell_connectivity), self.pheromone_min, dtype=float)
        # pheromones[:,0] - first column
        pheromones[:, 0][:, Direction.LEFT.value] = 0
        # pheromones[:,N_ROWS-1] -fight column
        pheromones[:, self.n_cols-1][:, Direction.RIGHT.value] = 0
        # first row
        pheromones[0][:, Direction.UP.value] = 0
        # last row
        pheromones[self.n_rows-1][:, Direction.DOWN.value] = 0
        return pheromones

    def pheromone_evaporation(self):
        self.map = np.where(self.map > self.pheromone_min, (1 - self.evaporation_speed) * self.map, self.pheromone_min)

    def update_pheromone_path(self, path):
        for transition in path:
            self.map[transition.pos][transition.direction.value] += 1 / transition.probability


if __name__ == '__main__':
    pheromone_map = PheromoneMap(n_rows=40, n_cols=40, pheromone_min=0.1, evaporation_speed=0.01)
    colony = Colony(size=1, pheromone_map=pheromone_map)
    ways, n_iter = colony.find_target(target_pos=(20, 20), max_iter=3000)
    print(len(ways[0]))
    print(n_iter)