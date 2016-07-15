# encoding: utf-8

import os
import unittest

from models import ACState
from config import Config


class ACStateTest(unittest.TestCase):
    def setUp(self):
        with open(Config.test_context["acStateCSVFilePath"], "w") as f:
            f.write("2016-04-01 13:24:00,off,cool,25,breeze")

        with open(Config.test_context["acStateLogCSVFilePath"], "w") as f:
            f.write("2016-04-01 13:24:00,off,cool,25,breeze")

        self.acstate = ACState(Config.test_context)

    def tearDown(self):
        os.remove(Config.test_context["acStateCSVFilePath"])
        os.remove(Config.test_context["acStateLogCSVFilePath"])

    def test_initiate_and_getter(self):
        # test ACState initiation
        self.assertEqual(self.acstate.__repr__(),
                         '<2016-04-01 13:24:00 off cool 25 breeze>')

    def test_makeSignalName(self):
        signal = self.acstate._makeSignalName()
        self.assertEqual(signal, 'off')

        self.acstate.onoff = "on"
        signal = self.acstate._makeSignalName()
        self.assertEqual(signal, 'cool25breeze')

    def test_states_setter_restrict(self):
        self.acstate.onoff = "on"
        self.assertEqual(self.acstate.onoff, 'on')

        # setter制限が働いているか確認
        self.acstate.onoff = "ok"
        self.assertEqual(self.acstate.onoff, 'on')

        self.acstate.operating = "warm"
        self.assertEqual(self.acstate.operating, 'warm')

        # setter制限が働いているか確認
        self.acstate.operating = "supercool"
        self.assertEqual(self.acstate.operating, 'warm')

        self.acstate.temperature = 30
        self.assertEqual(self.acstate.temperature, 30)

        # setter制限が働いているか確認
        self.acstate.temperature += 1
        self.assertEqual(self.acstate.temperature, 30)

        self.acstate.temperature = 18
        self.assertEqual(self.acstate.temperature, 18)

        # setter制限が働いているか確認
        self.acstate.temperature -= 1
        self.assertEqual(self.acstate.temperature, 18)

        self.acstate.wind = "strong"
        self.assertEqual(self.acstate.wind, "strong")

        # setter制限が働いているか確認
        self.acstate.wind = "week"
        self.assertEqual(self.acstate.wind, "strong")

if __name__ == "__main__":
    unittest.main()
