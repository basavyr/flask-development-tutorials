from encodings import utf_8
import psutil
from datetime import datetime
import platform
import os
import subprocess
from subprocess import TimeoutExpired
from subprocess import PIPE


def execute_linux_command(cmd):
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    try:
        stdout, stderr = proc.communicate()
    except TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()

    return stdout.decode('utf_8'), stderr.decode('utf_8')


def give_graph_data():
    return f'this is some graph dada -> 📉'


def main():
    cmd1 = ['ls', '-la']
    cmd2 = ['uname', '-a']
    cmd3 = ['whoami']
    uname = execute_linux_command(cmd2)
    print(uname)


if __name__ == '__main__':
    main()
