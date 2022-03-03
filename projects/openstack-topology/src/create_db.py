import sqlite3 as db

from sqlite3 import Error

from contextlib import closing
from datetime import datetime
import random


def get_timestamp():
    return datetime.utcnow()


OPENSTACK_SERVICES = ['nova-scheduler',
                      'nova-compute',
                      'nova-consoleauth',
                      'nova-conductor',
                      'nova-controller']
OPENSTACK_ZONES = ['nova', 'internal']
OPENSTACK_STATES = ['up', 'down']
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


# generate status
def generate_status():
    rng_status = random.choice(OPENSTACK_STATUS)
    return rng_status


# GENERATE HOSTS 1
def generate_nipne_host(index):
    return f'dual{index}-c.cloudifin.nipne.ro'


# GENERATE HOSTS 2
def generate_cloudifin_host(label):
    return f'dual-{label}.cloudifin'


# GENERATE HOSTS 3
def generate_bcsh_host(index):
    return f'bchs{index}'


# GENERATE HOSTS 4
def generate_dual_host(label):
    return f'dual-{label}'


# GENERATE HOSTS 5
def generate_controller_host(index):
    return f'ctrl-os-{index}'


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
