import unittest

import main


class TestMain(unittest.TestCase):
    def test_coerce_value(self):
        self.assertEqual(main.coerce_value("3", "int"), 3)
        self.assertEqual(main.coerce_value("3.5", "float"), 3.5)
        self.assertEqual(main.coerce_value("true", "bool"), True)
        self.assertEqual(main.coerce_value("FALSE", "bool"), False)
        self.assertEqual(main.coerce_value("a,b , c", "list"), ["a", "b", "c"])
        self.assertEqual(main.coerce_value("", "list"), [])

