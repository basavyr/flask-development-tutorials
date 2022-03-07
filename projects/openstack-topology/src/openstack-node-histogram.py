from matplotlib.figure import Figure
import sqlite3 as db
from contextlib import closing
import base64
from io import BytesIO


def get_db_content(db_file):
    db_connection = db.connect(db_file)
    with closing(db_connection):
        cursor = db_connection.cursor()
        raw_data = cursor.execute('SELECT * FROM HOSTS').fetchall()

    return raw_data


def get_openstack_node_types(openstack_list):
    nodes = []
    for node in openstack_list:
        nodes.append(node[1])

    return nodes


def make_histogram(data):
    fig = Figure()
    ax = fig.subplots()
    ax.hist(data)
    fig.suptitle('Openstack Nodes', fontsize=14)
    # ax.set_xticks(rotation=30, ha='right')
    # rotate the labels according to the link below
    fig.autofmt_xdate(rotation=30)
    # https://www.delftstack.com/howto/matplotlib/how-to-rotate-x-axis-tick-label-text-in-matplotlib/

    fig.savefig('openstack_nodes.png', bbox_inches='tight', dpi=400)


def main():
    LOCAL_DB_FILE = 'openstack_topology.db'
    openstack_list = get_db_content(LOCAL_DB_FILE)
    node_types = get_openstack_node_types(openstack_list)
    print(node_types)
    make_histogram(node_types)


if __name__ == '__main__':
    main()
