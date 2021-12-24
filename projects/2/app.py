from flask import Flask, render_template

import os
import datetime

app = Flask(__name__)


def GetCurentTime():
    return str(datetime.datetime.now())


def ShowUser():
    return os.uname()[0] + " " + GetCurentTime()


def Create_User_Data(data_file):
    # check of the data file exists
    if os.path.isfile(data_file):
        with open(data_file, "r") as file:
            data = file.readlines()
    else:
        data = ['inexistent file']

    clean_data = []
    for data_line in data:
        clean_data.append(data_line.strip())

    return clean_data


# create the main route "/"
@app.route("/")
def main_route():
    # show the index.html template
    return render_template("index.html", usr=ShowUser())


# create a route with some data
@app.route("/data")
def data_route():
    return render_template("data.html", data=Create_User_Data("data.txt"))


@app.route("/items", methods=['GET', 'POST'])
def items():
    items = ['item1', 'item2', 'item3']
