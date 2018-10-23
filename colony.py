from motion import Motion
from direction import Direction
import random
import math


class Ant:
    def __init__(self, colony_pos=(0, 0), direction=Direction.DOWN):
        self.colony_pos = colony_pos
        self.pos = colony_pos
        self.direction = direction
        self.motion = None


class Colony:

    def __init__(self, pheromone_map, pos=(0, 0), size=200):
        self.pos = pos
        self.pheromone_map = pheromone_map
        self.ants = []
        for i in range(size):
            ant = Ant(colony_pos=pos, direction=random.choice(Direction.to_list()))
            ant.motion = Motion(pheromone_map=pheromone_map, ant=ant,
                                direction_distr=[0.7, 0.2, 0.1],
                                pheromone_importance=0.9)
            self.ants.append(ant)

    def standard_length(self, target_pos):
        return math.fabs(self.pos[0] - target_pos[0]) + math.fabs(self.pos[1] - target_pos[1])

    def find_target(self, target_pos, proximity_to_standard=0.6, iter_max=None):
        best_way = None
        n_iter = 0
        way_counter = 0
        standard_length = self.standard_length(target_pos)
        satisfies_accuracy = False

        while True:
            iter_ways = []
            self.pheromone_map.pheromone_evaporation()
            for ant in self.ants:
                new_pos = ant.motion.move()
                if new_pos == target_pos:
                    iter_ways.append(ant.motion.path)
                    if best_way is None:
                        best_way = ant.motion.path
                    ant.motion.return_to_colony(len(best_way))
                    way_counter += 1
            n_iter += 1
            if iter_max is not None and n_iter >= iter_max:
                break
            if not iter_ways:
                continue
            pretendent = min(iter_ways, key=len)
            if best_way is None or len(best_way) > len(pretendent):
                best_way = pretendent
            if proximity_to_standard is not None and standard_length / len(best_way) >= proximity_to_standard:
                satisfies_accuracy = True
                break

        return best_way, n_iter, satisfies_accuracy
