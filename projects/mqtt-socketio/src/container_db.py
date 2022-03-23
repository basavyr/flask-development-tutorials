import gc
from re import S
import subprocess
from subprocess import PIPE
import sqlite3 as db
from webbrowser import get

UTF8 = 'utf-8'


def get_running_containers():
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


def get_container_ids(raw_list):
    raw_dockers = raw_list.strip()
    raw_dockers = str(raw_dockers).split('\n')[1:]

    dockers = [x.split() for x in raw_dockers]

    docker_ids = [container[0] for container in dockers]

    return docker_ids


def get_container_names(raw_list):
    raw_dockers = raw_list.strip()
    raw_dockers = str(raw_dockers).split('\n')[1:]

    dockers = [x.split() for x in raw_dockers]

    docker_names = [container[1] for container in dockers]

    return docker_names


def main():
    raw_containers = get_running_containers()
    docker_containers_id = get_container_ids(raw_containers)
    docker_containers_names = get_container_names(raw_containers)
    print(docker_containers_id)
    print(docker_containers_names)


if __name__ == '__main__':
    main()
