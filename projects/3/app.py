from flask import Flask

app = Flask(__name__)
app.debug = True  # https://stackoverflow.com/questions/17309889/how-to-debug-a-flask-app


# define a basic route without arguments
@app.route(rule='/')
def index():
    return '<h1>Hello World!</h1>'


# define a route which takes an argument and displays it as a paragpragh
@app.route(rule='/<name>')
def say_hi(name):
    return f'<h1>Flask App</h1>' + f'<p>Hello {name}!</p>'


if __name__ == '__main__':
    app.run()
