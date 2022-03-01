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
                           plot1=plotter.make_plot(),
                           plot2=plotter.make_plot(),
                           plot3=plotter.make_plot())


@app.route('/2')
def plot_example2():
    return render_template('plot2.html',
                           pie_chart1=1,
                           pie_chart2=1,
                           pie_chart3=1)


@app.route('/3')
def plot_example3():
    return render_template('plot3.html')


if __name__ == "__main__":
    app.run(debug=False, port=5000)