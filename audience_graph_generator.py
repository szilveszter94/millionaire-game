import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random


def create_random_list(incorrect_answers, correct):
    rand_num = [random.choice(range(0, 100)) for r in range(4)]  # create random integers
    rand_num = [int(i / sum(rand_num) * 100) for i in rand_num]
    index = incorrect_answers.index(correct)
    index_2 = rand_num.index(max(rand_num))
    if index != index_2:
        rand_num[index], rand_num[index_2] = rand_num[index_2], rand_num[index]
    graph_generator(rand_num)


def graph_generator(y_axis):
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["yellow", "green"])
    x_axis = ["A", "B", "C", "D"]
    y_axis = y_axis
    plt.bar(x_axis, y_axis, color=cmap(y_axis))
    ax = plt.gca()
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.grid(alpha=0.1)
    ax.title.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.suptitle('Audience result', fontsize=20, color="white")
    plt.ylim([0, 100])
    plt.savefig("res/img/bar_chart.png", transparent=True)
