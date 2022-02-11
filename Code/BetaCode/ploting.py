from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()


def animate(data_time, data_fitness):
    x = x_vals.append(data_time)
    y = y_vals.append(data_fitness)

    plt.cla()

    plt.plot(x, y, label='Fitness Value')

    plt.legend(loc='upper left')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()
