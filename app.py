import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap

from config import Config
from model import ACState


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY') or 'hard to guess string'
    Bootstrap(app)

    return app

app = create_app()

@app.route('/')
def index():
    state = ACState(Config.context) # ステータスデータを読み込む

    # 日本語変換
    jstate = state.convertToJapanese()

    return render_template('index.html', state=jstate)

@app.route('/on')
def turnOn():
    # ACStateインスタンス読み込み
    state = ACState(Config.context)

    # ステート変更 ログファイル追加
    state.onoff = "on"

    # stateを元に赤外線送信
    if state.sendSignalToAC():
        flash('信号を送信できませんでした')

    # 日本語変換
    jstate = state.convertToJapanese()

    return render_template('index.html', state=jstate)

@app.route('/off')
def turnOff():
    # ACStateインスタンス読み込み
    state = ACState(Config.context)

    # ステート変更 ログファイル追加
    state.onoff = "off"

    # stateを元に赤外線送信
    if state.sendSignalToAC():
        flash('信号を送信できませんでした')

    # 日本語変換
    jstate = state.convertToJapanese()

    return render_template('index.html', state=jstate)

@app.route('/operating/<operatingMode>')
def modeOperating(operatingMode):
    # ACStateインスタンス読み込み
    state = ACState(Config.context)

    # ステート変更 ログファイル追加
    state.operating = operatingMode

    # stateを元に赤外線送信
    if state.sendSignalToAC():
        flash('信号を送信できませんでした')

    # 日本語変換
    jstate = state.convertToJapanese()

    return render_template('index.html', state=jstate)

@app.route('/temperature/<temperatureMode>')
def modeTemperature(temperatureMode):
    # ACStateインスタンス読み込み
    state = ACState(Config.context)

    # ステート変更 ログファイル追加
    if temperatureMode == "up" and state.temperature >= 30:
        flash('最大設定温度です')
    elif temperatureMode == "up":
        state.temperature += 1

    if temperatureMode == "down" and state.temperature <= 18:
        flash('最低設定温度です')
    elif temperatureMode == "down":
        state.temperature -= 1

    # stateを元に赤外線送信
    if state.sendSignalToAC():
        flash('信号を送信できませんでした')

    # 日本語変換
    jstate = state.convertToJapanese()

    return render_template('index.html', state=jstate)

@app.route('/wind/<windMode>')
def modeWind(windMode):
    # ACStateインスタンス読み込み
    state = ACState(Config.context)

    # ステート変更 ログファイル追加
    state.wind = windMode

    # stateを元に赤外線送信
    if state.sendSignalToAC():
        flash('信号を送信できませんでした')

    # 日本語変換
    jstate = state.convertToJapanese()

    return render_template('index.html', state=jstate)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5055)
