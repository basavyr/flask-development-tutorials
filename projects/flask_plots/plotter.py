from matplotlib import pyplot as plt

import base64
from io import BytesIO
from matplotlib.figure import Figure


import random as rd


def generate_data():
    rand_number = lambda: rd.randrange(1, 15)
    data_size = 100
    y_data = [rand_number() for _ in range(data_size)]
    x_data = [idx + 1 for idx in range(data_size)]

    return [x_data, y_data]


def make_plot():
    xdata, ydata = generate_data()

    # generate the plot with the Figure command
    fig = Figure()
    ax = fig.subplots()
    ax.plot(xdata, ydata, '-ob', label='data')
    ax.legend(loc='best')
    ax.set_xlabel('x')
    ax.set_ylabel('rand')
    ax.set_ylim(0, 15)

    # Save it to a temporary buffer
    buffer = BytesIO()
    fig.savefig(buffer, format="png")

    # Embed the result in the html output.
    data = base64.b64encode(buffer.getbuffer()).decode("ascii")
    return data


def main():
    my_data = generate_data()
    make_plot(my_data)


if __name__ == '__main__':
    main()
