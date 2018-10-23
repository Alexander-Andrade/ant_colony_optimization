from simulation_situation import SimulationSituation
import time
import matplotlib
import matplotlib.pyplot as plt

N = 5


def time_test():
    results = []
    n_points = []
    for i in range(N):
        situation = SimulationSituation(loads=[(14, 33), (5, 35), (18, 23)],
                                        destinations=[(25, 25), (30, 30), (5, 18)],
                                        map_size=(40, 40),
                                        proximity_to_standard=0.6)

        situation.for_time_test()

        start = time.time()
        situation.perform()

        end = time.time()
        time_diff = end - start
        results.append(time_diff)
        n_points.append(i)

        print(time_diff)

    fig, ax = plt.subplots()
    ax.plot(results)

    ax.set(xlabel='N', ylabel='time (s)',
           title='Time test')
    ax.grid()
    plt.show()


def resource_test():
    positive_results = []
    n_points_positive = []
    negative_results = []
    n_points_negative = []

    for i in range(N):
        situation = SimulationSituation(loads=[(14, 33), (5, 35), (18, 23)],
                                        destinations=[(25, 25), (30, 30), (5, 18)],
                                        map_size=(40, 40),
                                        colony_size=(i+1)*20,
                                        iter_max=1000,
                                        proximity_to_standard=0.6)

        situation.for_resources_test()

        start = time.time()
        situation.perform()

        end = time.time()
        time_diff = end - start
        print(time_diff)

        if situation.success is True:
            positive_results.append(time_diff)
            n_points_positive.append(i)
        else:
            negative_results.append(time_diff)
            n_points_negative.append(i)

    fig, ax = plt.subplots()
    # red squares, and green triangles
    ax.plot(n_points_negative, negative_results, 'rs', n_points_positive, positive_results, 'g^')

    ax.set(xlabel='N', ylabel='time (s)',
           title='resource test')
    ax.grid()
    plt.show()


if __name__ == '__main__':
    # time_test()
    resource_test()
