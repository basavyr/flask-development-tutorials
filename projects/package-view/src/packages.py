import subprocess
from subprocess import PIPE
from subprocess import STDOUT

# return ann empty list of errors occurred during the execution of the command
EMPTY_LIST = ['No packages found']


def get_yum_packages():
    cmd = ['yum', 'list', 'installed']

    proc = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)

    try:
        stdout, stderr = proc.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()
        return EMPTY_LIST
    else:
        packages = str(stdout.decode('utf-8')).strip().split()
        with open('yum.packages.dat', 'w+') as writer:
            writer.write(str(packages))
        return packages


def get_brew_packages():
    """Retrieves all the manually installed packages on the system"""

    cmd = ['brew', 'list', '--versions']

    proc = subprocess.Popen(
        cmd, stdout=PIPE, stderr=PIPE)

    try:
        stdout, stderr = proc.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        return EMPTY_LIST
    else:
        # extract the packages as raw strings that are split only for new lines
        raw_packages = str(stdout.decode('utf-8')).strip().split('\n')

        # extract each package by splitting after whitespaces
        packages = [pack.split() for pack in raw_packages]
        print(packages[0])


get_brew_packages()
