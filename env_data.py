# encoding: utf-8

from config import Config


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
    env_data = EnvironData()
    room_temperature = env_data.get_temperature()
    room_humidity = env_data.get_humidity()
    room_pressure = env_data.get_pressure()
