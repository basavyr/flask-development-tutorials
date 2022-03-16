# general imports
from flask_socketio import SocketIO
from flask_socketio import emit
from flask import Flask, render_template
from random import random
import time
from threading import Thread, Event
from threading import Lock


import src.workflow as tools


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
sio = SocketIO(app, async_mode=async_mode)


@app.route("/", methods=['GET', 'POST'])
def show_index():
    return render_template('index.html')


@sio.on('client-request')
def request(msg):
    c_id = str(msg['client'])
    topic = str(msg['topic'])
    message = str(msg['msg']) + " from client: " + c_id
    tools.process_client(topic, message, c_id)


def main():
    sio.run(app, port=PORT, host=HOST)


if __name__ == '__main__':
    main()
