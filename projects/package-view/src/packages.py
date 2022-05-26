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


raw_packages = """
elfutils-debuginfod-client-devel.x86_64 0.185-1.el8                                    @baseos
elfutils-devel.x86_64                   0.185-1.el8                                    @baseos
elfutils-libelf-devel.x86_64            0.185-1.el8                                    @baseos
gettext-common-devel.noarch             0.19.8.1-17.el8                                @baseos
gettext-devel.x86_64                    0.19.8.1-17.el8                                @baseos
glibc-devel.x86_64                      2.28-164.el8_5.3                               @baseos
kernel-devel.x86_64                     4.18.0-348.20.1.el8_5                          @baseos
keyutils-libs-devel.x86_64              1.5.10-9.el8                                   @baseos
krb5-devel.x86_64                       1.18.2-14.el8                                  @baseos
libcom_err-devel.x86_64                 1.45.6-2.el8                                   @baseos
libselinux-devel.x86_64                 2.9-5.el8                                      @baseos
libsepol-devel.x86_64                   2.9-3.el8                                      @baseos
libstdc++-devel.x86_64                  8.5.0-4.el8_5                                  @appstream
libverto-devel.x86_64                   0.3.0-5.el8                                    @baseos
libxcrypt-devel.x86_64                  4.1.1-6.el8                                    @baseos
libzstd-devel.x86_64                    1.4.4-1.el8                                    @baseos
mariadb-connector-c-devel.x86_64        3.1.11-2.el8_3                                 @appstream
openssl-devel.x86_64                    1:1.1.1k-6.el8_5                               @baseos
pcre2-devel.x86_64                      10.32-2.el8                                    @baseos
platform-python-devel.x86_64            3.6.8-41.el8.rocky.0                           @appstream
python2-devel.x86_64                    2.7.18-7.module+el8.5.0+718+67e45b5f.rocky.0.2 @appstream
python36-devel.x86_64                   3.6.8-38.module+el8.5.0+671+195e4563           @appstream
systemtap-devel.x86_64                  4.5-3.el8                                      @appstream
valgrind-devel.x86_64                   1:3.17.0-5.el8                                 @appstream
xz-devel.x86_64                         5.2.4-3.el8.1                                  @baseos
zlib-devel.x86_64                       1.2.11-17.el8                                  @baseos
"""

command = "yum list --installed | more | grep devel"


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
    vm_topic = f'{OPENSTACK_TOPIC}{user_id}/{vm_id}'
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


def write_test_packages_on_db(userID, vm_id):
    packages = [pack.split() for pack in raw_packages.strip().split('\n')]

    pack_file = Path(f'{server_path}{userID}.VM-{vm_id}.packages.db')
    pack_file.touch(exist_ok=True)

    db = sqlite3.connect(pack_file)
    cursor = db.cursor()

    # first create the table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Packages
                        (Name TEXT, Version TEXT, Description TEXT)''')

    # keep the db always clean
    cursor.execute('''DELETE FROM Packages''')

    for pack in packages:
        db_item = (pack[0], pack[1], pack[2])
        cursor.execute('''INSERT INTO Packages VALUES (?,?,?)''', db_item)

    db.commit()
    db.close()


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
    write_test_packages_on_db(userID, vm_id)

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
