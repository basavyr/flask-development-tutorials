import sqlite3
import subprocess
from subprocess import PIPE, STDOUT


def get_all_containers():
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
