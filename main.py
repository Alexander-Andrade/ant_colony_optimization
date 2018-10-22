from simulation_situation import SimulationSituation
from window import Window
import time
import matplotlib
import matplotlib.pyplot as plt
import random
from pheromone_map import PheromoneMap
from colony import Colony


N = 5

if __name__ == '__main__':

    time_test_results = []

    for i in range(N):
        situation = SimulationSituation(loads=[(14, 33), (5, 35), (18, 23)],
                                        destinations=[(25, 25), (30, 30), (5, 18)],
                                        map_size=(40, 40))

        situation.for_time_test()

        start = time.time()
        situation.perform()

        end = time.time()
        time_diff = end - start
        time_test_results.append(time_diff)
        print(time_diff)

    fig, ax = plt.subplots()
    ax.plot(time_test_results)

    ax.set(xlabel='N', ylabel='time (s)',
           title='Time test')
    ax.grid()
    plt.show()
