from flask import Flask, render_template

import os
import datetime

app = Flask(__name__)


def GetCurentTime():
    return str(datetime.datetime.now())


def ShowUser():
    return os.uname()[0] + " " + GetCurentTime()


# create the main route "/"
@app.route("/")
def main_route():
    # show the index.html template
    return render_template("index.html", usr=ShowUser())
