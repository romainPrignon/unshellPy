from typing import Callable
from type import Options

import unittest
from unittest.mock import patch, call
from subprocess import CompletedProcess

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

    @patch('builtins.print')
    @patch('subprocess.run')
    def test_unshell_should_process_command(self, run_mock, print_mock):
        # given
        opt = Options(env={})
        cmd: str = "echo"
        cmd_args: str = "OK"
        res: str = "result of echo OK"

        def script():
            yield f"{cmd} {cmd_args}"

        # mock
        run_mock.return_value = CompletedProcess(
            args=[cmd_args],
            returncode=0,
            stdout=res
        )

        # when
        Unshell(opt)(script)

        # then
        run_mock.assert_called_once_with([cmd, cmd_args], capture_output=True)
        self.assertEqual(print_mock.mock_calls, [
            call(f"• {cmd} {cmd_args}"),
            call(f"➜ {res}"),
        ])

    @patch('builtins.print')
    @patch('subprocess.run')
    def test_unshell_should_not_process_unvalid_command(
        self, run_mock, print_mock
    ):
        # given
        opt = Options(env={})

        def script():
            yield ""

        # when
        Unshell(opt)(script)

        # then
        run_mock.assert_not_called()
        print_mock.assert_not_called()

    @patch('builtins.print')
    @patch('subprocess.run')
    def test_unshell_should_handle_command_throwing_error(
        self, run_mock, print_mock
    ):
        # given
        opt = Options(env={})
        cmd: str = "echo"
        cmd_args: str = "OK"
        cmd_res: str = "cmd error"

        def script():
            yield f"{cmd} {cmd_args}"

        # mock
        run_mock.return_value = CompletedProcess(
            args=[cmd, cmd_args],
            returncode=1,
            stderr=cmd_res
        )

        # when
        try:
            Unshell(opt)(script)
        except Exception as err:
            # then
            err_msg = f"{cmd} {cmd_args}: {cmd_res}"
            self.assertEqual(str(err), err_msg)
            self.assertEqual(print_mock.mock_calls, [
                call(f"• {cmd} {cmd_args}"),
                call(f"{err_msg}"),
            ])

    @patch('builtins.print')
    @patch('subprocess.run')
    def test_unshell_should_process_several_command(
        self,
        run_mock,
        print_mock
    ):
        # given
        opt = Options(env={})
        cmd: str = "echo"
        cmd_args: str = "OK"
        res: str = "result of echo OK"

        def script():
            yield f"{cmd} {cmd_args}"
            yield f"{cmd} {cmd_args}"

        # mock
        run_mock.return_value = CompletedProcess(
            args=[cmd_args],
            returncode=0,
            stdout=res
        )

        # when
        Unshell(opt)(script)

        # then
        self.assertEqual(run_mock.mock_calls, [
            call([cmd, cmd_args], capture_output=True),
            call([cmd, cmd_args], capture_output=True)
        ])
        self.assertEqual(print_mock.mock_calls, [
            call(f"• {cmd} {cmd_args}"),
            call(f"➜ {res}"),
            call(f"• {cmd} {cmd_args}"),
            call(f"➜ {res}"),
        ])

    @patch('builtins.print')
    @patch('subprocess.run')
    def test_unshell_should_process_yield_and_return_command(
        self,
        run_mock,
        print_mock
    ):
        # given
        opt = Options(env={})
        cmd: str = "echo"
        cmd_args: str = "OK"
        res: str = "result of echo OK"

        def script():
            yield f"{cmd} {cmd_args}"
            return f"{cmd} {cmd_args}"

        # mock
        run_mock.return_value = CompletedProcess(
            args=[cmd_args],
            returncode=0,
            stdout=res
        )

        # when
        Unshell(opt)(script)

        # then
        self.assertEqual(run_mock.mock_calls, [
            call([cmd, cmd_args], capture_output=True),
            call([cmd, cmd_args], capture_output=True)
        ])
        self.assertEqual(print_mock.mock_calls, [
            call(f"• {cmd} {cmd_args}"),
            call(f"➜ {res}"),
            call(f"• {cmd} {cmd_args}"),
            call(f"➜ {res}"),
        ])
