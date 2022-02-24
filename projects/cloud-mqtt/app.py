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
def service_2():
    """Shows information about the current system"""
    raw_info = deliver_content()
    parsed_info = tools.detalied_info_stats()
    return render_template("service2.html",
                           system_info=raw_info, system_info_parsed=parsed_info,
                           current_time=tools.get_time(),
                           disk_info=tools.show_disk_info(),
                           memory_info=tools.show_MEM_info(),
                           swap_info=tools.show_SWAP_info(),
                           cpu_info=tools.show_CPU_info(),
                           )


@app.route("/s3/", methods=['POST', 'GET'])
def service_3():
    raw_time = tools.get_time()
    parsed_time = f'{raw_time}'[11:19]
    return render_template("service3.html",
                           unparsed_time=raw_time,
                           parsed_time=parsed_time)


if __name__ == '__main__':
    app.run(debug=True, port=PORT)
