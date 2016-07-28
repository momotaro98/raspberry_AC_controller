import os

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap

from config import Config
from models import (ACState, ReserveState, ReserveOffTimeForm,
                    ReserveOnTimeForm, UndoReservationForm)
from experiment import LogFileForExperiment


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY') or 'hard to guess string'
    Bootstrap(app)

    return app

app = create_app()


@app.route('/')
def index():
    state = ACState(Config.context)  # ステータスデータを読み込む

    # 日本語変換
    jstate = state.convertToJapanese()

    return render_template('index.html', state=state, jstate=jstate)


@app.route('/on')
def turnOn():
    # ACStateインスタンス読み込み
    state = ACState(Config.context)

    # ステート変更 ログファイル追加
    state.onoff = "on"

    # stateを元に赤外線送信
    if not state.sendSignalToAC():
        flash('信号を送信できませんでした')

    # 日本語変換
    jstate = state.convertToJapanese()

    # 実験用ログ書き込み
    lffe = LogFileForExperiment(context=Config.context,
                                acstate=state,
                                ipaddr=request.remote_addr)
    lffe.write_log_file()

    return render_template('index.html', state=state, jstate=jstate)


@app.route('/off')
def turnOff():
    # ACStateインスタンス読み込み
    state = ACState(Config.context)

    # ステート変更 ログファイル追加
    state.onoff = "off"

    # stateを元に赤外線送信
    if not state.sendSignalToAC():
        flash('信号を送信できませんでした')

    # 日本語変換
    jstate = state.convertToJapanese()

    # 実験用ログ書き込み
    lffe = LogFileForExperiment(context=Config.context,
                                acstate=state,
                                ipaddr=request.remote_addr)
    lffe.write_log_file()

    return render_template('index.html', state=state, jstate=jstate)


@app.route('/operating/<operatingMode>')
def modeOperating(operatingMode):
    # ACStateインスタンス読み込み
    state = ACState(Config.context)

    # ステート変更 ログファイル追加
    state.operating = operatingMode

    # stateを元に赤外線送信
    if not state.sendSignalToAC():
        flash('信号を送信できませんでした')

    # 日本語変換
    jstate = state.convertToJapanese()

    # 実験用ログ書き込み
    lffe = LogFileForExperiment(context=Config.context,
                                acstate=state,
                                ipaddr=request.remote_addr)
    lffe.write_log_file()

    return render_template('index.html', state=state, jstate=jstate)


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
    if not state.sendSignalToAC():
        flash('信号を送信できませんでした')

    # 日本語変換
    jstate = state.convertToJapanese()

    # 実験用ログ書き込み
    lffe = LogFileForExperiment(context=Config.context,
                                acstate=state,
                                ipaddr=request.remote_addr)
    lffe.write_log_file()

    return render_template('index.html', state=state, jstate=jstate)


@app.route('/wind/<windMode>')
def modeWind(windMode):
    # ACStateインスタンス読み込み
    state = ACState(Config.context)

    # ステート変更 ログファイル追加
    state.wind = windMode

    # stateを元に赤外線送信
    if not state.sendSignalToAC():
        flash('信号を送信できませんでした')

    # 日本語変換
    jstate = state.convertToJapanese()

    # 実験用ログ書き込み
    lffe = LogFileForExperiment(context=Config.context,
                                acstate=state,
                                ipaddr=request.remote_addr)
    lffe.write_log_file()

    return render_template('index.html', state=state, jstate=jstate)


@app.route('/reservation', methods=['POST', 'GET'])
def reserve():
    state = ReserveState(Config.context)

    offForm = ReserveOffTimeForm()
    onForm = ReserveOnTimeForm()
    undoForm = UndoReservationForm()

    if offForm.validate_on_submit():
        # state書き換え
        state.change_state(offForm)

        # 赤外線送信
        # stateを元に赤外線送信
        if not state.sendSignalToAC():
            flash('信号を送信できませんでした')
        else:
            offtext = "{h}時間{m}分後の切予約をしました".\
                    format(h=offForm.off_hour.data, m=offForm.off_minute.data)
            flash(offtext)
        return redirect(url_for('reserve'))

    if onForm.validate_on_submit():
        # state書き換え
        state.change_state(onForm)

        # 赤外線送信
        # stateを元に赤外線送信
        if not state.sendSignalToAC():
            flash('信号を送信できませんでした')
        else:
            ontext = "{h}時間{m}分後の入予約をしました".\
                    format(h=onForm.on_hour.data, m=onForm.on_minute.data)
            flash(ontext)
        return redirect(url_for('reserve'))

    if undoForm.validate_on_submit():
        # state書き換え
        # 取り消し処理
        state.change_state(undoForm)

        # 赤外線送信
        # stateを元に赤外線送信
        if not state.sendSignalToAC():
            flash('信号を送信できませんでした')
        else:
            undotext = "予約を取り消しました"
            flash(undotext)
        return redirect(url_for('reserve'))

    timeout_text = state.makeTimeoutText()

    return render_template('reservation.html',
                           timeout_text=timeout_text,
                           offForm=offForm,
                           onForm=onForm,
                           undoForm=undoForm)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5055)
