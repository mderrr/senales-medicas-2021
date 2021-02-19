import numpy as np
import matplotlib.pyplot as plt 

SUBPLOT_OFFSET = 131
NUMBER_OF_SUBPLOTS = 3

DECIMAL_PLACES_SHOWN = 2

TITLE_FONT_SIZE = 20
TICK_FONT_SIZE = 18

PLOT_TITLE = "sum (sig1 * sig{}) = "

DATA = [
    [3, 4, 5, 4, 3, 0, -1,-5, -2, 2],
    [3.2, 2.8, 6, 3, 3.4, 0.5, -1.5, -5.2, -2.4, 1],
    [4, 5, 2, 3, 1, 2, 4, 3, 1, 3],
    [0, -1, -2, -5, -6, -2, 4, 4, 4, 2]
]

def remove_means(data):
    for i in range(len(data)):
        data[i] -= np.mean(data[i])

def make_plots():
    data_a = DATA[0]

    for plot_index in range(len(DATA) - 1):
        ax1 = plt.subplot(SUBPLOT_OFFSET + plot_index)
        data_to_compare = DATA[plot_index + 1]
        summatory = round(np.sum(data_a * data_to_compare), DECIMAL_PLACES_SHOWN)

        plt.plot(data_a)
        plt.plot(data_to_compare)
        plt.title(PLOT_TITLE.format(plot_index + 2) + str(summatory), fontsize=TITLE_FONT_SIZE)
        plt.grid()
        plt.xticks(fontsize=TICK_FONT_SIZE)
        plt.yticks(fontsize=TICK_FONT_SIZE)

remove_means(DATA)
make_plots()
plt.show()