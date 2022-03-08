from encodings import utf_8

import psutil

from datetime import datetime

import subprocess
from subprocess import TimeoutExpired
from subprocess import PIPE

import base64
from io import BytesIO
from matplotlib.figure import Figure
import matplotlib

import src.local_data as local_data

matplotlib.rcParams['font.size'] = 15
# matplotlib.rcParams.update({'hatch.color': 'k'})


def execute_linux_command(cmd):
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    try:
        stdout, stderr = proc.communicate()
    except TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()

    return stdout.decode('utf_8'), stderr.decode('utf_8')


def give_graph_data():
    user_name = ['whoami']
    node_info = ['uname', '-a']
    cmd1 = execute_linux_command(user_name)
    cmd2 = execute_linux_command(node_info)
    return cmd1, cmd2


def shower(pct, data):
    """show a proper point based on the percentage"""
    absolute = round(pct / 100 * sum(data), 2)
    return f'{round(pct,2)} %\n{absolute} GB'


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

    patches[0].set_color('#ADD8E6')
    patches[1].set_color('#C9A9A6')

    ax.legend(title='Swap memory',
              labels=data_labels,
              bbox_to_anchor=(0.35, 0.7),
              loc='upper right',
              )
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

    patches[0].set_color('#40B5AD')
    patches[1].set_color('#5D3FD3')

    ax.legend(title='Virtual memory',
              labels=data_labels,
              loc='upper right',
              bbox_to_anchor=(0.3, 0.7),
              )
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

    patches[0].set_color('#7393B3')
    patches[1].set_color('#E1C16E')

    # set the legend
    ax.legend(title='Disk usage',
              labels=data_labels,
              loc='best',
              bbox_to_anchor=(0.8, 0.7),
              )

    fig.tight_layout()
    # Save it to a temporary buffer
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    # fig.savefig('disk-pie-chart.pdf', dpi=300, bbox_inches='tight')

    # Embed the result in the html output.
    data = base64.b64encode(buffer.getbuffer()).decode("ascii")
    return data


def cpu_info_chart():
    cpu_usages, _ = local_data.get_cpu_info()

    bar_labels = [f'last\n{idx} minute(s)' for idx in [1, 5, 15]]

    fig = Figure()
    ax = fig.subplots()

    try:
        bar_plot = ax.bar(bar_labels, cpu_usages)
    except ValueError as err:
        print(f'Issue while creating the bar plot -> {err}')
        bar_plot = ax.bar(bar_labels, [1, 1, 1])

    set_colors = True

    if set_colors == True:
        # set the color for LOW usage mode
        if float(cpu_usages[0]) <= 50.0:
            bar_plot[0].set_color('#87CEEB')

        if float(cpu_usages[1]) <= 50.0:
            bar_plot[1].set_color('#87CEEB')

        if float(cpu_usages[2]) <= 50.0:
            bar_plot[2].set_color('#87CEEB')

        # set the color for MEDIUM usage mode
        if float(cpu_usages[0]) > 50.0 and float(cpu_usages[0]) <= 75.0:
            bar_plot[0].set_color('#4682B4')

        if float(cpu_usages[1]) > 50.0 and float(cpu_usages[1]) <= 75.0:
            bar_plot[1].set_color('#4682B4')

        if float(cpu_usages[2]) > 50.0 and float(cpu_usages[2]) <= 75.0:
            bar_plot[2].set_color('#4682B4')

        # set the color for high-usage mode
        if float(cpu_usages[0]) > 75.0:
            bar_plot[0].set_color('#A52A2A')

        # set the color for high-usage mode
        if float(cpu_usages[1]) > 75.0:
            bar_plot[1].set_color('#A52A2A')

        # set the color for high-usage mode
        if float(cpu_usages[2]) > 75.0:
            bar_plot[2].set_color('#A52A2A')

    hatches = ['\\', '.', '/']

    idx = 0
    for bar in bar_plot:
        current_height = bar.get_height() / 2
        text_label = f'{cpu_usages[idx]}'
        x_cord = bar.get_x() + bar.get_width() / 2
        y_cord = bar.get_y() + current_height
        ax.text(x_cord, y_cord,
                text_label,
                ha='center',
                color='white',
                size=25,
                fontweight='bold',)
        # bar.set(hatch=hatches[idx])
        # sources for setting the bar hatches
        # https://towardsdatascience.com/how-to-fill-plots-with-patterns-in-matplotlib-58ad41ea8cf8
        # https://stackoverflow.com/questions/56674645/changing-hatch-color-in-matplotlib
        bar.set_hatch(hatches[idx])
        bar.set_edgecolor('k')
        idx = idx + 1

    # fig.tight_layout()
    ax.set_title('Average CPU usage')
    ax.set_ylabel('%')
    # ax.set_ylim([0, 100])

    # Save it to a temporary buffer
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    # fig.savefig('cpu-chart.pdf', dpi=300, bbox_inches='tight')

    # Embed the result in the html output.
    data = base64.b64encode(buffer.getbuffer()).decode("ascii")
    return data


def main():
    cmd1 = ['ls', '-la']
    cmd2 = ['uname', '-a']
    cmd3 = ['whoami']
    uname = execute_linux_command(cmd2)
    print(uname)


if __name__ == '__main__':
    main()
