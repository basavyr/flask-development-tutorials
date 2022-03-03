import sqlite3 as db


def main():
    database_name = 'openstack_topology.db'
    database = db.connect(database_name)

    cursor = database.cursor()

    print(cursor)


if __name__ == '__main__':
    main()
