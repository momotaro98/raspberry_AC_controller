import os
import csv
from datetime import datetime

from flask.ext.wtf import Form
from wtforms import SelectField, SubmitField

from config import Config

# TODO: ReserveStateクラスを作っていくならば抽象クラスを設計する

class ACState:
    ACState_DICT = {"onoff": ("on", "off"),
                    "operating": ("cool", "warm", "dry", "auto"),
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

            self._onoff = last_row_list[1]
            self._operating = last_row_list[2]
            self._temperature = int(last_row_list[3])
            self._wind = last_row_list[4]

    def __repr__(self):
        return '<{0} {1} {2} {3}>'.format(self.onoff,
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
        timestamp = datetime.now()
        data_list = [str(timestamp),
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
        return InfraredSignal.sendSignal(onoff=self.onoff,
                                  operating=self.operating,
                                  temperature=self.temperature,
                                  wind=self.wind)


    class _ACStateConvertedJapanese:
        OperDictionary = {"cool":"冷房", "warm":"暖房", "dry":"除湿", "auto":"自動"}
        WindDictionary = {"strong":"強風", "weak":"弱風", "breeze":"微風", "auto":"自動"}
        def __init__(self, state):
            self.onoff = state.onoff
            self.operating = state._ACStateConvertedJapanese.OperDictionary[state.operating]
            self.temperature = state.temperature
            self.wind = state._ACStateConvertedJapanese.WindDictionary[state.wind]

    def convertToJapanese(self):
        self.acConvertedJ = ACState._ACStateConvertedJapanese(self)
        return self.acConvertedJ


class ReserveState:
    ReserveState_DICT = {"onoff": ("on", "off", "undo"),}

    def __init__(self, context):
        self._logFileName = context["reserveStateLogCSVFilePath"]
        with open(context["reserveStateCSVFilePath"], 'r') as f:
            self._fileName = context["reserveStateCSVFilePath"]

            reader = csv.reader(f)
            # TODO: この書き方だとUnboundLocalErrorが起きてしまうし、カッコ悪いので修正したい
            for row in reader:
                last_row_list = row

            self._timestamp = last_row_list[0] # TODO:use datetime library
            self._onoff = last_row_list[1]
            self._settime = last_row_list[2]

    def __repr__(self):
        return '<{0} {1} {2}>'.format(self.timestamp, self.onoff, self.settime)

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, x):
        self._timestamp = datetime.now()

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
        # セットして良い値であるかを確認 # TODO: ←を書く
        '''
        if not self._check_to_set(x, "settime"):
            return
        '''
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
        timestamp = datetime.now()
        data_list = [str(timestamp),
                        self.onoff,
                        self.settime]
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
        return InfraredSignal.sendSignal(onoff=self.onoff,
                                  operating=self.operating,
                                  temperature=self.temperature,
                                  wind=self.wind)

class InfraredSignal:
    controller = Config.CONTROLLER_NAME

    @classmethod
    def sendSignal(cls, **states):
        # statesから1つの信号NAMEを生成
        if states["onoff"] == "off":
            signal = "off"
        elif states["onoff"] == "on":
            signal = "{0}{1}{2}".format(states["operating"],
                                        states["temperature"],
                                        states["wind"])
        else:
            return

        # 赤外線を送信する
        if int(os.system('irsend SEND_ONCE {0} {1}'.format(cls.controller, signal))):
        # 異常終了したとき
            return "error"

        # 正常に送信できたとき
        return


class ReserveForm(Form):
    def change_ReserveState(self, acstate):
        pass

class ReserveOffTimeForm(ReserveForm):
    off_hour = SelectField('時間', choices=[(str(i), str(i)) for i in range(0, 13)]) # 最大12時間
    off_minute = SelectField('分', choices=[(str(0), str(0)), (str(30), str(30))])
    submit = SubmitField('送信')

    def change_ReserveState(self, acstate):
        # タイムスタンプを押す
        # TODO: setterの方でもdatetime.now()しているので二度手間になっている
        acstate.timestamp = datetime.now()

        # onoff変更
        acstate.onoff = "off"

        # 設定時間をセットする
        acstate.settime = "{0}:{1}".format(self.off_hour.data, self.off_minute.data)

class ReserveOnTimeForm(ReserveForm):
    on_hour = SelectField('時間', choices=[(str(i), str(i)) for i in range(0, 13)]) # 最大12時間
    on_minute = SelectField('分', choices=[(str(0), str(0)), (str(30), str(30))])
    submit = SubmitField('送信')

    def change_ReserveState(self, acstate):
        # タイムスタンプを押す
        # TODO: setterの方でもdatetime.now()しているので二度手間になっている
        acstate.timestamp = datetime.now()

        # onoff変更
        acstate.onoff = "on"

        # 設定時間をセットする
        acstate.settime = "{0}:{1}".format(self.on_hour.data, self.on_minute.data)

class UndoReservationForm(ReserveForm):
    submit = SubmitField('送信')

    def change_ReserveState(self, acstate):
        # タイムスタンプを押す
        # TODO: setterの方でもdatetime.now()しているので二度手間になっている
        acstate.timestamp = datetime.now()

        # onoff変更
        acstate.onoff = "undo"

        # 設定時間をセットする
        acstate.settime = "0:0"
