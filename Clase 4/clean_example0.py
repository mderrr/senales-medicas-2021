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

    return data
 
def make_plots(data):
    reference_data = data[0]

    for plot_index in range(len(data) - 1):
        data_to_compare = data[plot_index + 1]
        summatory = round(np.sum(reference_data * data_to_compare), DECIMAL_PLACES_SHOWN)

        plt.subplot(SUBPLOT_OFFSET + plot_index)
        plt.plot(reference_data)
        plt.plot(data_to_compare)
        plt.title(PLOT_TITLE.format(plot_index + 2) + str(summatory), fontsize=TITLE_FONT_SIZE)
        plt.grid()
        plt.xticks(fontsize=TICK_FONT_SIZE)
        plt.yticks(fontsize=TICK_FONT_SIZE)

if __name__ == "__main__":
    make_plots(remove_means(DATA))
    plt.show()