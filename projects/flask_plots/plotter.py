from cProfile import label
from tabnanny import check
from threading import local

import base64
from io import BytesIO

from matplotlib import pyplot
from matplotlib.figure import Figure
import matplotlib

import numpy

import data as local_data


matplotlib.rcParams['font.size'] = 15


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
    fig.tight_layout()

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
        patches, texts, autotexts = ax.pie(data,
                                           autopct=lambda pct: shower(
                                               pct, data),
                                           explode=(0.01, 0.01),
                                           textprops={'fontsize': 17,
                                                      'fontweight': 'bold',
                                                      })
    except ValueError as err:
        patches, texts, autotexts = ax.pie([idx + 1 for idx in range(len(data))],
                                           autopct=lambda pct: shower(
                                               pct, data),
                                           explode=(0.01, 0.01),
                                           textprops={'fontsize': 17,
                                                      'fontweight': 'bold',
                                                      })

    for auto in autotexts:
        auto.set_color('white')

    ax.legend(title='Swap memory [GB]',
              labels=data_labels,
              loc='center right',
              bbox_to_anchor=(1.2, 1),
              )
    fig.tight_layout()

    # Save it to a temporary buffer
    buffer = BytesIO()
    # fig.savefig('swap-pie-chart.pdf', dpi=300, bbox_inches='tight')
    fig.savefig(buffer, format="png")

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
        patches, texts, autotexts = ax.pie(data,
                                           autopct=lambda pct: shower(
                                               pct, data),
                                           explode=(0.01, 0.01),
                                           textprops={'fontsize': 17,
                                                      'fontweight': 'bold',
                                                      })
    except ValueError as err:
        patches, texts, autotexts = ax.pie([idx + 1 for idx in range(len(data))],
                                           autopct=lambda pct: shower(
                                               pct, data),
                                           explode=(0.01, 0.01),
                                           textprops={'fontsize': 17,
                                                      'fontweight': 'bold',
                                                      })

    for auto in autotexts:
        auto.set_color('white')

    ax.legend(title='Virtual memory [GB]',
              labels=data_labels,
              loc='best',
              bbox_to_anchor=(0.8, 0.7),
              )
    fig.tight_layout()

    # Save it to a temporary buffer
    buffer = BytesIO()
    # fig.savefig('virtual-memory-pie-chart.pdf', dpi=300, bbox_inches='tight')
    fig.savefig(buffer, format="png")

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
        patches, texts, autotexts = ax.pie(data,
                                           autopct=lambda pct: shower(
                                               pct, data),
                                           explode=(0.01, 0.01),
                                           textprops={'fontsize': 17,
                                                      'fontweight': 'bold',
                                                      })
    except ValueError as err:
        patches, texts, autotexts = ax.pie([idx + 1 for idx in range(len(data))],
                                           autopct=lambda pct: shower(
                                               pct, data),
                                           explode=(0.01, 0.01),
                                           textprops={'fontsize': 17,
                                                      'fontweight': 'bold',
                                                      })

    for auto in autotexts:
        auto.set_color('white')

    # set the legend
    ax.legend(title='Disk usage [GB]',
              labels=data_labels,
              loc='best',
              bbox_to_anchor=(0.8, 0.7),
              )

    fig.tight_layout()
    # Save it to a temporary buffer
    buffer = BytesIO()
    fig.savefig('disk-pie-chart.pdf', dpi=300, bbox_inches='tight')
    fig.savefig(buffer, format="png")

    # Embed the result in the html output.
    data = base64.b64encode(buffer.getbuffer()).decode("ascii")
    return data


def cpu_info_chart():
    cpu_usages, cpu_count = local_data.get_cpu_info()

    bar_labels = [f'last\n{idx} minute(s)' for idx in [1, 5, 15]]

    fig = Figure()
    ax = fig.subplots()

    try:
        bar_plot = ax.bar(bar_labels, cpu_usages)
    except ValueError as err:
        print(f'Issue while creating the bar plot -> {err}')
        bar_plot = ax.bar(bar_labels, [1, 1, 1])

    idx = 0
    for bar in bar_plot:
        current_height = bar.get_height() / 2
        text_label = cpu_usages[idx]
        x_cord = bar.get_x() + bar.get_width() / 2
        y_cord = bar.get_y() + current_height
        ax.text(x_cord, y_cord,
                text_label,
                ha='center',
                color='white',
                # size=14,
                fontweight='bold',)
        idx = idx + 1

    # fig.tight_layout()
    ax.set_title('Average CPU usage')
    ax.set_ylabel('%')
    # ax.set_ylim([0, 100])
    bar_plot[0].set_color('r')
    # bar_plot[1].set_color('')
    bar_plot[2].set_color('y')

    # Save it to a temporary buffer
    buffer = BytesIO()
    # fig.savefig('cpu-chart.pdf', dpi=300, bbox_inches='tight')
    fig.savefig(buffer, format="png")

    # Embed the result in the html output.
    data = base64.b64encode(buffer.getbuffer()).decode("ascii")
    return data


def main():
    disk_pie_chart()
    # swap_pie_chart()
    # virtual_memory_pie_char()
    # cpu_info_chart()


if __name__ == '__main__':
    main()
