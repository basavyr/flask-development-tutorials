from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask import Flask, render_template
from random import random
import time
from threading import Thread, Event
from threading import Lock


import src.local_tools as tools

# define the port and host that the app will run on
PORT = 5001
LOCALHOST = '127.0.0.1'


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None
# threads
thread = None
thread_lock = Lock()


# define the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

# define the socketio object
socketio = SocketIO(app, async_mode=async_mode)


# define the index page
@app.route('/')
def index():
    return render_template('index.html',
                           app_name=f'{app}')


@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            print('nice')
            # thread = socketio.start_background_task(background_thread)
    # emit('my_response', {'data': 'Connected', 'count': 0})
    emit('psutil-info',
         {"virtual_memory": tools.get_system_info(), }
         )


@socketio.event
def request_docker_containers(request_number):
    print(
        f'REQ#{request_number["request_number"]}: the client requested the docker container list')

    container_list = tools.get_docker_containers()

    # take a break to make sure the container list is properly processed
    # time.sleep(1)

    # send the container list once it has been retrieved
    emit('response_docker_containers', {"container_list": container_list, })
    print('the container list has been sent to the client')


@socketio.event
def request_docker_container_info(message):
    container = message['container_name']
    print(f'will get info about the container {container}')


def main():
    socketio.run(app, port=PORT, host=LOCALHOST)


if __name__ == '__main__':
    main()
