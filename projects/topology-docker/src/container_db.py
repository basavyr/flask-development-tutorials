from curses import raw
from shelve import DbfilenameShelf
import subprocess
from subprocess import PIPE
import sqlite3 as db
from contextlib import closing
from sys import stderr


UTF8 = 'utf-8'
DB_FILE = 'containers.docker.db'
EMPTY_LIST = []


def manipulate_raw_string(raw_string):
    """
    - obtain a list of containers from the initial raw string provided by subprocess
    """
    processed_raw_string = []
    for line in str(raw_string).strip().split('\n')[1:]:
        c_line = line.split()
        docker_container = [c_line[0], c_line[1], c_line[-1]]
        processed_raw_string.append(docker_container)
    return processed_raw_string


def get_active_containers():
    docker_cmd = ['docker', 'ps']
    process = subprocess.Popen(docker_cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    try:
        assert stderr == b'', 'Error while running the command'
    except AssertionError as issue:
        return []
    else:
        return manipulate_raw_string(stdout.decode(UTF8))


def get_docker_containers():
    """
    - Retreive all the docker containers that are installed on the current machine
    - The function returns a tuple list containing the container ID, the image name, the container name, and the status of the container
    - Returns an empty list if any errors occur during the command execution
    """
    docker_ps = ['docker', 'ps']
    docker_ps_a = ['docker', 'ps', '-a']

    # execute process for retreiving only the active/started containers from the system
    try:
        proc_docker_ps = subprocess.Popen(docker_ps, stdout=PIPE, stderr=PIPE)
    except Exception:
        return EMPTY_LIST
    else:
        pass

    # execute process for retreiving ALL the containers from the system
    try:
        proc_docker_ps_a = subprocess.Popen(
            docker_ps_a, stdout=PIPE, stderr=PIPE)
    except Exception:
        return EMPTY_LIST
    else:
        pass

    try:
        stdout_ps, stderr_ps = proc_docker_ps.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        proc_docker_ps.kill()
        return EMPTY_LIST
    else:
        pass

    try:
        assert stderr_ps == b'', 'Error while running the command'
    except AssertionError as issue:
        # if error occurs, stop the process
        # add a print function for debugging
        print(stderr_ps.decode('utf-8'))
        return EMPTY_LIST
    else:
        # first decode the command result from binary to standard utf8
        decoded_string = stdout_ps.decode(UTF8)

        # 1-> manipulate the raw string to a list
        # 2->store the active containers in a list
        active_containers = manipulate_raw_string(decoded_string)

        # execute the command for getting ALL the docker containers within the local system
        try:
            stdout_ps_a, stderr_ps_a = proc_docker_ps_a.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            proc_docker_ps_a.kill()
            return EMPTY_LIST
        else:
            pass

        if stderr_ps_a != b'':
            return EMPTY_LIST
        else:
            # continue with processing the containers list
            decoded_string = stdout_ps_a.decode(UTF8)
            all_containers = manipulate_raw_string(decoded_string)
            containers = []
            for idx in range(len(all_containers)):
                if all_containers[idx] in active_containers:
                    tuple_item = [all_containers[idx]
                                  [0], all_containers[idx][1], all_containers[idx][2], 1]
                else:
                    tuple_item = [all_containers[idx]
                                  [0], all_containers[idx][1], all_containers[idx][2], 0]
                containers.append(tuple_item)
            return containers


def create_container_db():
    DB_CONN = db.connect(DB_FILE)

    with closing(DB_CONN):
        cursor = DB_CONN.cursor()
        cursor.execute('DROP TABLE IF EXISTS CONTAINERS')
        cursor.execute('''CREATE TABLE IF NOT EXISTS CONTAINERS
                                (c_id integer primary_key,
                                ID text,
                                Image text,
                                Name text,
                                Status integer)''')

        DB_CONN.commit()


def add_containers_to_db(db_connection, containers):
    # create a list of tuples with all the information required for the db
    tuple_items = [(idx, containers[idx - 1][0], containers[idx - 1][1],
                    containers[idx - 1][2], containers[idx - 1][3]) for idx in range(len(containers))]

    cursor = db_connection.cursor()
    cursor.executemany(
        'INSERT INTO CONTAINERS VALUES (?,?,?,?,?)', tuple_items)
    db_connection.commit()


def get_container_db():
    # execute the docker command on the local system and get the complete list of docker containers
    # the function returns the containers as a list object
    docker_containers = get_docker_containers()
    if(docker_containers == -1):
        # print('Container list has an invalid format -> [] = -1')
        return []

    # add the docker containers in a database
    # 1 -> create the database file
    create_container_db()
    # 2-> make a connection to the (pre-existing) database
    db_connection = db.connect(DB_FILE)
    with closing(db_connection):
        # use the container list obtained above as a data source for the opened database
        # print('adding container list to the database...')
        add_containers_to_db(db_connection, docker_containers)
        # print('finished updating the database...')

    # retrieve the content from the database once it has been updated
    db_conn = db.connect(DB_FILE)
    raw_data = db_conn.execute('SELECT * FROM CONTAINERS').fetchall()
    if (len(raw_data) == 0):
        return []
    # the final container list to be returned as result
    container_list = []
    for data in raw_data:
        container = [d for d in data[1:]]
        print(container)
        container_list.append(container)

    return container_list


def main():
    C = get_container_db()
    try:
        assert C != [], 'Issue while retreiving the containers'
    except AssertionError as issue:
        print(issue)
    else:
        print(f'All good -> {C}')


if __name__ == '__main__':
    main()
