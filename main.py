from simulation_situation import SimulationSituation
from window import Window
import time
import random


if __name__ == '__main__':
    random.seed(0)
    start = time.time()

    situation = SimulationSituation(loads=[(14, 33), (5, 35), (18, 23)],
                                    destinations=[(25, 25), (30, 30), (5, 18)],
                                    map_size=(40, 40))
    situation.for_time_test()
    situation.perform()

    end = time.time()
    print(end - start)

    window = Window(greed_size=(40, 40))
    window.render_simulation_situation(simulation_situation=situation.situation)
    window.run()
