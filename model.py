import csv
from datetime import datetime

from config import Config

class ACState:
    def __init__(self):
        """
        CSVファイルから最後の行のデータを読み込む
        """
        with open("acstate.csv", 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                last_row_list = row

            self._onoff = last_row_list[1]
            self._operating = last_row_list[2]
            self._temperature = last_row_list[3]
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
        self._operating = x
        # ファイル書き込み
        self._addLineToFile()

    @property
    def operating(self):
        return self._operating

    @operating.setter
    def operating(self, x):
        self._operating = x
        # ファイル書き込み
        self._addLineToFile()

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, x):
        self._operating = x
        # ファイル書き込み
        self._addLineToFile()

    @property
    def wind(self):
        return self._wind

    @wind.setter
    def wind(self, x):
        self._wind = x
        # ファイル書き込み
        self._addLineToFile()

    @property
    def wind(self):
        return self._wind

    @wind.setter
    def wind(self, x):
        self._wind = x
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
        with open("acstate.csv", 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(data_list)


class InfraredSignal:
    def __init__(self):
        pass

    def sendSignal(self):
        """
        赤外線を送信する
        os.system('irsend SEND_ONCE {0} {1}'.format(Config.CONTROLLER_NAME, Config.SIGNALS['stop']))
        """
        pass
