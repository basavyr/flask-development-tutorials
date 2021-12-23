from flask import Flask

# define the application
app = Flask(__name__)


#set the application port
app.config['PORT'] = 5001

# create a route
@app.route("/")
def hello():
    # return a an html paragraph with the text Hello World
    return "<p1>Hello World!</p1>"


# add another route
@app.route("/about")
def about():
    # return a an html paragraph with the text Hello World
    return "<p1>About Us!</p1>"
