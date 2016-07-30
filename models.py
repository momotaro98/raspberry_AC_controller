import os
import csv

from flask.ext.wtf import Form
from wtforms import SelectField, SubmitField

from config import Config
import utils


class ACState:
    ACState_DICT = {"onoff": ("on", "off"),
                    "operating": ("cool", "warm", "dry", "auto", "blast"),
                    "wind": ("strong", "weak", "breeze", "auto")}

    def __init__(self, context):
        # TODO: 現状、インスタンス毎に設定コンテキストを指定しているので、
        # 管理用のプログラムを書き、参照するCSVファイルの指定を
        # さらに抽象的なレベルで行いたい

        self._logFileName = context["acStateLogCSVFilePath"]
        with open(context["acStateCSVFilePath"], 'r') as f:
            self._fileName = context["acStateCSVFilePath"]

            reader = csv.reader(f)
            for row in reader:
                last_row_list = row
            # row = next(reader)

            self._timestamp = utils.strToDatetime(last_row_list[0])
            self._onoff = last_row_list[1]
            self._operating = last_row_list[2]
            self._temperature = int(last_row_list[3])
            self._wind = last_row_list[4]

    def __repr__(self):
        return '<{0} {1} {2} {3} {4}>'.format(self.timestamp,
                                              self.onoff,
                                              self.operating,
                                              self.temperature,
                                              self.wind)

    @classmethod
    def _check_to_set(cls, val, mode):
        if val in cls.ACState_DICT[mode]:
            return True
        else:
            return False

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, x):
        pass

    @property
    def onoff(self):
        return self._onoff

    @onoff.setter
    def onoff(self, x):
        # セットして良い値であるかを確認
        if not self._check_to_set(x, "onoff"):
            return
        self._onoff = x
        # ファイル書き込み
        self._writeFiles()

    @property
    def operating(self):
        return self._operating

    @operating.setter
    def operating(self, x):
        # セットして良い値であるかを確認
        if not self._check_to_set(x, "operating"):
            return
        self._operating = x

        # onoffがoffのときはonにする
        if self.onoff == "off":
            self._onoff = "on"
        # ファイル書き込み
        self._writeFiles()

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, x):
        # セットして良い値であるかを確認
        # 設定温度制限
        if not 18 <= x <= 30:
            return
        self._temperature = x

        # onoffがoffのときはonにする
        if self.onoff == "off":
            self._onoff = "on"
        # ファイル書き込み
        self._writeFiles()

    @property
    def wind(self):
        return self._wind

    @wind.setter
    def wind(self, x):
        # セットして良い値であるかを確認
        if not self._check_to_set(x, "wind"):
            return
        self._wind = x

        # onoffがoffのときはonにする
        if self.onoff == "off":
            self._onoff = "on"
        # ファイル書き込み
        self._writeFiles()

    def _writeFiles(self):
        """
        method to write csv files
        """
        timestamp = utils.nowTimeToString()
        data_list = [timestamp,
                     self._onoff,
                     self._operating,
                     self._temperature,
                     self._wind]

        # write to 1 line csv file that has current A/C state
        with open(self._fileName, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(data_list)

        # write to logs csv file
        with open(self._logFileName, 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(data_list)

    def sendSignalToAC(self):
        signal = self._makeSignalName()
        if signal:  # 正しく信号名が作られたとき
            return InfraredSignal.sendSignal(signal)

    def _makeSignalName(self):
        if self.onoff == "off":
            return "off"  # TODO: 赤外線信号対応テーブルを作って保守性を高くする
        elif self.onoff == "on":
            op = self.operating
            if op == "dry" or op == "blast" or op == "auto":
                return op
            else:
                return "{0}{1}{2}".format(self.operating,
                                          self.temperature,
                                          self.wind)
        else:
            return

    class _ACStateConvertedJapanese:
        OperDictionary = {"cool": "冷房", "warm": "暖房",
                          "dry": "除湿", "auto": "自動",
                          "blast": "送風"}
        WindDictionary = {"strong": "強風", "weak": "弱風",
                          "breeze": "微風", "auto": "自動"}

        def __init__(self, state):
            self.onoff = state.onoff
            self.operating = state._ACStateConvertedJapanese.\
                OperDictionary[state.operating]
            self.temperature = state.temperature
            self.wind = state._ACStateConvertedJapanese.\
                WindDictionary[state.wind]

    def convertToJapanese(self):
        self.acConvertedJ = ACState._ACStateConvertedJapanese(self)
        return self.acConvertedJ


class ReserveState:
    ReserveState_DICT = {"onoff": ("on", "off", "offundo", "onundo")}

    def __init__(self, context):
        self._logFileName = context["reserveStateLogCSVFilePath"]
        with open(context["reserveStateCSVFilePath"], 'r') as f:
            self._fileName = context["reserveStateCSVFilePath"]

            reader = csv.reader(f)
            # TODO: この書き方だとUnboundLocalErrorが起きてしまうし、カッコ悪いので修正したい
            for row in reader:
                last_row_list = row

            self._timestamp = utils.strToDatetime(last_row_list[0])
            self._onoff = last_row_list[1]
            self._settime = int(last_row_list[2])  # 数値にする min

    def __repr__(self):
        return '<{0} {1} {2}>'.format(self.timestamp, self.onoff, self.settime)

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, x):
        pass

    @property
    def onoff(self):
        return self._onoff

    @onoff.setter
    def onoff(self, x):
        # セットして良い値であるかを確認
        if not self._check_to_set(x, "onoff"):
            return
        self._onoff = x

    @property
    def settime(self):
        return self._settime

    @settime.setter
    def settime(self, x):
        # セットして良い値であるかを確認
        # int型であるかを確認する
        if not isinstance(x, int):
            return
        self._settime = x

    def change_state(self, form):
        # アトリビュートを書き換え
        form.change_ReserveState(self)
        # ↑自身のアトリビュートの変更を他のクラスに任せる
        # ということをしてしまっているのだが、これはNGであろうか？

        # ファイル書き込み
        self._writeFiles()

    @classmethod
    def _check_to_set(cls, val, mode):
        if val in cls.ReserveState_DICT[mode]:
            return True
        else:
            return False

    def _writeFiles(self):
        """
        method to write csv files
        """
        timestamp = utils.nowTimeToString()
        data_list = [timestamp, self.onoff, self.settime]
        # TODO: ↑この部分だけがACStateのものと異なるのだが、
        # メソッドを抽象化するにはどうしたら良いか

        # write to 1 line csv file that has current A/C state
        with open(self._fileName, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(data_list)

        # write to logs csv file
        with open(self._logFileName, 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(data_list)

    def sendSignalToAC(self):
        # TODO: ACStateとまったく同じメソッドだからどうにかする
        signal = self._makeSignalName()
        if signal:  # 正しく信号名が作られたとき
            return InfraredSignal.sendSignal(signal)

    def _makeSignalName(self):
        if self.onoff == "onundo" or self.onoff == "offundo":
            return self.onoff
            # TODO: 赤外線信号対応テーブルを作って保守性を高くする
        elif self.onoff == "on" or self.onoff == "off":
            '''
            信号名
            例
            on02
            off03
            '''
            h = utils.minToHour(self.settime)
            return "{0}{1:0>2}".format(self.onoff, h)
        else:
            return

    def makeTimeoutText(self):
        text = ""
        tdelta = utils.nowDatetime() - self.timestamp
        processed_time_minute = utils.secToMin(tdelta.seconds)
        remaining_time = self.settime - processed_time_minute
        if remaining_time > 0:
            # タイマーが切れていないとき
            th, tm = utils.minToHourMin(remaining_time)
            if self.onoff == "off":
                text = "切予約済 {0}時間{1}分後".format(th, tm)
            if self.onoff == "on":
                text = "入予約済 {0}時間{1}分後".format(th, tm)
        return text


class ReserveForm(Form):
    def change_ReserveState(self, rstate):
        pass


class ReserveOffTimeForm(ReserveForm):
    off_hour = SelectField('時間', choices=[
        (str(i), str(i)) for i in range(1, 13)])  # 最大12時間
    submit = SubmitField('送信')

    def change_ReserveState(self, rstate):
        # onoff変更
        rstate.onoff = "off"

        # 設定時間をセットする
        rstate.settime = utils.hourToMin(self.off_hour.data)


class ReserveOnTimeForm(ReserveForm):
    on_hour = SelectField('時間', choices=[
        (str(i), str(i)) for i in range(1, 13)])  # 最大12時間
    submit = SubmitField('送信')

    def change_ReserveState(self, rstate):
        # onoff変更
        rstate.onoff = "on"

        # 設定時間をセットする
        rstate.settime = utils.hourToMin(self.on_hour.data)


class UndoReservationForm(ReserveForm):
    submit = SubmitField('送信')

    def change_ReserveState(self, rstate):
        # onoff変更
        if rstate.onoff == "off":
            rstate.onoff = "offundo"
        elif rstate.onoff == "on":
            rstate.onoff = "onundo"

        # 設定時間をセットする
        rstate.settime = 0  # UNDOの場合は0


class InfraredSignal:
    controller = Config.CONTROLLER_NAME

    @classmethod
    def sendSignal(cls, signal):
        # 赤外線を送信する
        if int(os.system('irsend SEND_ONCE {0} {1}'.format(cls.controller,
                                                           signal))):
            # irsendが正しく実行されなかったとき
            return False  # TODO: irsendコマンドのエラーの場合どうするか

        # 正常に送信できたとき
        return True
