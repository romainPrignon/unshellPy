from dataclasses import dataclass
from typing import Callable, List
from .type import Options

import unittest
import asyncio
from unittest.mock import patch, call

# test
from .core import Unshell


# mock
loop = asyncio.get_event_loop()


def make_future_process(return_code, stdout, stderr):
    @dataclass
    class Stdout:
        def decode(self, format):
            return stdout

    @dataclass
    class Stderr:
        def decode(self, format):
            return stderr

    @dataclass
    class Process:
        returncode: int = return_code

        async def wait(self):
            return

        async def communicate(self):
            return [Stdout(), Stderr()]

    future_process: asyncio.Future = asyncio.Future(loop=loop)
    future_process.set_result(Process())

    return future_process


class TestUnshell(unittest.TestCase):
    def test_unshell_should_return_function(self):
        # given
        opt: Options = {"env": {}}

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
    @patch('asyncio.create_subprocess_shell')
    def test_unshell_should_process_command(self, shell_mock, print_mock):
        # given
        opt = {"env": {}}
        cmd: str = "echo OK"
        stdout: str = "result of echo OK"
        stderr: str = ""

        def script():
            yield f"{cmd}"

        # mock
        shell_mock.return_value = make_future_process(0, stdout, stderr)

        # when
        Unshell(opt)(script)

        # then
        shell_mock.assert_called_once_with(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        self.assertEqual(print_mock.mock_calls, [
            call(f"• {cmd}"),
            call(f"➜ {stdout}"),
        ])

    @patch('builtins.print')
    @patch('asyncio.create_subprocess_shell')
    def test_unshell_should_not_process_unvalid_command(
        self, shell_mock, print_mock
    ):
        # given
        opt = {"env": {}}

        def script():
            yield ""

        # when
        Unshell(opt)(script)

        # then
        shell_mock.assert_not_called()
        print_mock.assert_not_called()

    @patch('builtins.print')
    @patch('asyncio.create_subprocess_shell')
    def test_unshell_should_handle_command_throwing_error(
        self, shell_mock, print_mock
    ):
        # given
        opt = {"env": {}}
        cmd: str = "echo OK"
        stderr: str = "cmd error"

        def script():
            yield f"{cmd}"

        # mock
        shell_mock.return_value = make_future_process(1, None, stderr)

        # when
        try:
            Unshell(opt)(script)
        except Exception as err:
            # then
            err_msg = f"{cmd}: {stderr}"
            self.assertEqual(str(err), err_msg)
            self.assertEqual(print_mock.mock_calls, [
                call(f"• {cmd}"),
                call(f"{err_msg}"),
            ])

    @patch('builtins.print')
    @patch('asyncio.create_subprocess_shell')
    def test_unshell_should_throw_if_nothing_returns(
        self, shell_mock, print_mock
    ):
        # given
        opt = {"env": {}}
        cmd: str = "echo OK"

        def script():
            yield f"{cmd}"

        # mock
        shell_mock.return_value = make_future_process(None, None, None)

        # when
        try:
            Unshell(opt)(script)
        except Exception as err:
            # then
            err_msg = f"unshell: something went wrong"
            self.assertEqual(str(err), err_msg)
            self.assertEqual(print_mock.mock_calls, [
                call(f"• {cmd}"),
            ])

    @patch('builtins.print')
    @patch('asyncio.create_subprocess_shell')
    def test_unshell_should_process_several_command(
        self,
        shell_mock,
        print_mock
    ):
        # given
        opt = {"env": {}}
        cmd: str = "echo OK"
        stdout: str = "result of echo OK"

        def script():
            yield f"{cmd}"
            yield f"{cmd}"

        # mock
        shell_mock.return_value = make_future_process(0, stdout, None)

        # when
        Unshell(opt)(script)

        # then
        self.assertEqual(shell_mock.mock_calls, [
            call(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
            call(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
        ])
        self.assertEqual(print_mock.mock_calls, [
            call(f"• {cmd}"),
            call(f"➜ {stdout}"),
            call(f"• {cmd}"),
            call(f"➜ {stdout}"),
        ])

    @patch('builtins.print')
    @patch('asyncio.create_subprocess_shell')
    def test_unshell_should_process_yield_and_return_command(
        self,
        shell_mock,
        print_mock
    ):
        # given
        opt = {"env": {}}
        cmd: str = "echo OK"
        stdout: str = "result of echo OK"

        def script():
            yield f"{cmd}"
            return f"{cmd}"

        # mock
        shell_mock.return_value = make_future_process(0, stdout, None)

        # when
        Unshell(opt)(script)

        # then
        self.assertEqual(shell_mock.mock_calls, [
            call(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
            call(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
        ])
        self.assertEqual(print_mock.mock_calls, [
            call(f"• {cmd}"),
            call(f"➜ {stdout}"),
            call(f"• {cmd}"),
            call(f"➜ {stdout}"),
        ])

    @patch('builtins.print')
    @patch('asyncio.create_subprocess_shell')
    def test_unshell_should_pass_cmd_res_to_next_cmd(
        self,
        shell_mock,
        print_mock
    ):
        # given
        opt = {"env": {}}
        cmd1: str = "echo 1"
        cmd2: str = "echo 2"
        stdout: str = "result of echo"

        def script():
            cmd1_res = yield f"{cmd1}"
            yield f"{cmd2} {cmd1_res}"

        # mock
        shell_mock.return_value = make_future_process(0, stdout, None)

        # when
        Unshell(opt)(script)

        # then
        self.assertEqual(shell_mock.mock_calls, [
            call(
                cmd1,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
            call(
                f"{cmd2} {stdout}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
        ])

    @patch('builtins.print')
    @patch('asyncio.create_subprocess_shell')
    def test_unshell_should_pass_args_to_script(self, shell_mock, print_mock):
        # given
        opt = {"env": {}}
        cmd: str = "echo"
        script_args: List[str] = ['1', '2']
        stdout: str = "result of echo"

        def script(*args: List[str]):
            for arg in args:
                yield f"{cmd} {arg}"

        # mock
        shell_mock.return_value = make_future_process(0, stdout, None)

        # when
        Unshell(opt)(script, *script_args)

        # then
        self.assertEqual(shell_mock.mock_calls, [
            call(
                f"{cmd} {script_args[0]}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
            call(
                f"{cmd} {script_args[1]}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
        ])
        self.assertEqual(print_mock.mock_calls, [
            call(f"• {cmd} {script_args[0]}"),
            call(f"➜ {stdout}"),
            call(f"• {cmd} {script_args[1]}"),
            call(f"➜ {stdout}"),
        ])

    @patch('builtins.print')
    @patch('asyncio.create_subprocess_shell')
    def test_unshell_should_process_async_command(
        self,
        shell_mock,
        print_mock
    ):
        # given
        opt = {"env": {}}
        cmd: str = "echo OK"
        stdout: str = "result of echo OK"
        stderr: str = ""

        async def do_cmd():
            return cmd

        async def script():
            yield f"{await do_cmd()}"
            yield f"{await do_cmd()}"

        # mock
        shell_mock.return_value = make_future_process(0, stdout, stderr)

        # when
        Unshell(opt)(script)

        # then
        self.assertEqual(shell_mock.mock_calls, [
            call(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
            call(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
        ])
        self.assertEqual(print_mock.mock_calls, [
            call(f"• {cmd}"),
            call(f"➜ {stdout}"),
            call(f"• {cmd}"),
            call(f"➜ {stdout}")
        ])

    @patch('builtins.print')
    @patch('asyncio.create_subprocess_shell')
    def test_unshell_should_pass_cmd_res_to_next_async_cmd(
        self,
        shell_mock,
        print_mock
    ):
        # given
        opt = {"env": {}}
        cmd1: str = "echo 1"
        cmd2: str = "echo 2"
        stdout: str = "result of echo OK"
        stderr: str = ""

        async def do_cmd1():
            return cmd1

        async def do_cmd2():
            return cmd2

        async def script():
            cmd_res = yield f"{await do_cmd1()}"
            yield f"{await do_cmd2()} {cmd_res}"

        # mock
        shell_mock.return_value = make_future_process(0, stdout, stderr)

        # when
        Unshell(opt)(script)

        # then
        self.assertEqual(shell_mock.mock_calls, [
            call(
                cmd1,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
            call(
                f"{cmd2} {stdout}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
        ])
        self.assertEqual(print_mock.mock_calls, [
            call(f"• {cmd1}"),
            call(f"➜ {stdout}"),
            call(f"• {cmd2} {stdout}"),
            call(f"➜ {stdout}")
        ])
