# Start with a basic flask app webpage.
from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event


import src.local_tools as tools

# define the port and host that the app will run on
PORT = 6969
LOCALHOST = '127.0.0.1'


# define the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# app.config['DEBUG'] = True

# define the socketio object
socketio = SocketIO(app)


# define the main page
@app.route("/", methods=['GET'])
def show_index():
    return render_template('index.html', time=tools.get_time())


@socketio.on('connect')
def test_connect():
    # this sends a dict to the client
    emit('connection_response',
         {
             'message': 'Connection Established',
             'time': tools.get_time()
         })


@socketio.on('disconnect')
def test_disconnect():
    pass
    # print('Client disconnected')


# define the tree test channels
@socketio.event
def channel1(data):
    emit('channel1 response', {'data': data})


@socketio.on('channel2')
def channel2(data):
    print('server -> received args on channel2 from client: ' + data)
    emit('channel2 response', {
        'time': tools.get_time(),
        'user': tools.get_uname(),
        'content': data,
    }
    )


@socketio.event
def channel3(data):
    emit('channel3 response', {'data': data})


# log any incoming message that was emitted by the client
@socketio.on('message')
def handle_unnamed_message(data):
    print('...(received from client)...')
    print(f'Server-side message: {data}')
    print('...')
    emit('message', {'data': data})


def main():
    # app.run(debug=True, port=PORT)
    socketio.run(app, port=PORT, host=LOCALHOST, debug=True)


if __name__ == '__main__':
    main()
