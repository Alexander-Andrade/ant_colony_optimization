from colony import Colony
from pheromone_map import PheromoneMap
import random
from multiprocessing import Pool
import math


class AgentTask:

    def __init__(self, agent_pos, load_pos, destination_pos, map_size):
        self.agent_pos = agent_pos
        self.load_pos = load_pos
        self.destination_pos = destination_pos
        self.map_size = map_size
        self.path = []

    def perform(self):
        whole_path = []
        pheromone_map = PheromoneMap(n_rows=self.map_size[0],
                                     n_cols=self.map_size[1])
        colony = Colony(pos=self.agent_pos, pheromone_map=pheromone_map)
        path, n_iter = colony.find_target(self.load_pos)
        whole_path = path

        pheromone_map = PheromoneMap(n_rows=self.map_size[0],
                                     n_cols=self.map_size[1])
        colony = Colony(pos=self.load_pos, pheromone_map=pheromone_map)
        path, n_iter = colony.find_target(self.destination_pos)
        whole_path += path
        return whole_path


class SimulationSituation:

    def __init__(self, loads, destinations, map_size, n_agents=None):
        self.loads = loads
        self.destinations = destinations
        self.map_size = map_size
        self.n_agents = n_agents
        self.situation = []
        self.pool = Pool(len(self.loads))

    def for_time_test(self):
        for load, destination in zip(self.loads, self.destinations):
            agent_x = math.floor(random.uniform(0, self.map_size[0]))
            agent_y = math.floor(random.uniform(0, self.map_size[1]))
            self.situation.append(AgentTask(agent_pos=(agent_x, agent_y),
                                            load_pos=load,
                                            destination_pos=destination,
                                            map_size=self.map_size))
        return self.situation

    def for_resources_test(self):
        pass

    @staticmethod
    def perform_situation(task):
        return task.perform()

    def perform(self):
        pathes = self.pool.map(SimulationSituation.perform_situation, self.situation)

        for task, path in zip(self.situation, pathes):
            task.path = path

        return self.situation

