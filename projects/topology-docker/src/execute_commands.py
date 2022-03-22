from asyncio.subprocess import STDOUT
import subprocess
from subprocess import PIPE
from sys import stderr


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
