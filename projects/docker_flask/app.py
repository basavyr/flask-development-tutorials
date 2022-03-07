from flask import Flask, render_template
import platform
import socket


app = Flask(__name__)


@app.route("/")
def show_index():
    return render_template('index.html',
                           sys_info=str(platform.uname()))


def main():
    #app.run(debug=True, host='172.17.0.2',port=5051)
    local_ip_addr=socket.gethostbyname(socket.gethostname())
    print(local_ip_addr)

if __name__ == "__main__":
    main()


