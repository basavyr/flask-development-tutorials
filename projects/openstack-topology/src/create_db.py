import sqlite3 as db

from sqlite3 import Error

from contextlib import closing
from datetime import datetime
import random

OPENSTACK_SERVICE_TYPE = ['nova-scheduler',
                          'nova-compute',
                          'nova-consoleauth',
                          'nova-conductor',
                          'nova-controller']


def generate_data():
    data = 1
    return data


def get_timestamp():
    return datetime.utcnow()


def generate_nipne_host(index):
    return f'dual{index}-c.cloudifin.nipne.ro'


def generate_cloudifin_host(label):
    return f'dual-{label}.cloudifin'


def generate_bcsh_host(index):
    return f'bchs{index}'


def generate_dual_host(label):
    return f'dual-{label}'


def generate_controller_host(index):
    return f'ctrl-os-{index}'


def generate_host(idx):
    hosts = ['ctrl-os',
             'dual-a',
             'dual-c',
             'dual-d',
             'bchs',
             'dual1-c.cloudifin.nipne.ro',
             'dual-d'
             ]


def db_connect(db_file):
    try:
        db_conn = db.connect(db_file)
        db_cursor = db_conn.cursor()
    except Error as err:
        print(f'There was an issue with establishing database connection')
        return -1, -1
    else:
        print('All good with the db stuff')

        return db_conn, db_cursor


def db_init():
    dbFile = 'openstack_topology.db'

    db_object = db_connect(db_file=dbFile)

    connection = db_object[0]
    cursor = db_object[1]
    with closing(connection) as db_conn:
        cursor.execute('''DROP TABLE IF EXISTS HOSTS''')
        cursor.execute('''CREATE TABLE HOSTS (id_cloud integer primary_key
                                              service text,
                                              host text,
                                              zone text,
                                              status text, 
                                              state text, 
                                              updated text)''')
        connection.commit()


def main():
    print(get_timestamp())


if __name__ == '__main__':
    main()
