import os
from flask import Flask, render_template, redirect, url_for

from config import Config

app = Flask(__name__)

@app.route('/')
def index():
    state = 'HOME Now'
    return render_template('index.html', state=state)

@app.route('/stop')
def do_stopping():
    os.system('irsend SEND_ONCE {0} {1}'.format(Config.CONTROLLER_NAME, Config.SIGNALS['stop']))
    state = 'Now Stopping'
    return render_template('index.html', state=state)

@app.route('/warm')
def do_warming():
    os.system('irsend SEND_ONCE {0} {1}'.format(Config.CONTROLLER_NAME, Config.SIGNALS['warm']))
    state = 'Now Warming'
    return render_template('index.html', state=state)

@app.route('/cool')
def do_cooling():
    os.system('irsend SEND_ONCE {0} {1}'.format(Config.CONTROLLER_NAME, Config.SIGNALS['cool']))
    state = 'Now Cooling'
    return render_template('index.html', state=state)

if __name__ == '__main__':
    app.run()
