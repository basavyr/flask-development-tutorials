import subprocess
from subprocess import PIPE
import sqlite3 as db
from contextlib import closing


UTF8 = 'utf-8'


def get_active_containers():
    docker_cmd = ['docker', 'ps']
    process = subprocess.Popen(docker_cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    try:
        assert stderr == b'', 'Error while running the command'
    except AssertionError as issue:
        return stderr.decode(UTF8)
    else:
        return stdout.decode(UTF8)


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
    containers_active = get_active_containers()

    create_container_db()

    print(containers_active)

if __name__ == '__main__':
    main()
