import unittest

# test
from .colors import red, green


class TestColors(unittest.TestCase):
    def test_red(self):
        # given
        val = 'value'

        # when
        output = red(val)

        # then
        self.assertEqual(output, f"\x1b[31m{val}\x1b[0m")

    def test_green(self):
        # given
        val = 'value'

        # when
        output = green(val)

        # then
        self.assertEqual(output, f"\x1b[32m{val}\x1b[0m")
