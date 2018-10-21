from simulation_situation import SimulationSituation
from window import Window
import time
import random
from pheromone_map import PheromoneMap
from colony import Colony


if __name__ == '__main__':
    # random.seed(0)
    start = time.time()

    situation = SimulationSituation(loads=[(14, 33), (5, 35), (18, 23)],
                                    destinations=[(25, 25), (30, 30), (5, 18)],
                                    map_size=(40, 40))
    situation.for_time_test()
    situation.perform()

    # pheromone_map = PheromoneMap(n_rows=40,
    #                              n_cols=40)
    # colony = Colony(pos=(0, 0), pheromone_map=pheromone_map)
    # path, n_iter = colony.find_target((20, 20))

    end = time.time()
    print(end - start)

    # window = Window(greed_size=(40, 40))
    # window.draw_pheromone_map(pheromone_map)
    # window.run()

    # window = Window(greed_size=(40, 40))
    # window.visualize_path_search(colony_pos=(0, 0), target_pos=(20, 20), path=path)
    # window.run()

    window = Window(greed_size=(40, 40))
    window.render_simulation_situation(simulation_situation=situation.situation)
    window.run()
