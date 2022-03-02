from cProfile import label
from tabnanny import check
from threading import local

import base64
from io import BytesIO

from matplotlib import pyplot
from matplotlib.figure import Figure

import numpy

import data as local_data


def shower(pct, data):
    """show a proper point based on the percentage"""
    absolute = round(pct / 100 * sum(data), 2)
    return f'{round(pct,2)} %\n{absolute} GB'


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

    percent = raw_dict_data['percent']

    # delete the percent element from the array
    del raw_dict_data['percent']
    # delete the total amount from the array
    del raw_dict_data['total']

    data = [float(raw_dict_data[key]) for key in raw_dict_data]
    data_labels = [k for k in raw_dict_data]

    fig = Figure()
    ax = fig.subplots()

    try:
        ax.pie(data,
               autopct=lambda pct: shower(pct, data),
               explode=(0.01, 0.01))
    except ValueError as err:
        print('Issue while creating the SWAP pie chart -> {err} ')
        ax.pie([idx + 1 for idx in range(len(data))],
               autopct=lambda pct: shower(pct, data),
               explode=(0.01, 0.01))

    ax.legend(title='Swap memory [GB]',
              loc='best',
              labels=data_labels)
    fig.tight_layout()

    # Save it to a temporary buffer
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    # fig.savefig('swap-pie-chart.pdf', dpi=300, bbox_inches='tight')

    # Embed the result in the html output.
    data = base64.b64encode(buffer.getbuffer()).decode("ascii")
    return data


def virtual_memory_pie_char():
    raw_dict_data = local_data.get_virtual_memory_info()

    percent = raw_dict_data['percent']

    # remove the percentage from the array
    del raw_dict_data['percent']
    # remove the total value from the data
    del raw_dict_data['total']

    data = [float(raw_dict_data[key]) for key in raw_dict_data]
    data_labels = [k for k in raw_dict_data]

    fig = Figure()
    ax = fig.subplots()

    try:
        ax.pie(data,
               autopct=lambda pct: shower(pct, data),
               explode=(0.01, 0.01))
    except ValueError as err:
        print('Issue while creating the VIRTUAL_MEMORY pie chart -> {err} ')
        ax.pie([idx + 1 for idx in range(len(data))],
               autopct=lambda pct: shower(pct, data),
               explode=(0.01, 0.01))

    ax.legend(title='Virtual memory [GB]',
              labels=data_labels,
              loc='best')
    fig.tight_layout()

    # Save it to a temporary buffer
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    # fig.savefig('virtual-memory-pie-chart.pdf', dpi=300, bbox_inches='tight')

    # Embed the result in the html output.
    data = base64.b64encode(buffer.getbuffer()).decode("ascii")
    return data


def disk_pie_chart():
    raw_dict_data = local_data.get_disk_info()

    percent = raw_dict_data['percent']

    # remove the percentage from the array
    del raw_dict_data['percent']
    # remove the total value from the array
    del raw_dict_data['total']

    data = [float(raw_dict_data[key]) for key in raw_dict_data]
    data_labels = [k for k in raw_dict_data]

    fig = Figure()
    ax = fig.subplots()
    try:
        ax.pie(data,
               autopct=lambda pct: shower(pct, data),
               explode=(0.01, 0.01))
    except ValueError as err:
        ax.pie([idx + 1 for idx in range(len(data))],
               autopct=lambda pct: shower(pct, data),
               explode=(0.01, 0.01))

    ax.legend(title='Disk usage [GB]',
              labels=data_labels,
              loc='best')
    fig.tight_layout()
    # Save it to a temporary buffer
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    # fig.savefig('disk-pie-chart.pdf', dpi=300, bbox_inches='tight')

    # Embed the result in the html output.
    data = base64.b64encode(buffer.getbuffer()).decode("ascii")
    return data


def main():
    disk_pie_chart()
    swap_pie_chart()
    virtual_memory_pie_char()


if __name__ == '__main__':
    main()
