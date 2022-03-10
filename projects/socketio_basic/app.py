from distutils.log import debug
from socket import socket
from flask import Flask, render_template
from flask_socketio import SocketIO, emit


import src.local_tools as tools

PORT = 6969
LOCALHOST = '127.0.0.1'


# define the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route("/", methods=['GET', 'POST'])
def show_index():
    return render_template('index.html')


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)


def main():
    # app.run(debug=True, port=PORT)
    socketio.run(app,port=PORT,host=LOCALHOST,debug=True)


if __name__ == '__main__':
    main()
