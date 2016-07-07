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
    state = ACState(Config.context) # ステータスデータを読み込む
    return render_template('index.html', state=state)

@app.route('/on')
def turnOn():
    # ACStateインスタンス読み込み
    state = ACState(Config.context)

    # ステート変更 ログファイル追加
    state.onoff = "on"

    # stateを元に赤外線送信
    state.sendSignalToAC()

    return render_template('index.html', state=state)

@app.route('/off')
def turnOff():
    # ACStateインスタンス読み込み
    state = ACState(Config.context)

    # ステート変更 ログファイル追加
    state.onoff = "off"

    # stateを元に赤外線送信
    state.sendSignalToAC()

    return render_template('index.html', state=state)

@app.route('/operating/<operatingMode>')
def modeOperating(operatingMode):
    # ACStateインスタンス読み込み
    state = ACState(Config.context)

    # ステート変更 ログファイル追加
    state.operating = operatingMode

    # stateを元に赤外線送信
    state.sendSignalToAC()

    return render_template('index.html', state=state)

@app.route('/temperature/<temperatureMode>')
def modeTemperature(temperatureMode):
    # ACStateインスタンス読み込み
    state = ACState(Config.context)

    # ステート変更 ログファイル追加
    if temperatureMode == "up":
        state.temperature += 1
    if temperatureMode == "down":
        state.temperature -= 1

    # stateを元に赤外線送信
    state.sendSignalToAC()

    return render_template('index.html', state=state)

@app.route('/wind/<windMode>')
def modeWind(windMode):
    # ACStateインスタンス読み込み
    state = ACState(Config.context)

    # ステート変更 ログファイル追加
    state.wind = windMode

    # stateを元に赤外線送信
    state.sendSignalToAC()

    return render_template('index.html', state=state)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5055)
