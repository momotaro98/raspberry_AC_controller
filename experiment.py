# condig: utf-8

"""
実験・研究のためのモジュールファイル
"""

import csv

from config import Config
import utils


class LogFileForExperiment:
    """ 実験用のログファイルのためのクラス"""
    DATA_COLUMN_DICT = {"01_timestamp": "",
                        "02_ac_onoff": "",
                        "03_ac_operating": "",
                        "04_ac_temperature": "",
                        "05_ac_wind": "",
                        "06_room_temperature": "",
                        "07_room_humidity": "",
                        "08_room_pressure": "",
                        "09_ope_ip_addr": ""}

    def __init__(self, context, acstate, ipaddr):
        self.log_data_dict = self.DATA_COLUMN_DICT
        self._csvfile = context["experimentLogCSVFilePath"]

        # Get timestamp
        self.log_data_dict["01_timestamp"] = utils.nowTimeToString()

        # Get ACState
        try:
            self.log_data_dict["02_ac_onoff"] = acstate.onoff
            self.log_data_dict["03_ac_operating"] = acstate.operating
            self.log_data_dict["04_ac_temperature"] = acstate.temperature
            self.log_data_dict["05_ac_wind"] = acstate.wind
        except:
            pass

        # Get environmental data if we have sensors
        try:
            ed = EnvironData()
            self.log_data_dict["06_room_temperature"] = ed.get_temperature()
            self.log_data_dict["07_room_humidity"] = ed.get_humidity()
            self.log_data_dict["08_room_pressure"] = ed.get_pressure()
        except:
            pass

        # Get Visitor IP Address
        self.log_data_dict["09_ope_ip_addr"] = ipaddr

    def write_log_file(self):
        """ method to write csv file """
        # Make LogDataList
        log_data_list = utils.dictToListSortedByValue(self.log_data_dict)
        # write to logs csv file
        with open(self._csvfile, 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(log_data_list)


class EnvironData:
    cmd = Config.ENV_DATA_CMD
    '''
    このコマンドにより
    """
    25.7
    54.7
    1012.5
    """
    といった3行の標準出力が得られなけらばならない
    '''

    def __init__(self):
        env_list = self._get_envdata_list()
        for ind, val in enumerate(env_list):
            if ind == 0:
                self._temperature = val  # 1行目は気温(℃)
            elif ind == 1:
                self._humidity = val  # 2行目は湿度(%)
            elif ind == 2:
                self._pressure = val  # 3行目は気圧(hPa)

    def _get_envdata_list(self):
        from subprocess import Popen, PIPE

        p = Popen(self.cmd.split(' '), stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        out, err = out.decode('utf-8'), err.decode('utf-8')  # for Python3

        return [s for s in out.split('\n') if s]

    def get_temperature(self):
        return self._temperature

    def get_humidity(self):
        return self._humidity

    def get_pressure(self):
        return self._pressure


if __name__ == "__main__":
    # Test EnvironData class
    # This test run only if on Raspberry Pi with environ sensor

    env_data = EnvironData()
    room_temperature = env_data.get_temperature()
    room_humidity = env_data.get_humidity()
    room_pressure = env_data.get_pressure()
