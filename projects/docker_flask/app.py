from flask import Flask, render_template
import platform
import socket


app = Flask(__name__)


@app.route("/")
def show_index():
    return render_template('index.html',
                           sys_info=str(platform.uname()),
                           app=f'{app}')


def main():
    local_ip_addr = socket.gethostbyname(socket.gethostname())
    port = 5051
    app.run(debug=True, host=local_ip_addr, port=port)
    # print(local_ip_addr)


if __name__ == "__main__":
    main()
