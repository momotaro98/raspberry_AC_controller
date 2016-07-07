import os

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap

from config import Config
from model import ACState


def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    return app

app = create_app()

@app.route('/')
def index():
    state = ACState() # ステータスデータを読み込む
    return render_template('index.html', state=state)

@app.route('/on')
def turnOn():
    '''
    # 読み込み
    # 受け取るデータ型は
    state = state.read()

    # 赤外線送信
    os.system('irsend SEND_ONCE {0} {1}'.format(Config.CONTROLLER_NAME, Config.SIGNALS['stop']))

    # 状態ファイル書き換え or 追加
    state.write()

    '''
    state = ACState() # ステータスデータを読み込む
    return render_template('index.html', state=state)

@app.route('/off')
def turnOff():
    '''
    # 赤外線送信
    os.system('irsend SEND_ONCE {0} {1}'.format(Config.CONTROLLER_NAME, Config.SIGNALS['stop']))

    # 状態ファイル書き換え or 追加
    state.write()
    '''
    state = ACState() # ステータスデータを読み込む
    return render_template('index.html', state=state)

@app.route('/operating/<operatingMode>')
def modeOperating():
    '''
    # 状態ファイル書き換え or 追加
    state.write()
    # 読み込み
    state = state.read()

    # 赤外線送信
    os.system('irsend SEND_ONCE {0} {1}'.format(Config.CONTROLLER_NAME, Config.SIGNALS['stop']))

    '''
    state = ACState() # ステータスデータを読み込む
    return render_template('index.html', state=state)

@app.route('/temperature/<temperatureMode>')
def modeTemperature():
    '''
    # 状態ファイル書き換え or 追加
    state.write()
    # 読み込み
    state = state.read()

    # 赤外線送信
    os.system('irsend SEND_ONCE {0} {1}'.format(Config.CONTROLLER_NAME, Config.SIGNALS['stop']))

    '''
    state = ACState() # ステータスデータを読み込む
    return render_template('index.html', state=state)

@app.route('/wind/<windMode>')
def modeWind():
    '''
    # 状態ファイル書き換え or 追加
    state.write()
    # 読み込み
    state = state.read()

    # 赤外線送信
    os.system('irsend SEND_ONCE {0} {1}'.format(Config.CONTROLLER_NAME, Config.SIGNALS['stop']))
    '''
    state = ACState() # ステータスデータを読み込む
    return render_template('index.html', state=state)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5055)
