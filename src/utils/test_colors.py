import unittest

# test
import src.utils.colors as colors


class TestColors(unittest.TestCase):
    def test_red(self):
        # given
        val = 'value'

        # when
        output = colors.red(val)

        # then
        self.assertEqual(output, f"\x1b[31m${val}\x1b[0m")

    def test_green(self):
        # given
        val = 'value'

        # when
        output = colors.green(val)

        # then
        self.assertEqual(output, f"\x1b[32m${val}\x1b[0m")
