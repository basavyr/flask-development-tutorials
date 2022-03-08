from flask import Flask, render_template


import logging

import src.create_db as db
import src.node_plotter as plotter
import src.graphs as graf

app = Flask(__name__)


@app.route("/")
def show_index():
    return render_template('index.html')


@app.route("/topology")
def show_topology():
    node_list = db.pull_db_data(db_file=db.GLOBAL_DB_FILE)
    return render_template('topology.html',
                           nodes=node_list,
                           time_stamp=db.generate_update_timestamp())


@app.route('/histogram')
def show_histogram():
    openstack_nodes = plotter.get_db_content(plotter.GLOBAL_DB_FILE)
    node_types = plotter.get_openstack_node_types(
        openstack_list=openstack_nodes)
    hist = plotter.make_histogram(node_types)
    return render_template('histogram.html',
                           histogram=hist)


@app.route('/graphs')
def show_graphs():
    graph_data = graf.give_graph_data()
    return render_template('graphs.html',
                           graph_data=graph_data,
                           disk_pie_chart=graf.disk_pie_chart(),
                           swap_pie_chart=graf.swap_pie_chart(),
                           virtual_memory_pie_chart=graf.virtual_memory_pie_char(),
                           cpu_chart=graf.cpu_info_chart(),
                           node_name=graf.local_data.get_node_name(),
                           sys_info=graf.local_data.get_sys_info(),
                           time_stamp=graf.local_data.get_timestamp(),
                           arch=graf.local_data.get_platform_arch(),
                           cpu_info=graf.local_data.get_cpu_info(),
                           )


def main():
    logging.basicConfig(filename='flask_app_errors.log', level=logging.DEBUG)
    app.run(debug=True, port=5050)


if __name__ == '__main__':
    main()
