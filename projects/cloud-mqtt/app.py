from flask import Flask, render_template
from flask_bootstrap import Bootstrap


import tools

app = Flask(__name__)

PORT = 5055


def deliver_content():
    return tools.show_system_info()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/s1/', methods=['POST', 'GET'])
@app.route('/s1/<url_input>', methods=['POST', 'GET'])
def service_1(url_input=None):
    return render_template("service1.html", input_name=url_input)


@app.route("/s2/", methods=['POST', 'GET'])
@app.route("/s2/<var>", methods=['POST', 'GET'])
def service_2(var=None):
    """Shows information about the current system"""
    return render_template("service2.html", system_info=deliver_content(), system_info_parsed='⚙️', pressed_info=var)


@app.route("/s3/")
def service_3():
    current_time = tools.get_time()
    return render_template("service3.html", time=current_time)


if __name__ == '__main__':
    app.run(debug=True, port=PORT)
