from re import S
import subprocess
from subprocess import PIPE
import sqlite3 as db

UTF8 = 'utf-8'


def get_containers():
    """
    - retrieve a list of containers
    """
    cmd = ['docker', 'ps']

    docker = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = docker.communicate()

    try:
        assert stderr == b'', 'Error when retrieving the containers'
    except AssertionError:
        return ''
    else:
        return stdout.decode(UTF8)


def manipulate_container_string(raw_string):
    raw_dockers = raw_string.strip()
    raw_dockers = str(raw_dockers).split('\n')[1:]
    dockers = [x.split() for x in raw_dockers]
    # print('Containers:')
    # for container in dockers:
    #     print(container)
    docker_ids = [container[0] for container in dockers]
    docker_names = [container[1] for container in dockers]
    # print(docker_ids)
    # print(docker_names)
    return docker_ids, docker_names


def main():
    raw_containers = get_containers()
    manipulate_container_string(raw_containers)


if __name__ == '__main__':
    main()
