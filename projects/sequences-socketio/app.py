# general imports
from flask_socketio import SocketIO
from flask_socketio import emit
from flask import Flask, render_template
from random import random
import time
from threading import Thread, Event
from threading import Lock

# local imports
import src.seq as tools

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


# define the background thread
def background_thread(arg1, arg2):
    """Example of how to send server generated events to clients."""

    # testing the bg task with extra arguments
    print('value of the arg1 is ' + str(arg1))
    print('value of the arg2 is ' + str(arg2))

    count = 1
    limit = arg2

    ok = True
    while ok:
        # generate a new random sequence every arg1 seconds
        # print('generating a new random sequence...')
        socketio.sleep(arg1)
        socketio.emit('sequence',
                      {"sequence": tools.get_sequence(), }
                      )
        if count == limit:
            print('task limit exceeded. stopping the background task...')
            ok = False
        count += 1


@app.route("/", methods=['GET'])
def show_index():
    sequence = tools.get_sequence()
    return render_template('index.html', sequence=sequence)


@socketio.on('connect')
def on_connect():
    print('Connection established...')
    # define the arguments to be used in the background task
    # arg1 represents the time between each iteration
    # arg2 represents the number of iterations
    arg1 = 5
    arg2 = 100

    global thread
    with thread_lock:
        if thread is None:
            print('server -> starting the background thread...')
            thread = socketio.start_background_task(
                background_thread, arg1=arg1, arg2=arg2)


@socketio.event
def request_sequence_calculation(msg):
    """handle the request to analyze a sequence"""
    sequence = msg['sequence']
    # print('server -> request to handle a sequence was received from the client')
    # print('the sequence:')
    tools.process_sequence(sequence)


@socketio.event
def stop_task():
    print('will stop the bg task')


def main():
    socketio.run(app, port=PORT, host=HOST)


if __name__ == '__main__':
    main()
