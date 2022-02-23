from flask import Flask, render_template
from flask_bootstrap import Bootstrap


def sayhi():
    return f'Hello there'


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, port=5055)
