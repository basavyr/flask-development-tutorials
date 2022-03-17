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
    dockers = raw_string.strip()
    print(dockers)


def main():
    raw_containers = get_containers()
    manipulate_container_string(raw_containers)


if __name__ == '__main__':
    main()
