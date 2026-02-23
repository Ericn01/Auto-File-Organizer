import unittest

import utils


class TestMain(unittest.TestCase):
    def test_coerce_value(self):
        self.assertEqual(utils.coerce_value("3", "int"), 3)
        self.assertEqual(utils.coerce_value("3.5", "float"), 3.5)
        self.assertEqual(utils.coerce_value("true", "bool"), True)
        self.assertEqual(utils.coerce_value("FALSE", "bool"), False)
        self.assertEqual(utils.coerce_value("a,b , c", "list"), ["a", "b", "c"])
        self.assertEqual(utils.coerce_value("", "list"), [])
