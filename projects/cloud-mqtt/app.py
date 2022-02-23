from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)

PORT = 5055


def deliver_content(arg):
    return f'{arg}-{arg}'


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/s1/')
@app.route('/s1/<url_input>')
def service_1(url_input=None):
    return render_template("service1.html", input_name=url_input, delivered_content=deliver_content(url_input))


@app.route("/s2/")
def service_2():
    return render_template("service2.html")


@app.route("/s3/")
def service_3():
    return render_template("service3.html")


if __name__ == '__main__':
    app.run(debug=True, port=PORT)
