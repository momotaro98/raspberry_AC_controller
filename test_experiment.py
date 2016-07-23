import os
import unittest

from config import Config
from experiment import LogFileForExperiment


# Test LogFileForExperiment class
class LogFileForExperimentTest(unittest.TestCase):
    def setUp(self):
        from models import ACState

        with open(Config.test_context["acStateCSVFilePath"], "w") as f:
            f.write("2016-04-01 13:24:00,off,cool,25,breeze")

        with open(Config.test_context["experimentLogCSVFilePath"], "w") as f:
            clist = [k for k in LogFileForExperiment.DATA_COLUMN_DICT.keys()]
            f.write(",".join(clist))

        self.acstate = ACState(Config.test_context)
        self.lffe = LogFileForExperiment(context=Config.test_context,
                                         acstate=self.acstate,
                                         ipaddr="192.168.1.5")

    def tearDown(self):
        os.remove(Config.test_context["acStateCSVFilePath"])
        os.remove(Config.test_context["experimentLogCSVFilePath"])

    def test_initiate(self):
        self.assertEqual(self.lffe.log_data_dict["02_ac_onoff"], "off")
        self.assertEqual(self.lffe.log_data_dict["03_ac_operating"], "cool")
        self.assertEqual(self.lffe.log_data_dict["04_ac_temperature"], 25)
        self.assertEqual(self.lffe.log_data_dict["05_ac_wind"], "breeze")
