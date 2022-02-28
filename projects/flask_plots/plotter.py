from cProfile import label
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


def swap_pie_chart():
    raw_dict_data = local_data.get_swap_info()

    del raw_dict_data['percent']

    data = [int(raw_dict_data[key]) for key in raw_dict_data]
    print(data)
    _labels = [k for k in raw_dict_data]

    fig = Figure()

    ax = fig.subplots()

    try:
        ax.pie(data, labels=_labels)
    except ValueError as err:
        print(f'oops -> {err}')

    fig.tight_layout()
    ax.legend()
    fig.savefig('swap-data.pdf', dpi=300, bbox_inches='tight')

def main():
    swap_pie_chart()


if __name__ == '__main__':
    main()
