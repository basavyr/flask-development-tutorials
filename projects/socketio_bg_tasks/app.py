from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask import Flask, render_template
from random import random
from time import sleep
from threading import Thread, Event


# define the port and host that the app will run on
PORT = 6868
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


@socketio.on('connect')
def on_connect():
    print('Client connected')
    emit('connected', {'data': 'Connected',
                       'status': 1})


@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected...')
    # emit('disconnect', {'data': 'Disconnected',
    #                     'status': 1})


# only use this for testing
@socketio.on('message')
def on_message(message):
    print('Server -> recieved from client: ' + message)


# trigger the retreival of system info
@socketio.on('system_info_request')
def sir_handler(data):
    # print('server -> system information have been requested by the server')
    # print(f'data: {data}')
    emit('system_info_response', {'data': 'System information',
                                  'status': 1,
                                  })


def main():
    socketio.run(app, port=PORT, host=LOCALHOST)


if __name__ == '__main__':
    main()
