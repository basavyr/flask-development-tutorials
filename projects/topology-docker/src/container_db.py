from curses import raw
import subprocess
from subprocess import PIPE
import sqlite3 as db
from contextlib import closing
from sys import stderr


UTF8 = 'utf-8'


def manipulate_raw_string(raw_string):
    raw_string = [line.split()[0:2]
                  for line in str(raw_string).strip().split('\n')]
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
    # retreive the list of active containers
    active_containers = get_active_containers()
    # command for getting all the docker containers
    docker_cmd = ['docker', 'ps', '-a']
    # execute command
    process = subprocess.Popen(docker_cmd, stdout=PIPE, stderr=PIPE)
    # get the result of the command
    stdout, stderr = process.communicate()

    try:
        assert stderr == b'', 'Error while running the command'
    except AssertionError as issue:
        return []
    else:
        all_containers = manipulate_raw_string(stdout.decode(UTF8))
        container_status = retrieve_container_status(
            active_containers, all_containers)
        # store each container and its status within a separate object
        res = []
        for idx in range(len(all_containers)):
            res.append([all_containers[idx][0], all_containers[idx]
                       [1], container_status[idx]])
        return res


def get_docker_containers():
    """
    - Retreive all the docker containers that are installed on the current machine
    - The function returns a tuple list containing the ID, the name, and the status of the container
    """
    docker_ps = ['docker', 'ps']
    docker_ps_a = ['docker', 'ps', '-a']

    # execute process for retreiving only the active/started containers from the system
    proc_docker_ps = subprocess.Popen(docker_ps, stdout=PIPE, stderr=PIPE)
    # execute process for retreiving ALL the containers from the system
    proc_docker_ps_a = subprocess.Popen(docker_ps_a, stdout=PIPE, stderr=PIPE)

    stdout_ps, stderr_ps = proc_docker_ps.communicate()
    try:
        assert stderr_ps == b'', 'Error while running the command'
    except AssertionError as issue:
        print('there are no active containers')
        print(stderr_ps.decode(UTF8))
    else:
        # first decode the command result from binary to standard utf8
        decoded_string = stdout_ps.decode(UTF8)
        # manipulate the raw string to a list
        # store the active containers in a list
        active_containers = manipulate_raw_string(decoded_string)
        # execute the command for getting all the docker containers within the local system
        stdout_ps_a, stderr_ps_a = proc_docker_ps_a.communicate()
        if stderr_ps_a != b'':
            print('Issue with the retrieval of docker containers')
            return []
        else:
            # continue with processing the containers list
            decoded_string = stdout_ps_a.decode(UTF8)
            all_containers = manipulate_raw_string(decoded_string)
            print(all_containers)


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


def add_containers_to_db(db_conn, containers, container_status):
    cursor = db_conn.cursor()
    idx = 1
    for container in containers:
        print(f'will add this container to the db: {container}')
        cursor.execute('INSERT INTO CONTAINERS VALUES (?,?,?,?)',
                       (idx, container[0], container[1], container_status[idx - 1]))
        idx = idx + 1
    db_conn.commit()


def main():
    get_docker_containers()
    # retreive all the docker containers
    # containers_all = get_all_containers()
    # set the status for every docker container within the current machine
    # container_status = retrieve_container_status(
    #     containers_active, containers_all)

    # create the db object
    # db_conn = create_container_db()
    # add the containers to the actual database
    # add_containers_to_db(db_conn, containers_all, container_status)


if __name__ == '__main__':
    main()
