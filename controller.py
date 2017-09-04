from flask import Flask, request
import json
import os
from os.path import expanduser
import socket
import win32com.client
import win32con
import win32api
shell = win32com.client.Dispatch("WScript.Shell")

app = Flask(__name__)

def expand(path):
    if path.startswith('~'):
        path = path[1:]
        path = expanduser("~") + path
    return path

@app.route("/fetch")
def fetch_shows():
    dir = request.args.get('directory')
    dir = expand(dir)
    if os.path.isfile(dir):
        os.startfile(dir)
        dir = '/'.join(dir.split('/')[:-1])
    dirs = filter(lambda x: not x.startswith('.'), os.listdir(dir))
    return json.dumps(list(dirs))


@app.route("/maximize")
def maximize():
    shell.SendKeys('m')
    return ok()

@app.route("/pause")
def pause():
    shell.SendKeys(' ')
    return ok()

@app.route("/volume")
def volume():
    cmd = request.args.get('direction')
    if cmd == 'up':
        shell.SendKeys('{UP}')
    elif cmd == 'down':
        shell.SendKeys('{DOWN}')
    return ok()

@app.route("/rewind")
def rewind():
    shell.SendKeys('{LEFT}')
    return ok()

@app.route("/fast_forward")
def fast_forward():
    shell.SendKeys('{RIGHT}')
    return ok()

@app.route("/left_click")
def left_click():
    x, y = win32api.GetCursorPos()
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    return ok()

@app.route("/right_click")
def right_click():
    x, y = win32api.GetCursorPos()
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
    return ok()

@app.route("/move_mouse")
def move_mouse():
    x, y = win32api.GetCursorPos()
    x_diff = request.args.get('x')
    y_diff = request.args.get('y')
    win32api.SetCursorPos((int(x + float(x_diff)), int(y + float(y_diff))))
    return ok()

def ok():
    return json.dumps({'result': 'OK'})

print("IP is ", socket.gethostbyname(socket.gethostname()))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
