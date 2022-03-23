from crypt import methods
from flask_socketio import SocketIO
from flask_socketio import emit
from flask import Flask, render_template
import time
from threading import Thread, Event
from threading import Lock


from src.container_db import get_container_db
from src.container_db import EMPTY_LIST
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
    return render_template('view.html')


@socketio.event
def request_container_db():
    # print(f'Refreshing the docker database')
    # get the docker containers via the list -> db -> list  workflow
    docker_containers = get_container_db()
    if docker_containers == EMPTY_LIST:
        emit('docker_db_fail', {
             'msg': 'Issue when retreiving the database with docker containers'})
    else:
        try:
            n_rows = len(docker_containers)
            n_cols = len(docker_containers[0])
        except TypeError as issue:
            print('In <<< request_container_db() >>>')
            print('sio event error')
            print(issue)
            emit('docker_db_fail', {
                'msg': 'Issue when retreiving the database with docker containers'})
        else:
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

    docker_containers = get_container_db()

    n_rows = len(docker_containers)
    n_cols = len(docker_containers[0])

    T = table.table(['Container ID', 'Image', 'Container Name', 'Container Status'],
                    docker_containers, n_rows, n_cols)

    emit('receive_container_db', {
        "db": docker_containers,
        "table": T,
    })


@socketio.event
def request_container_details(msg):
    container = str(msg['container_id'])
    status = str(msg['status'])

    # print(f'Will process container #{container}')
    # print(f'Status of the container: {status}')

    container_inspect = exe.execute_docker_inspect(container)
    if(container_inspect != -1):
        container_info = exe.process_string(container_inspect)
    else:
        container_info = ['-', '-', '-']

    if(status == 'active'):
        emit('response_container_details', {
             "status": 1, "id": container, "info": container_info, })
    else:
        emit('response_container_details', {
             "status": 0, "id": container, "info": container_info, })


def main():
    socketio.run(app, port=PORT, host=HOST)


if __name__ == '__main__':
    main()
