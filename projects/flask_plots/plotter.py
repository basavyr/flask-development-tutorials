from tabnanny import check
from threading import local

import base64
from io import BytesIO

from matplotlib import pyplot
from matplotlib.figure import Figure


import data as local_data


def plot_data():
    xdata, ydata = local_data.generate_data()

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


def pie_chart():
    test_data = local_data.get_swap_info()
    
    del test_data['percent']

    test_labels = [k for k in test_data]

    fig = Figure()

    ax = fig.subplots()

    ax.pie([12, 3, 4], labels=test_labels)
    ax.legend()
    fig.tight_layout()
    fig.savefig('pie-chart-data.pdf', dpi=300, bbox_inches='tight')

    return test_data


def main():
    pie_chart()


if __name__ == '__main__':
    main()
