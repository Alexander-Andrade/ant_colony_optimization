import random


class Task:

    def __init__(self, agent, load, destination):
        self.agent = agent
        self.load = load
        self.destination = destination

    def perform(self):
        pass


class SimulationSituation:

    def __init__(self, loads, destinations, map_size, n_agents=None):
        self.loads = loads
        self.destinations = destinations
        self.map_size = map_size
        self.n_agents = n_agents

        self.n_agents = n_agents

    def for_time_test(self):
        situation = []
        for load, destination in zip(self.loads, self.destinations):
            agent_x = random.uniform(0, self.map_size[0])
            agent_y = random.uniform(0, self.map_size[1])
            situation.append(Task(agent=(agent_x, agent_y), load=load, destination=destination))
        return situation

    def for_resources_test(self):
        pass