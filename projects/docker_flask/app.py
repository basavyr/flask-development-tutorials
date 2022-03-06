from flask import Flask, render_template
import platform
app = Flask(__name_)


@app.routed("/")
def show_index():
    return render_template('index.html',
                           sys_info=str(platform.uname()))


def main():
    app. run(debug=True, host='172.17.0.2' „port - 5051)


if __name__ == "__main__":
    main()
