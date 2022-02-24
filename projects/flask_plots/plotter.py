from matplotlib import pyplot as plt
import random as rd


def generate_data():
    rand_number = lambda: rd.randrange(1, 15)
    data_size = 100
    y_data = [rand_number() for _ in range(data_size)]
    x_data = [idx + 1 for idx in range(data_size)]

    return [x_data, y_data]


def plot_data(data):
    xdata, ydata = data

    plt.plot(xdata, ydata, '-ob', label='data')
    plt.legend(loc='best')
    plt.xlabel('x')
    plt.ylabel('rand')
    plt.ylim(0, 15)
    plt.show()


def main():
    my_data = generate_data()
    plot_data(my_data)


if __name__ == '__main__':
    main()
