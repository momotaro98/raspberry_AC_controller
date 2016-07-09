import os
import csv
from datetime import datetime

from config import Config

class ACState:
    def __init__(self, context):
        """
        CSVファイルから最後の行のデータを読み込む
        """
        with open(context["csvFilePath"], 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                last_row_list = row

            self._fileName = context["csvFilePath"]
            self._onoff = last_row_list[1]
            self._operating = last_row_list[2]
            self._temperature = int(last_row_list[3])
            self._wind = last_row_list[4]

    def __repr__(self):
        return '<{0} {1} {2} {3}>'.format(self.onoff,
                                        self.operating,
                                        self.temperature,
                                        self.wind)

    @property
    def onoff(self):
        return self._onoff

    @onoff.setter
    def onoff(self, x):
        self._onoff = x
        # ファイル書き込み
        self._addLineToFile()

    @property
    def operating(self):
        return self._operating

    @operating.setter
    def operating(self, x):
        self._operating = x

        if self.onoff == "off":
            self._onoff = "on"
        # ファイル書き込み
        self._addLineToFile()

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, x):
        if 18 <= x <= 30: # 設定温度制限
            self._temperature = x
        else:
            return

        if self.onoff == "off":
            self._onoff = "on"
        # ファイル書き込み
        self._addLineToFile()

    @property
    def wind(self):
        return self._wind

    @wind.setter
    def wind(self, x):
        self._wind = x

        if self.onoff == "off":
            self._onoff = "on"
        # ファイル書き込み
        self._addLineToFile()

    def _addLineToFile(self):
        """
        CSVファイルに書き込む用のメソッド
        """
        timestamp = datetime.now()
        data_list = [str(timestamp),
                        self._onoff,
                        self._operating,
                        self._temperature,
                        self._wind]
        with open(self._fileName, 'a') as f:
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
