# Start with a basic flask app webpage.
from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event


import src.local_tools as tools

PORT = 6969
LOCALHOST = '127.0.0.1'


# define the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# app.config['DEBUG'] = True

socketio = SocketIO(app)


@app.route("/", methods=['GET'])
def show_index():
    return render_template('index.html')


@socketio.on('connect')
def test_connect():
    print('Connection Established ')
    emit('connection response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on("test")
def test_message(message):
    print("received test message: " + message)
    # emit("test response", {"data": message})


@socketio.on('message')
def handle_message(data):
    print('this is on the server')
    print('received message: ' + data)
    emit(data)


def main():
    # app.run(debug=True, port=PORT)
    socketio.run(app, port=PORT, host=LOCALHOST, debug=True)


if __name__ == '__main__':
    main()
