from flask_socketio import SocketIO
from flask_socketio import emit
from flask import Flask, render_template
from random import random
import time
from threading import Thread, Event
from threading import Lock


import src.seq as tools

# define the port and host that the app will run on
PORT = 5051
HOST = '127.0.0.1'


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


# define the background thread
def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    limit = 20

    ok = True
    while ok:
        # generate a new random sequence every 5 seconds
        # print('generating a new random sequence...')
        socketio.sleep(5)
        socketio.emit('sequence',
                      {"sequence": tools.get_sequence(), }
                      )
        count += 1
        if count == limit:
            ok = False


@app.route("/", methods=['GET'])
def show_index():
    sequence = tools.get_sequence()
    return render_template('index.html', sequence=sequence)


@socketio.on('connect')
def on_connect():
    global thread
    with thread_lock:
        if thread is None:
            print('server -> starting the background thread...')
            thread = socketio.start_background_task(background_thread)


@socketio.event
def request_sequence_calculation(msg):
    """handle the request to analyze a sequence"""
    print('server -> request to handle a sequence was recieved from the client')


def main():
    socketio.run(app, port=PORT, host=HOST)


if __name__ == '__main__':
    main()
