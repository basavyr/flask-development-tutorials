import subprocess
from subprocess import PIPE
from subprocess import STDOUT
from sys import stderr, stdout
import subprocess
import psutil


def docker_ps():
    docker_cmd = ['docker', 'ps', '-a']
    process = subprocess.Popen(docker_cmd, stdout=PIPE, stderr=PIPE)

    stdout, stderr = process.communicate()

    if(stderr.decode('utf-8') == ''):
        return stdout.decode('utf-8')
    else:
        return ''


def get_system_info():
    return f'{psutil.virtual_memory()}'


def get_docker_containers():
    docker_containers = []
    containers = docker_ps().strip().split('\n')[1:]

    for container in containers:
        ct = container.split()
        docker_containers.append(f'{ct[0]}-{ct[1]}')

    return docker_containers


def main():
    containers = get_docker_containers()
    print(containers)


if __name__ == '__main__':
    main()
