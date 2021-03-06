# general imports
from asyncio.subprocess import DEVNULL
from flask_socketio import SocketIO
from flask_socketio import emit
from flask import Flask, render_template
from threading import Lock
import subprocess
import glob
import os

# local imports
import src.active_containers as containers_db
import src.active_vms as vm_db
import src.packages as pack
import src.graphs as graf
import src.stats as stats


VM_DB = "db/userID.openstack.VM.list.db"
CONTAINER_DB = "db/userID.VM.containers.db"
CLOUD_CONTAINER_DB = "db/ccdb.db"


# define the port and host that the app will run on
PORT = 6969
HOST = '127.0.0.1'


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
# source of the doc => https://github.com/miguelgrinberg/Flask-SocketIO/blob/main/example/app.py
async_mode = None

thread = None
thread_lock = Lock()


# define the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

# define the socketio object
socketio = SocketIO(app, async_mode=async_mode)


USER_ID = 'user69'


@app.route("/", methods=['GET', 'POST'])
def show_index():
    return render_template('index.html',
                           user_id=USER_ID)


@app.route('/packages', methods=['GET', 'POST'])
def show_packages():
    return render_template('packages.html',
                           user_id=USER_ID)


@app.route('/topology', methods=['GET', 'POST'])
def show_topology():
    return render_template('topology.html',
                           user_id=USER_ID)


@app.route('/stats', methods=['GET', 'POST'])
def show_system_statistics():
    graph_template = 'system_statistics.html'
    graph_data = graf.give_graph_data()

    return render_template(graph_template,
                           graph_data=graph_data,
                           disk_pie_chart=graf.disk_pie_chart(),
                           swap_pie_chart=graf.swap_pie_chart(),
                           virtual_memory_pie_chart=graf.virtual_memory_pie_char(),
                           cpu_chart=graf.cpu_info_chart(),
                           node_name=graf.get_node_name(),
                           sys_info=graf.get_sys_info(),
                           time_stamp=graf.get_timestamp(),
                           arch=graf.get_platform_arch(),
                           cpu_info=graf.get_cpu_info(),
                           user_id=USER_ID,
                           )


###################################
# define any socketIO event
###################################


@socketio.event
def on_connect(payload):
    pass


# the vms that will be returned when 'package-management' module is selected
@socketio.event
def refresh_instances():
    print('User requested VM list')

    # clean the db dir
    for db_file in glob.glob('db/user69.*'):
        os.remove(db_file)

    active_vms = [(vm[0], vm[1])
                  for vm in vm_db.get_user_vms(CLOUD_CONTAINER_DB)]
    emit('instances', {'vms': active_vms})


# the vms that will be returned when 'system-statistics' module is selected
@socketio.event
def refresh_instances_stats():
    print('User requested VM list')

    # clean the db dir
    for db_file in glob.glob('db/user69.*'):
        os.remove(db_file)

    active_vms = [(vm[0], vm[1])
                  for vm in vm_db.get_user_vms(CLOUD_CONTAINER_DB)]
    emit('instances_stats', {'vms': active_vms})


@socketio.event
def vm_selected(data):
    vm_id = data['vm_id']
    vm_name = data['vm_name']

    # run the shell command for getting the packages that are installed on the current vm
    vm_packages = pack.get_vm_packages(USER_ID, vm_id)
    emit('vm_packages', {'vm_packages': vm_packages})

    # get the active containers and put them into the dropdown list
    vm_containers = containers_db.get_vm_containers(USER_ID, vm_id)
    emit('available_vm_containers', {'vm_containers': vm_containers})


@socketio.event
def check_update(data):
    vm_id = data['vm_id']
    package_name = data['package']
    pack.execute_check_update(USER_ID, vm_id, package_name)


@socketio.event
def update(data):
    vm_id = data['vm_id']
    package_name = data['package']
    pack.execute_update(USER_ID, vm_id, package_name)


@socketio.event
def get_vm_stats(data):
    vm_id = data['vm_id']
    print(f'Will get stats for the VM with ID: {vm_id}')
    stats.publish_command(USER_ID, vm_id)

###################################
# main function
###################################


def main():
    socketio.run(app, port=PORT, host=HOST, debug=True)


if __name__ == '__main__':
    main()
