#encoding: utf-8

import os
import unittest

from model import ACState
from config import Config

class ACStateTest(unittest.TestCase):
    def setUp(self):
        with open(Config.test_context["csvFilePath"], "w") as f:
            f.write("2016-04-01 13:24:00,off,cool,25,breeze")

        with open(Config.test_context["LogCsvFilePath"], "w") as f:
            f.write("2016-04-01 13:24:00,off,cool,25,breeze")

        self.state = ACState(Config.test_context)

    def tearDown(self):
        os.remove(Config.test_context["csvFilePath"])
        os.remove(Config.test_context["LogCsvFilePath"])

    def test_initiate_and_getter(self):
        # test ACState initiation
        self.assertEqual(self.state.__repr__(), '<off cool 25 breeze>')

    def test_states_setter_restrict(self):
        self.state.onoff = "on"
        self.assertEqual(self.state.onoff, 'on')

        # setter制限が働いているか確認
        self.state.onoff = "ok"
        self.assertEqual(self.state.onoff, 'on')

        self.state.operating = "warm"
        self.assertEqual(self.state.operating, 'warm')

        # setter制限が働いているか確認
        self.state.operating = "supercool"
        self.assertEqual(self.state.operating, 'warm')

        self.state.temperature = 30
        self.assertEqual(self.state.temperature, 30)

        # setter制限が働いているか確認
        self.state.temperature += 1
        self.assertEqual(self.state.temperature, 30)

        self.state.temperature = 18
        self.assertEqual(self.state.temperature, 18)

        # setter制限が働いているか確認
        self.state.temperature -= 1
        self.assertEqual(self.state.temperature, 18)

        self.state.wind = "strong"
        self.assertEqual(self.state.wind, "strong")

        # setter制限が働いているか確認
        self.state.wind = "week"
        self.assertEqual(self.state.wind, "strong")

if __name__ == "__main__":
    unittest.main()
