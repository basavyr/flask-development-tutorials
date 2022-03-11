from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask import Flask, render_template
from random import random
import time
from threading import Thread, Event


import src.local_tools as tools

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
    print('server -> system information have been requested by the client: ' +
          data['clientid'])
    time.sleep(3)
    try:
        emit('system_info_response', {'header': 'System information',
                                      'data': tools.get_uname(),
                                      'status': 1,
                                      })
    except Exception as issue:
        emit('system_info_response', {'header': 'System information',
                                      'data': '',
                                      'status': 0,
                                      })
    finally:
        print('sent the response to the client')


# trigger the vm retrieval when a 'get_vm_list' event arrives
@socketio.event
def get_vm_list():
    vm_list = tools.generate_vm_list()
    emit('vm_list_response', {'vm_list': vm_list})


def main():
    socketio.run(app, port=PORT, host=LOCALHOST)


if __name__ == '__main__':
    main()
