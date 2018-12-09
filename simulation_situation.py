from colony import Colony
from pheromone_map import PheromoneMap
import random
from multiprocessing import Pool
import math


# задание муравью на нахождение пути до нагрузки
# и нахождении пути от нагрузки до конечной точки
class AgentTask:

    def __init__(self, agent_pos, load_pos, destination_pos, map_size, proximity_to_standard=None,
                 colony_size=200, iter_max=None):
        self.agent_pos = agent_pos
        self.load_pos = load_pos
        self.destination_pos = destination_pos
        self.map_size = map_size
        self.colony_size = colony_size
        self.proximity_to_standard = proximity_to_standard
        self.iter_max = iter_max
        self.path = []
        self.success = True

    def perform(self):
        whole_path = []
        pheromone_map = PheromoneMap(n_rows=self.map_size[0],
                                     n_cols=self.map_size[1])
        colony = Colony(pos=self.agent_pos,
                        pheromone_map=pheromone_map,
                        size=self.colony_size)
        path, n_iter, satisfies_accuracy = colony.find_target(self.load_pos,
                                                              proximity_to_standard=self.proximity_to_standard,
                                                              iter_max=self.iter_max)
        whole_path = path

        if path is None or not satisfies_accuracy:
            return None

        pheromone_map = PheromoneMap(n_rows=self.map_size[0],
                                     n_cols=self.map_size[1])
        colony = Colony(pos=self.load_pos,
                        pheromone_map=pheromone_map,
                        size=self.colony_size)
        path, n_iter, satisfies_accuracy = colony.find_target(self.destination_pos,
                                                              proximity_to_standard=self.proximity_to_standard,
                                                              iter_max=self.iter_max)

        if path is None or not satisfies_accuracy:
            return None

        whole_path += path

        return whole_path


# имитационная ситуация
# задаются позиции нагрузок
# позиции конечных точек
# и случайным образом назначаются задачи муравьям
class SimulationSituation:

    def __init__(self, loads, destinations, map_size, colony_size, proximity_to_standard=None, iter_max=None):
        self.loads = loads
        self.destinations = destinations
        self.map_size = map_size
        self.colony_size = colony_size
        self.proximity_to_standard = proximity_to_standard
        self.iter_max = iter_max
        self.situation = []
        self.pool = Pool(len(self.loads))
        self.success = True

    def generate(self):
        for load, destination in zip(self.loads, self.destinations):
            agent_x = math.floor(random.uniform(0, self.map_size[0]))
            agent_y = math.floor(random.uniform(0, self.map_size[1]))
            self.situation.append(AgentTask(agent_pos=(agent_x, agent_y),
                                            load_pos=load,
                                            destination_pos=destination,
                                            map_size=self.map_size,
                                            colony_size=self.colony_size,
                                            iter_max=self.iter_max,
                                            proximity_to_standard=self.proximity_to_standard))
        return self.situation

    def print_situation(self):
        for task in self.situation:
            print("robot: {0} load: {1} destination: {2}".format(task.agent_pos, task.load_pos, task.destination_pos))

    @staticmethod
    def perform_situation(task):
        return task.perform()

    def perform(self):
        pathes = self.pool.map(SimulationSituation.perform_situation, self.situation)

        # pathes = []
        # for task in self.situation:
        #     pathes.append(task.perform())

        for task, path in zip(self.situation, pathes):
            task.path = path
            if path is None:
                task.success = False
                self.success = False

        return self.situation

