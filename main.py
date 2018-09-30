import numpy as np
from enum import Enum


N_ROWS = 40
N_COLS = 40
N_DIRS = 4


PHEROMONE_INIT = 0.1
START_POS = (0, 0)
END_POS = (15, 15)

N_ANTS = 5

MAX_ITER = 1000

# probability, that the ant will comtinue move forvard
STRAIGHT_PROB = 0.6
# propbability of ant turning aside
TURN_BACK_PROB = 0.3
TURN_ASIDE_PROB = 0.1

# pheromone importance
P_WEIGHT = 0.5
# transition weight (lenght) importance
L_WEIGHT = 0.5


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


class Ant:
    def __init__(self, pos=(0, 0), direction=Direction.DOWN):
        self.pos = pos
        self.direction = direction
        self.path = []
           

def length_probability(cur_direction, new_direction):
    if cur_direction == new_direction:
        return STRAIGHT_PROB
    if cur_direction.succ() == new_direction or cur_direction.pred() == new_direction:
        return TURN_ASIDE_PROB
    return TURN_BACK_PROB 

def transition_probability(pos, cur_direction, new_direction, pheromone_map):
    pheromones = pheromone_map[pos]
    l_p = length_probability(cur_direction, new_direction)
    prob_numerator = (pheromones[new_direction.value] ** P_WEIGHT) * (l_p ** L_WEIGHT)
    prob_denominator = 0
    for direction in list(Direction):
        l_p = length_probability(direction, new_direction)
        prob_denominator += (pheromones[direction.value] ** P_WEIGHT) * (l_p ** L_WEIGHT)
    return prob_numerator / prob_denominator

def init_pheromones():
    pheromones = np.full((N_ROWS, N_COLS, N_DIRS), PHEROMONE_INIT, dtype=float)
    # pheromones[:,0] - first column
    pheromones[:,0][:, Direction.LEFT.value] = 0
    # pheromones[:,N_ROWS-1] -fight column
    pheromones[:,N_COLS-1][:, Direction.RIGHT.value] = 0
    # first row
    pheromones[0][:, Direction.UP.value] = 0
    # last row
    pheromones[N_ROWS-1][:, Direction.UP.value] = 0
    return pheromones

def next_direction(ant, pheromone_map):
    dir_probs = {}
    dir_probs[Direction.UP] = transition_probability(ant.pos, ant.direction, Direction.UP, pheromone_map)
    dir_probs[Direction.RIGHT] = transition_probability(ant.pos, ant.direction, Direction.RIGHT, pheromone_map)
    dir_probs[Direction.DOWN] = transition_probability(ant.pos, ant.direction, Direction.DOWN, pheromone_map)
    dir_probs[Direction.LEFT] = transition_probability(ant.pos, ant.direction, Direction.LEFT, pheromone_map)
    return max(dir_probs, key=dir_probs.get)
    
    
    
# init pheromone_map
pheromone_map = init_pheromones()

colony = [Ant(pos=START_POS) for i in range(N_ANTS)]

