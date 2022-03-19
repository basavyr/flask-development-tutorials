from curses import raw
import subprocess
from subprocess import PIPE
import sqlite3 as db
from contextlib import closing


UTF8 = 'utf-8'


def manipulate_raw_string(raw_string):
    raw_string = [line.split() for line in str(raw_string).strip().split('\n')]
    return raw_string[1:]


def get_active_containers():
    docker_cmd = ['docker', 'ps']
    process = subprocess.Popen(docker_cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    try:
        assert stderr == b'', 'Error while running the command'
    except AssertionError as issue:
        # return stderr.decode(UTF8)
        return []
    else:
        return manipulate_raw_string(stdout.decode(UTF8))


def get_all_containers():
    docker_cmd = ['docker', 'ps', '-a']
    process = subprocess.Popen(docker_cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    try:
        assert stderr == b'', 'Error while running the command'
    except AssertionError as issue:
        return []
    else:
        return manipulate_raw_string(stdout.decode(UTF8))


def retrieve_container_status(active_containers, all_containers):
    container_status = []
    for container in all_containers:
        if container in active_containers:
            container_status.append(1)
        else:
            container_status.append(0)

    return container_status


def create_container_db():
    DB_FILE = 'containers.docker.db'

    DB_CONN = db.connect(DB_FILE)
    with closing(DB_CONN):
        cursor = DB_CONN.cursor()
        cursor.execute('DROP TABLE IF EXISTS CONTAINERS')
        cursor.execute('''CREATE TABLE IF NOT EXISTS CONTAINERS
                                (id integer primary_key,
                                container_id text,
                                container_name text,
                                container_status text)''')

        DB_CONN.commit()

    return db.connect(DB_FILE)


def add_containers_to_db(db_conn, containers, status):
    cursor = db_conn.cursor()
    idx = 1
    for container in containers:
        print(f'will add this container to the db: {container}')
        cursor.execute('INSERT INTO CONTAINERS VALUES (?,?,?,?)',
                       (idx, container[0], container[1], status))
        idx = idx + 1
    db_conn.commit()


def main():
    containers_active = get_active_containers()
    containers_all = get_all_containers()

    print(retrieve_container_status(containers_active, containers_all))

    # db_conn = create_container_db()
    # add_containers_to_db(db_conn, containers_active, 'up')
    # add_containers_to_db(db_conn, containers_all, 'down')


if __name__ == '__main__':
    main()
