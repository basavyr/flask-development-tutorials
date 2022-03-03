import sqlite3 as db

from sqlite3 import Error

from contextlib import closing


def generate_data():
    data = 1
    return data


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


def main():
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


if __name__ == '__main__':
    main()
