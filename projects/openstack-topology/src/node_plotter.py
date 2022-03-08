from datetime import datetime
from turtle import color, left
from matplotlib.figure import Figure
import sqlite3 as db
from contextlib import closing
import base64
from io import BytesIO

import platform

HOST = platform.uname()[0]

GLOBAL_DB_FILE = 'src/openstack_topology.db'


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
    ax.hist(data, color='#79B473')
    # ax.hist(data,color=[['#79B473','#70A37F','#41658A','#414073','#4C3957']])
    time_stamp = f'{datetime.utcnow()}'[:-7]
    fig.suptitle(
        f'Openstack Nodes running on\n<<{HOST}>> @ {time_stamp}', fontsize=14)

    # ax.set_xticks(rotation=30, ha='right')
    # rotate the labels according to the link below
    fig.autofmt_xdate(rotation=30)
    ax.set_xticklabels(data,fontsize=8, fontweight='bold')
    # https://www.delftstack.com/howto/matplotlib/how-to-rotate-x-axis-tick-label-text-in-matplotlib/

    # fig.savefig('openstack_nodes.png', bbox_inches='tight', dpi=400)
    # fig.savefig('openstack_nodes.png', dpi=400)

    fig.subplots_adjust(bottom=0.25, left=0.2, right=0.95, top=0.90)
    # Save it to a temporary buffer
    buffer = BytesIO()
    # fig.savefig('swap-pie-chart.pdf', dpi=300, bbox_inches='tight')
    fig.savefig(buffer, format="png", aspect='equal', dpi=450)

    # Embed the result in the html output.
    data = base64.b64encode(buffer.getbuffer()).decode("ascii")
    return data


def main():
    LOCAL_DB_FILE = 'openstack_topology.db'
    openstack_list = get_db_content(LOCAL_DB_FILE)
    node_types = get_openstack_node_types(openstack_list)
    print(node_types)
    make_histogram(node_types)


if __name__ == '__main__':
    main()
