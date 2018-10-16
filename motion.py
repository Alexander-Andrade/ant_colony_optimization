from direction import Direction
from transition import Transition
import random
import numpy as np

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
        prob_numerator = (pheromones[new_direction.value] ** self.pheromone_importance) * (
                    l_p ** self.length_importance)
        prob_denominator = 0
        for direction in Direction.to_list():
            l_p = self.length_probability(direction, new_direction)
            prob_denominator += (pheromones[direction.value] ** self.pheromone_importance) * (
                        l_p ** self.length_importance)
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
            return cur_pos[0] - 1, cur_pos[1]
        if direction == Direction.RIGHT:
            return cur_pos[0], cur_pos[1] + 1
        if direction == Direction.DOWN:
            return cur_pos[0] + 1, cur_pos[1]
        if direction == Direction.LEFT:
            return cur_pos[0], cur_pos[1] - 1

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