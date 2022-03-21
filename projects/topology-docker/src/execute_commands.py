from asyncio.subprocess import STDOUT
import subprocess
from subprocess import PIPE
from sys import stderr


def execute_docker_command(command, docker_id):
    cmd = ['docker', f'{command}', f'{docker_id}']
    process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    print(stdout)
    print(stderr)
    try:
        assert stderr == b'', 'Issue while executing the command'
    except AssertionError as issue:
        return -1
    else:
        return stdout.decode('utf-8')
