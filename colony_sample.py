from colony import Colony
from pheromone_map import PheromoneMap
from window import Window


if __name__ == '__main__':
    pheromone_map = PheromoneMap(n_rows=40,
                                 n_cols=40)
    colony = Colony(pos=(0, 0), pheromone_map=pheromone_map)
    path, n_iter = colony.find_target((20, 20))

    window = Window(greed_size=(40, 40))
    window.visualize_path_search(colony_pos=(0, 0), target_pos=(20, 20), path=path)
    window.run()
