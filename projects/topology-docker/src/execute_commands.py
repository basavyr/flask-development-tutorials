from asyncio.subprocess import STDOUT
from concurrent.futures import process
from pickle import EMPTY_LIST
import subprocess
from subprocess import PIPE
from sys import stderr
import json


EMPTY_LIST = []


def execute_docker_command(command, docker_id):
    cmd = ['docker', f'{command}', f'{docker_id}']

    # print('before POPEN')
    process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    # print('after POPEN')

    # print('before communicate()')
    stdout, stderr = process.communicate()
    # print('after communicate()')

    if (stdout.decode('utf-8').strip() == str(docker_id)):
        print('Docker container state was successfully changed')

    try:
        assert stderr == b'', 'Issue while executing the command'
    except AssertionError as issue:
        print(issue)
        print(stderr.decode('utf-8'))
        return -1
    else:
        return stdout.decode('utf-8')


def execute_docker_inspect(docker_id):
    command = ['docker', 'inspect', f'{docker_id}']

    process = subprocess.Popen(command, stdout=PIPE, stderr=PIPE)

    try:
        stdout, stderr = process.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        process.kill()
        return -1
    else:
        docker_file = f'docker.{docker_id}.inspect.dat'
        with open(docker_file, 'w+') as writer:
            writer.write(stdout.decode('utf-8'))

    return docker_file


def process_string(docker_file):
    with open(docker_file, 'r+') as reader:
        y = json.loads(reader.read().strip())
        container_IP = print(y[0]['NetworkSettings']['IPAddress'])
        container_Gateway = print(y[0]['NetworkSettings']['Gateway'])
        container_MacAddress = print(y[0]['NetworkSettings']['MacAddress'])

    return [container_IP, container_Gateway, container_MacAddress]
