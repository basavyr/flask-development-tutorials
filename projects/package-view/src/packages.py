from email.contentmanager import raw_data_manager
from multiprocessing import connection
import subprocess
from subprocess import PIPE
from subprocess import STDOUT
from pathlib import Path
import sqlite3
import random


import time
import paho.mqtt.client as mqtt

# define the server parameters
OPENSTACK_BROKER = "127.0.0.1"
OPENSTACK_PORT = 1883
OPENSTACK_TOPIC = "/openstack/cloudifin/servers/"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def publish_command(user_id, vm_id, command):
    client = mqtt.Client(str(user_id))
    client.on_connect = on_connect

    # start the connection in order to publish messages on the proper topic
    client.connect(OPENSTACK_BROKER, OPENSTACK_PORT)
    client.loop_start()
    vm_topic = f'{OPENSTACK_TOPIC}{vm_id}'
    print(f'Will publish on the topic: {vm_topic}')
    client.publish(vm_topic, command)
    client.loop_stop()


# return ann empty list of errors occurred during the execution of the command
EMPTY_LIST = []

server_path = 'db/'


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


def write_packages_on_db(userID, vm_id):
    """Retrieves all the manually installed packages on the system"""

    cmd = ['brew', 'list', '--versions']

    proc = subprocess.Popen(
        cmd, stdout=PIPE, stderr=PIPE)

    try:
        stdout, stderr = proc.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        return len(EMPTY_LIST)
    else:

        pack_file = Path(f'{server_path}{userID}.VM-{vm_id}.packages.db')
        pack_file.touch(exist_ok=True)

        # extract the packages as raw strings that are split only for new lines
        raw_packages = str(stdout.decode('utf-8')).strip().split('\n')

        packages = [pack.split() for pack in raw_packages]

        db = sqlite3.connect(pack_file)

        cursor = db.cursor()

        # first create the table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Packages
                        (PackageName TEXT, PackageVersion TEXT)''')

        # keep the db always clean
        cursor.execute('''DELETE FROM Packages''')

        # only select a random number of data points to make the db
        number_of_items = random.randint(3, 7)
        packages = packages[0:number_of_items]

        for pack in packages:
            db_item = (pack[0], pack[1])
            cursor.execute('''INSERT INTO Packages VALUES (?,?)''', db_item)

        db.commit()
        db.close()


def get_vm_packages(userID, vm_id):
    # first make sure db exists and update it
    write_packages_on_db(userID, vm_id)

    db = sqlite3.connect(f'{server_path}{userID}.VM-{vm_id}.packages.db')

    cursor = db.cursor()

    packages = cursor.execute('''SELECT * FROM Packages''').fetchall()

    return packages


def execute_check_update(userID, vm_id, package_name):
    print(f'From: {userID}')
    print(f'will check update for {package_name} on VM: {vm_id}')
    # shell command to be executed on the selected VM
    command = f'yum check-update | grep {package_name}'
    publish_command(userID, vm_id, command)


def execute_update(userID, vm_id, package_name):
    print(f'From: {userID}')
    print(f'will update {package_name} on VM: {vm_id}')
    # shell command to be executed on the selected VM
    command = f'yum update {package_name}'
    publish_command(userID, vm_id, command)
