import os
from flask import Flask, render_template, redirect, url_for
from flask.ext.script import Manager

app = Flask(__name__)

manager = Manager(app)

@app.route('/')
def index():
    state = 'HOME Now'
    return render_template('index.html', state=state)

@app.route('/stop')
def do_stopping():
    os.system('irsend SEND_ONCE Panasonic stop')
    state = 'Now Stopping'
    return render_template('index.html', state=state)

@app.route('/warm')
def do_warming():
    os.system('irsend SEND_ONCE Panasonic warm')
    state = 'Now Warming'
    return render_template('index.html', state=state)

@app.route('/cool')
def do_cooling():
    os.system('irsend SEND_ONCE Panasonic cold')
    state = 'Now Cooling'
    return render_template('index.html', state=state)

if __name__ == '__main__':
    manager.run()
