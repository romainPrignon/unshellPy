from typing import Callable
from type import Options

import unittest

# test
from src.unshell import Unshell


class TestUnshell(unittest.TestCase):
    def test_unshell_should_return_function(self):
        # given
        opt = Options(env={})

        # when
        output = Unshell(opt)

        # then
        self.assertTrue(isinstance(output, Callable))

    def test_unshell_should_return_default_options(self):
        self.assertTrue(isinstance(Unshell(), Callable))

    def test_unshell_should_raise_if_script_not_generator(self):
        # given
        def script():
            return "echo OK"

        # then
        with self.assertRaises(TypeError):
            Unshell()(script)

    def test_unshell_should_process_command(self):
        # given
        def script():
            yield "echo OK"

        # when
        Unshell()(script)

        # then
