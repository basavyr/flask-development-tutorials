from flask import Flask, render_template


import base64
from io import BytesIO
from matplotlib.figure import Figure

import tools as local_tools
import plotter
import data as local_data

app = Flask(__name__)


@app.route("/")
def indexhtml():
    return render_template('index.html', message='ok')


@app.route('/1', methods=['POST', 'GET'])
def plot_example1():
    return render_template('plot1.html',
                           plot1=plotter.plot_data(),
                           plot2=plotter.plot_data(),
                           plot3=plotter.plot_data())


@app.route('/2', methods=['POST', 'GET'])
def plot_example2():
    return render_template('plot2.html',
                           disk_pie_chart=plotter.disk_pie_chart(),
                           swap_pie_chart=plotter.swap_pie_chart(),
                           virtual_memory_pie_chart=plotter.virtual_memory_pie_char(),
                           cpu_chart=plotter.cpu_info_chart(),
                           node_name=plotter.local_data.get_node_name(),
                           sys_info=plotter.local_data.get_sys_info(),
                           )


@app.route('/3', methods=['POST', 'GET'])
def plot_example3():
    node_list = local_tools.get_node_list()
    node_types = local_tools.get_node_types(node_list)

    return render_template('plot3.html',
                           time_stamp=local_tools.get_current_time(),
                           map_info=local_tools.get_openstack_map(),
                           nodes=node_list,
                           node_types=node_types,
                           )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
