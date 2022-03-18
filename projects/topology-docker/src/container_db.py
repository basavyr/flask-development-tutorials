import sqlite3 as db
from contextlib import closing


def create_container_db():
    DB_NAME = 'containers.docker.db'
    db_conn = db.connect(DB_NAME)
    with closing(db_conn):
        cursor = db_conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS CONTAINERS')
        cursor.execute('''CREATE TABLE IF NOT EXISTS CONTAINERS
                                (id integer primary_key,
                                container_id text,
                                container_name, text
                                container_status text)''')

        db_conn.commit()


def main():
    create_container_db()


if __name__ == '__main__':
    main()
