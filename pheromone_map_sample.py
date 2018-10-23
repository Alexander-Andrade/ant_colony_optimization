from pheromone_map import PheromoneMap
from colony import Colony
from window import Window


if __name__ == '__main__':
    pheromone_map = PheromoneMap(n_rows=40,
                                 n_cols=40)
    colony = Colony(pos=(0, 0), pheromone_map=pheromone_map)
    path, n_iter, satisfies_accuracy = colony.find_target((20, 20), proximity_to_standard=0.6)

    window = Window(greed_size=(40, 40))
    window.draw_pheromone_map(pheromone_map)
    window.run()
