from multiprocessing import connection
import sqlite3 as db

from sqlite3 import Error

from contextlib import closing
from datetime import datetime
import random


def generate_update_timestamp():
    return f'{datetime.utcnow()}'


OPENSTACK_SERVICES = ['nova-scheduler',
                      'nova-compute',
                      'nova-consoleauth',
                      'nova-conductor',
                      'nova-controller']
OPENSTACK_ZONES = ['nova', 'internal']
OPENSTACK_STATES = ['up 🟩', 'down 🟥']
OPENSTACK_STATUS = ['enabled', 'disabled']


# generate services (binaries)
def generate_service():
    rng_service = random.choice(OPENSTACK_SERVICES)
    return rng_service


# generate zones
def generate_zone():
    rng_zone = random.choice(OPENSTACK_ZONES)
    return rng_zone


# generate states
def generate_state():
    rng_state = random.choice(OPENSTACK_STATES)
    return rng_state


# generate status
def generate_status():
    rng_status = random.choice(OPENSTACK_STATUS)
    return rng_status


# GENERATE HOSTS 1
def generate_cloudifin_host(label):
    return f'dual-{label}.cloudifin'


# GENERATE HOSTS 2
def generate_dual_host(label):
    return f'dual-{label}'


# GENERATE HOSTS 3
def generate_nipne_host(index):
    return f'dual{index}-c.cloudifin.nipne.ro'


# GENERATE HOSTS 4
def generate_bcsh_host(index):
    return f'bchs{index}'


# GENERATE HOSTS 5
def generate_controller_host(index):
    return f'ctrl-os-{index}'


# host generation stage
def generate_random_host(host_id):
    if isinstance(host_id, str):
        # print('Will generate a host with <<label>>')
        labeled_host = [generate_dual_host(host_id),
                        generate_cloudifin_host(host_id)]
        return random.choice(labeled_host)
    elif isinstance(host_id, int):
        # print('Will generate a host with <<index>>')
        indexed_host = [generate_bcsh_host(host_id),
                        generate_nipne_host(host_id),
                        generate_controller_host(host_id)
                        ]
        return random.choice(indexed_host)


GLOBAL_DB_FILE = './src/openstack_topology.db'


def db_connect_object(db_file):
    """
    - create a connection and initialize a cursor for the database
    - the database is given via the db_file argument
    """
    try:
        db_conn = db.connect(db_file)
        db_cursor = db_conn.cursor()
    except Error as err:
        print(
            f'There was an issue with establishing database connection -> {err}')
        return -1, -1
    else:
        print('All good with the db stuff')

        return db_conn, db_cursor


def generate_db_entry(index):
    host_id = ['a', 'c', 'd', 1, 2, 3, 4]

    db_entry = (index,
                generate_service(),
                generate_random_host(random.choice(host_id)),
                generate_zone(),
                generate_status(),
                generate_state(),
                generate_update_timestamp(),
                )
    return db_entry


def db_init_drop(db_file):
    """
    - create a table named HOSTS
    - if the table already exists, it will DELETE it before initializing the connection and cursor objects
    """
    db_object = db_connect_object(db_file)

    connection = db_object[0]
    cursor = db_object[1]
    with closing(connection):
        cursor.execute('''DROP TABLE IF EXISTS HOSTS''')
        cursor.execute('''CREATE TABLE HOSTS (id_cloud integer primary_key,
                                              service text,
                                              host text,
                                              zone text,
                                              status text, 
                                              state text, 
                                              updated text)''')
        connection.commit()


def db_init_no_drop(db_file):
    """
    - create the table named HOSTS
    - if the table already exists, it will add data to it
    """
    db_object = db_connect_object(db_file)

    connection = db_object[0]
    cursor = db_object[1]
    with closing(connection):
        cursor.execute('''CREATE TABLE IF NOT EXISTS HOSTS (id_cloud integer primary_key,
                                              service text,
                                              host text,
                                              zone text,
                                              status text, 
                                              state text, 
                                              updated text)''')
        connection.commit()


def show_data(data):
    for data_element in data:
        print(data_element)


def db_update(db_file, data):
    db_object = db_connect_object(db_file)

    show_data(data)

    connection = db_object[0]
    cursor = db_object[1]

    # data is given as a list of tuples
    # each element of the list will be added in the database
    with closing(connection):
        cursor.executemany('INSERT INTO HOSTS VALUES (?,?,?,?,?,?,?)', data)
        connection.commit()

    # for data_element in data:
    #     id_cloud = int(data_element[0])
    #     service = str(data_element[1])
    #     host = str(data_element[2])
    #     zone = str(data_element[3])
    #     status = str(data_element[4])
    #     state = str(data_element[5])
    #     updated = str(data_element[6])


def pull_db_data(db_file):
    db_object = db_connect_object(db_file)

    connection = db_object[0]
    with closing(connection):
        cursor = db_object[1]
        raw_db_data = cursor.execute('SELECT * FROM HOSTS').fetchall()

    return raw_db_data


def main():
    LOCAL_DB_FILE = 'openstack_topology.db'
    node_number = 30
    openstack_data = [generate_db_entry(index + 1)
                      for index in range(node_number)]
    db_init_drop(LOCAL_DB_FILE)
    db_update(LOCAL_DB_FILE, openstack_data)


if __name__ == '__main__':
    main()
