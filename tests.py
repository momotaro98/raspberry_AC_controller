#encoding: utf-8

import unittest

from model import ACState
from config import Config

class ACStateTest(unittest.TestCase):
    def setUp(self):
        self.state = ACState(Config.test_context)
        # TODO: テスト用のCSVファイルを作成する

    def tearDonw(self):
        # TODO: setUpで作成したCSVファイルの削除
        pass

    def test_initiate_and_getter(self):
        """
        test ACState initiation
        """
        self.assertEqual(self.state.__repr__(), '<off warm 25 breeze>')

    def test_states_setter(self):
        # TODO: write this test
        pass

if __name__ == "__main__":
    unittest.main()
