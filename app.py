import os

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from config import Config


def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    return app

app = create_app()

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
    app.run(debug=True, host="0.0.0.0", port=5050)
