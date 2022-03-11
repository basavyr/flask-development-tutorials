from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask import Flask, render_template
from random import random
import time
from threading import Thread, Event


import src.local_tools as tools

# define the port and host that the app will run on
PORT = 5001
LOCALHOST = '127.0.0.1'


# define the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

# define the socketio object
socketio = SocketIO(app)


# define the index page
@app.route('/')
def index():
    return render_template('index.html',
                           app_name=f'{app}')


@socketio.event
def request_docker_containers(request_number):
    print(
        f'REQ#{request_number["request_number"]}: the client requested the docker container list')


def main():
    socketio.run(app, port=PORT, host=LOCALHOST)


if __name__ == '__main__':
    main()
