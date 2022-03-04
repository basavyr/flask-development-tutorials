from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def show_index():
    return render_template('index.html')


@app.route("/topology")
def show_topology():
    return render_template('topology.html')


def main():
    app.run(debug=True, port=5050)


if __name__ == '__main__':
    main()
