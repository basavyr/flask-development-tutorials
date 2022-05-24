# general imports
from crypt import methods
from distutils.log import debug
from flask_socketio import SocketIO
from flask_socketio import emit
from flask import Flask, render_template
import random
import time
from threading import Thread, Event
from threading import Lock

import src.active_containers as containers_db
import src.active_vms as vm_db
import src.packages as pack


VM_DB = "db/userID.openstack.VM.db"
CONTAINER_DB = "db/userID.VM.containers.db"


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
    return render_template('system_statistics.html',
                           user_id=USER_ID)


###################################
# define any socketIO event
###################################


@socketio.event
def on_connect(payload):
    print(payload['msg'])


@socketio.event
def refresh_instances():
    print('User requested VM and Container list')
    active_vms = [(vm[0], vm[1]) for vm in vm_db.get_user_vms(VM_DB)]
    emit('instances', {'vms': active_vms})


@socketio.event
def vm_selected(data):
    vm_id = data['vm_id']
    vm_name = data['vm_name']
    print(vm_id, vm_name)
    vm_containers = containers_db.get_vm_containers(USER_ID, vm_id)
    # print(vm_containers)
    emit('available_vm_containers', {'vm_containers': vm_containers})

###################################
# main function
###################################


def main():
    socketio.run(app, port=PORT, host=HOST, debug=True)


if __name__ == '__main__':
    main()
