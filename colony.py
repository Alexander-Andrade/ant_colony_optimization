from ant import Ant
from motion import Motion
from direction import Direction
import random


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

    def find_target(self, target_pos, max_iter=500000):
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
                    way_counter += 1
            n_iter += 1
            if not iter_ways:
                continue
            pretendent = min(iter_ways, key=len)
            if best_way is None or len(best_way) > len(pretendent):
                best_way = pretendent

        return best_way, n_iter