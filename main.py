from simulation_situation import SimulationSituation
import time
import matplotlib
import matplotlib.pyplot as plt

N = 10


def test(title, colony_size=None, iter_max=None):
    positive_results = []
    n_points_positive = []
    negative_results = []
    n_points_negative = []

    for i in range(N):
        situation = SimulationSituation(loads=[(14, 33), (5, 35), (18, 23)],
                                        destinations=[(25, 25), (30, 30), (5, 18)],
                                        map_size=(40, 40),
                                        colony_size=colony_size if colony_size is not None else (i+1)*20,
                                        iter_max=iter_max if iter_max is not None else (i+1)*200,
                                        proximity_to_standard=0.6)

        print("Situation {0}".format(i))
        situation.generate()
        situation.print_situation()

        start = time.time()
        situation.perform()

        end = time.time()
        time_diff = end - start

        print("time: {0}".format(time_diff))

        if situation.success is True:
            positive_results.append(time_diff)
            n_points_positive.append(i)
        else:
            negative_results.append(time_diff)
            n_points_negative.append(i)

    fig, ax = plt.subplots()
    ax.plot(n_points_negative, negative_results, 'rs', n_points_positive, positive_results, 'g^')

    ax.set(xlabel='N', ylabel='time (s)',
           title=title)
    ax.grid()
    plt.show()


if __name__ == '__main__':
    # time test
    # test(title='Time test', colony_size=100)
    # resource test
    test(title='Resource test', iter_max=1000)
