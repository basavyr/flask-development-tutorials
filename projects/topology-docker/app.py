from crypt import methods
from flask_socketio import SocketIO
from flask_socketio import emit
from flask import Flask, render_template
from random import random
import time
from threading import Thread, Event
from threading import Lock


from src.container_db import get_container_db
import src.table_generator as table
import src.execute_commands as exe

# define the port and host that the app will run on
PORT = 5051
HOST = '127.0.0.1'


async_mode = None

thread = None
thread_lock = Lock()


# define the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

# define the socketio object
socketio = SocketIO(app, async_mode=async_mode)


@app.route('/', methods=['GET', 'POST'])
def show_index():
    return render_template('index.html')


@app.route('/docker', methods=['GET', 'POST'])
def show_docker():
    # get the docker containers via the list -> db -> list  workflow
    docker_containers = get_container_db()
    print(docker_containers)
    return render_template('view.html',
                           docker_containers=docker_containers)


@socketio.event
def request_container_db():
    print(f'Refreshing the docker database')

    docker_containers = get_container_db()
    print(docker_containers)
    try:
        n_rows = len(docker_containers)
        n_cols = len(docker_containers[0])
    except TypeError as issue:
        print('In <<< request_container_db() >>>')
        print('sio event error')
        print(issue)
        return
    else:
        pass
    T = table.table(['Container ID', 'Image', 'Container Name', 'Container Status'],
                    docker_containers, n_rows, n_cols)
    emit('receive_container_db', {
        "db": docker_containers,
        "table": T,
    })


@socketio.event
def docker_action(msg):
    if msg['req'] == 'START':
        exe.execute_docker_command('start', msg['container_id'])
    elif msg['req'] == 'STOP':
        exe.execute_docker_command('stop', msg['container_id'])

    # add blocking operation in order to emit a changed state of the container within the database
    time.sleep(1)

    containers = tools.get_docker_containers()

    n_rows = len(containers)
    n_cols = len(containers[0])
    T = table.table(['Container ID', 'Image', 'Container Name', 'Container Status'],
                    containers, n_rows, n_cols)

    emit('receive_container_db', {
        "db": containers,
        "table": T,
    })


@socketio.event
def request_container_details(msg):
    container = str(msg['container_id'])
    print(f'Will process container #{container}')
    emit('response_container_details', {"status": 'CLICK', "id": container})


def main():
    socketio.run(app, port=PORT, host=HOST)


if __name__ == '__main__':
    main()
