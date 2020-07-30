import serial
import serial.tools.list_ports as spools
ports = spools.comports()

from flask import Flask,request
from flask import render_template, send_from_directory
import atexit
import time
import requests as req
from subprocess import call
from colorthief import ColorThief
import numpy as np
import random
# creates a Flask application, named app
app = Flask(__name__)
import glob

#connect to correct serial
sp = ""
for port, desc, hwid in sorted(ports):
        if desc.find("CircuitPlayground Express") > -1:
            sp = port

ser = serial.Serial(sp,9600)
time.sleep(.1)

def read():
    try:
        return ser.read_all()
    except:
        ser = serial.Serial(sp,9600)
        time.sleep(.1)
        return ser.read_all()

def write(inp):
    try:
        ser.write(bytearray(str(inp)+"\r\n",'ascii'))
    except:
        ser = serial.Serial(sp,9600)
        ser.write(bytearray(str(inp)+"\r\n",'ascii'))


print(read())

# a route where we will display a welcome message via an HTML template
@app.route("/")
def hello():
    return open("index.html").read()

# Custom static data
@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory('static/', filename)

#thanks stack https://stackoverflow.com/a/14032302/565514
@app.route('/lights/',defaults={'val': None}, methods=["GET","POST"])
@app.route('/lights/<val>', methods=["GET","POST"])
def light_post(val):
    if request.method == "POST":
        value = request.form['light'].strip()+"\n"
        print(value)
        write(value)
        print(read())

    elif request.method == "GET":
        try:
            val = val.replace("_",",")
        except:
            val = "0,0,0"
        if val == "rand":
            val = ("%i,%i,%i" % (jj(),jj(),jj()))
        value = val
        write(val)
    return value

def jj():
    return 255*round(random.random())
@app.route("/reset/")
def reset():
    write('\x04')
    return "reset"

@app.route("/match_screen/")
def screen():
    call(["screencapture", '-x',"screenshot.png"])
    call(["sips","-Z", "320","screenshot.png"])
    print("called")
    c = ColorThief('screenshot.png').get_palette(quality=10)
    print(c)
    pm = 0
    mi = [0,0,0]
    for i in c:
        a = np.abs(np.diff(i))
        for j in a:
            if j > pm:
                j = pm
                mi = tuple(a)
    c = mi
    col = str(c).replace("(","").replace(")","")
    write(col)
    return col


# run the application
if __name__ == "__main__":
    app.run(debug=True)
