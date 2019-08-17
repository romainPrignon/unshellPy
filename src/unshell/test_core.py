from dataclasses import dataclass
from typing import Callable, List, Union, Optional
from typing_extensions import Literal
from .type import Options, Commands, AsyncCommands

import unittest
import asyncio
from asyncio import Future
from unittest.mock import patch, call, Mock

# test
from .core import Unshell

# type
ReturnCode = Union[Literal[0], Literal[1]]

# mock
loop = asyncio.get_event_loop()


def make_future_process(
    return_code: Union[None, ReturnCode],
    stdout: Optional[str],
    stderr: Optional[str]
) -> Future:
    @dataclass
    class Stdout:
        def decode(self, format: str) -> Optional[str]:
            return stdout

    @dataclass
    class Stderr:
        def decode(self, format: str) -> Optional[str]:
            return stderr

    @dataclass
    class Process:
        returncode: Union[None, ReturnCode] = return_code

        async def wait(self) -> None:
            return None

        async def communicate(self) -> List[object]:
            return [Stdout(), Stderr()]

    future_process: asyncio.Future = asyncio.Future(loop=loop)
    future_process.set_result(Process())

    return future_process


class TestCore(unittest.TestCase):
    def test_unshell_should_return_function(self) -> None:
        # given
        opt: Options = {"env": {}}

        # when
        output = Unshell(opt)

        # then
        self.assertTrue(isinstance(output, Callable))  # type: ignore

    def test_unshell_should_return_default_options(self) -> None:
        self.assertTrue(isinstance(Unshell(), Callable))  # type: ignore

    def test_unshell_should_raise_if_script_not_generator(self) -> None:
        # given
        def script() -> str:
            return "echo OK"

        # then
        with self.assertRaises(TypeError):
            Unshell()(script)  # type: ignore

    @patch('builtins.print')
    @patch('asyncio.create_subprocess_shell')
    def test_unshell_should_process_command(self, shell_mock: Mock, print_mock: Mock) -> None:
        # given
        opt: Options = {"env": {}}
        cmd: str = "echo OK"
        stdout: str = "result of echo OK"
        stderr: str = ""

        def script() -> Commands:  # type: ignore
            yield f"{cmd}"

        # mock
        shell_mock.return_value = make_future_process(0, stdout, stderr)

        # when
        Unshell(opt)(script)  # type: ignore

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
        self, shell_mock: Mock, print_mock: Mock
    ) -> None:
        # given
        opt: Options = {"env": {}}

        def script() -> Commands:  # type: ignore
            yield ""

        # when
        Unshell(opt)(script)  # type: ignore

        # then
        shell_mock.assert_not_called()
        print_mock.assert_not_called()

    @patch('builtins.print')
    @patch('asyncio.create_subprocess_shell')
    def test_unshell_should_handle_command_throwing_error(
        self, shell_mock: Mock, print_mock: Mock
    ) -> None:
        # given
        opt: Options = {"env": {}}
        cmd: str = "echo OK"
        stderr: str = "cmd error"

        def script() -> Commands:  # type: ignore
            yield f"{cmd}"

        # mock
        shell_mock.return_value = make_future_process(1, None, stderr)

        # when
        try:
            Unshell(opt)(script)  # type: ignore
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
        self, shell_mock: Mock, print_mock: Mock
    ) -> None:
        # given
        opt: Options = {"env": {}}
        cmd: str = "echo OK"

        def script() -> Commands:  # type: ignore
            yield f"{cmd}"

        # mock
        shell_mock.return_value = make_future_process(None, None, None)

        # when
        try:
            Unshell(opt)(script)  # type: ignore
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
        shell_mock: Mock,
        print_mock: Mock
    ) -> None:
        # given
        opt: Options = {"env": {}}
        cmd: str = "echo OK"
        stdout: str = "result of echo OK"

        def script() -> Commands:  # type: ignore
            yield f"{cmd}"
            yield f"{cmd}"

        # mock
        shell_mock.return_value = make_future_process(0, stdout, None)

        # when
        Unshell(opt)(script)  # type: ignore

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
        shell_mock: Mock,
        print_mock: Mock
    ) -> None:
        # given
        opt: Options = {"env": {}}
        cmd: str = "echo OK"
        stdout: str = "result of echo OK"

        def script() -> Commands:
            yield f"{cmd}"
            return f"{cmd}"

        # mock
        shell_mock.return_value = make_future_process(0, stdout, None)

        # when
        Unshell(opt)(script)  # type: ignore

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
        shell_mock: Mock,
        print_mock: Mock
    ) -> None:
        # given
        opt: Options = {"env": {}}
        cmd1: str = "echo 1"
        cmd2: str = "echo 2"
        stdout: str = "result of echo"

        def script() -> Commands:  # type: ignore
            cmd1_res = yield f"{cmd1}"
            yield f"{cmd2} {cmd1_res}"

        # mock
        shell_mock.return_value = make_future_process(0, stdout, None)

        # when
        Unshell(opt)(script)  # type: ignore

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
    def test_unshell_should_pass_args_to_script(self, shell_mock: Mock, print_mock: Mock) -> None:
        # given
        opt: Options = {"env": {}}
        cmd: str = "echo"
        script_args: List[str] = ['1', '2']
        stdout: str = "result of echo"

        def script(*args: List[str]) -> Commands:  # type: ignore
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
        shell_mock: Mock,
        print_mock: Mock
    ) -> None:
        # given
        opt: Options = {"env": {}}
        cmd: str = "echo OK"
        stdout: str = "result of echo OK"
        stderr: str = ""

        async def do_cmd() -> str:
            return cmd

        async def script() -> AsyncCommands:
            yield f"{await do_cmd()}"
            yield f"{await do_cmd()}"

        # mock
        shell_mock.return_value = make_future_process(0, stdout, stderr)

        # when
        Unshell(opt)(script)  # type: ignore

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
        shell_mock: Mock,
        print_mock: Mock
    ) -> None:
        # given
        opt: Options = {"env": {}}
        cmd1: str = "echo 1"
        cmd2: str = "echo 2"
        stdout: str = "result of echo OK"
        stderr: str = ""

        async def do_cmd1() -> str:
            return cmd1

        async def do_cmd2() -> str:
            return cmd2

        async def script() -> AsyncCommands:
            cmd_res = yield f"{await do_cmd1()}"
            yield f"{await do_cmd2()} {cmd_res}"

        # mock
        shell_mock.return_value = make_future_process(0, stdout, stderr)

        # when
        Unshell(opt)(script)  # type: ignore

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
