# general imports
from crypt import methods
from flask_socketio import SocketIO
from flask_socketio import emit
from flask import Flask, render_template
from random import random
import time
from threading import Thread, Event
from threading import Lock


import src.container_db as tools
import src.table_generator as table


# define the port and host that the app will run on
PORT = 5051
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


@app.route('/', methods=['GET', 'POST'])
def show_index():
    return render_template('index.html')


@app.route('/docker', methods=['GET', 'POST'])
def show_docker():
    docker_containers = tools.get_docker_containers()
    return render_template('view.html',
                           docker_containers=docker_containers)


@socketio.event
def request_container_db():
    print(f'Refreshing the docker database')

    containers = tools.get_docker_containers()
    n_rows = len(containers)
    n_cols = len(containers[0])
    T = table.table(['header1', 'header2', 'header3', 'header4'],
                    containers, n_rows, n_cols)
    emit('receive_container_db', {
        "db": containers,
        "table": T,
    })


def main():
    socketio.run(app, port=PORT, host=HOST)


if __name__ == '__main__':
    main()
