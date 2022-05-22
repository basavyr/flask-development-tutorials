from multiprocessing import connection
import sqlite3 as db
import subprocess
from subprocess import PIPE, STDOUT


def execute_docker_ps():
    cmd = ['docker', 'ps', '-a']
    proc = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)

    try:
        raw_output, error = proc.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        return []
    else:
        output = raw_output.decode('utf-8').strip().split('\n')[1:]
        containers = []
        for out in output:
            out_t = out.split()
            container_id = out_t[0]
            container_name = out_t[1]
            containers.append((container_name, container_id))
        return containers


def store_docker_containers(db_file):
    """Execute a docker command to get all the containers and store them to a pre-defined database"""

    containers = execute_docker_ps()

    connection = db.connect(db_file)

    # open the cursor
    cursor = connection.cursor()

    # first create the table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Containers
                   (ContainerName TEXT, ContainerID Text)''')

    cursor.execute('''DELETE FROM Containers''')

    # add the containers into the db
    for container in containers:
        cursor.execute('''INSERT INTO Containers VALUES (?,?)''', container)

    connection.commit()
    connection.close()


def get_containers(db_file):
    container_db = store_docker_containers(db_file)

    connection = db.connect(db_file)

    cursor = connection.cursor()

    containers = cursor.execute('''SELECT * FROM Containers''').fetchall()

    return containers
