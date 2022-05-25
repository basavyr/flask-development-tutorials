from encodings import utf_8

import psutil
import platform
import subprocess

from subprocess import TimeoutExpired
from subprocess import PIPE
import base64
from io import BytesIO
from datetime import datetime

from matplotlib.figure import Figure
import matplotlib
matplotlib.rcParams['font.size'] = 15


################# move local data from separate module into here for app execution #######################
##########################################################################################################
##########################################################################################################
##########################################################################################################
GBYTES = 1024 * 1024 * 1024  # transform memory in gbytes


def get_timestamp():
    return f'{datetime.utcnow()}'


def get_swap_info():
    swap_info = psutil.swap_memory()

    memory = {
        "total": round(swap_info.total / GBYTES, 2),
        "available": round(swap_info.free / GBYTES, 2),
        "used": round(swap_info.used / GBYTES, 2),
        "percent": swap_info.percent,
    }

    return memory


def get_virtual_memory_info():
    mem_info = psutil.virtual_memory()

    memory = {
        "total": round(mem_info.total / GBYTES, 2),
        "available": round(mem_info.available / GBYTES, 2),
        "used": round(mem_info.used / GBYTES, 2),
        "percent": mem_info.percent,
    }

    return memory


def get_disk_info():
    disk_info = psutil.disk_usage('/')

    disk = {
        "total": round(disk_info.total / GBYTES, 2),
        "available": round(disk_info.free / GBYTES, 2),
        "used": round(disk_info.used / GBYTES, 2),
        "percent": disk_info.percent,
    }

    return disk


def get_cpu_info():
    n_cpus = psutil.cpu_count()
    load_average = [round(load * 100 / n_cpus, 2)
                    for load in psutil.getloadavg()]

    return load_average, n_cpus


def get_platform_arch():
    arch = platform.architecture()[0]
    processor = platform.processor()

    return f'{processor}-{arch}'


def get_node_name():
    node_name = platform.node()

    return f'{node_name}'


def get_sys_info():

    sys_info = [x for x in platform.uname()]
    # sys_info[5] = ''
    # fix the case when the system does not return a processor value
    if (sys_info[5] == ''):
        labels = ['System', 'Node', 'Release',
                  'Version', 'Machine', 'MachineX2']
        sys_info[5] = platform.machine()
    else:
        labels = ['System', 'Node', 'Release',
                  'Version', 'Machine', 'Processor']

    data_dict = {f'{labels[idx]}': sys_info[idx]
                 for idx in range(len(sys_info))}
    # print(data_dict)
    return data_dict


################# the self-contained graphs module (unified in this app, but separated in the 'openstack-topology' app) #######################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
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
    raw_dict_data = get_swap_info()

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
              bbox_to_anchor=(0.20, 0.95),
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
    raw_dict_data = get_virtual_memory_info()

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
              bbox_to_anchor=(0.2, 0.95),
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
    raw_dict_data = get_disk_info()

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
    cpu_usages, _ = get_cpu_info()

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

    # adjust the sizing and padding of the figure
    fig.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.90)

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
