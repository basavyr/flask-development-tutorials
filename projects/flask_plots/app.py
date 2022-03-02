from flask import Flask, render_template


import base64
from io import BytesIO
from matplotlib.figure import Figure


import plotter

app = Flask(__name__)


@app.route("/")
def indexhtml():
    return render_template('index.html', message='ok')


@app.route('/1', methods=['POST', 'GET'])
def plot_example1():
    return render_template('plot1.html',
                           plot1=plotter.plot_data(),
                           plot2=plotter.plot_data(),
                           plot3=plotter.plot_data())


@app.route('/2', methods=['POST', 'GET'])
def plot_example2():
    return render_template('plot2.html',
                           disk_pie_chart=plotter.disk_pie_chart(),
                           swap_pie_chart=plotter.swap_pie_chart(),
                           virtual_memory_pie_chart=plotter.virtual_memory_pie_char(),
                           cpu_chart=plotter.cpu_info_chart(),
                           node_name='testNode-01',
                           )


@app.route('/3')
def plot_example3():
    return render_template('plot3.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
