from flask import Flask, render_template


import src.create_db as db
import src.node_plotter as plotter


app = Flask(__name__)


@app.route("/")
def show_index():
    return render_template('index.html')


@app.route("/topology")
def show_topology():
    node_list = db.pull_db_data(db_file=db.GLOBAL_DB_FILE)
    return render_template('topology.html',
                           nodes=node_list)


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
    return render_template('graphs.html')


def main():
    app.run(debug=True, port=5050)


if __name__ == '__main__':
    main()
