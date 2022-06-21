# type: ignore

# type
from dataclasses import dataclass
from typing import Callable
# framework
import pytest
from unittest.mock import call, MagicMock
# mock
import builtins
import asyncio
# under test
from .core import Unshell

# mock
loop = asyncio.get_event_loop()


def make_future_process(
    return_code,
    stdout,
    stderr
):
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
        returncode = return_code

        async def wait(self):
            return None

        async def communicate(self):
            return [Stdout(), Stderr()]

    future_process = asyncio.Future(loop=loop)
    future_process.set_result(Process())

    return future_process

# test


def test_unshell_should_return_function():
    # given
    opt = {"env": {}}

    # when
    output = Unshell(opt)

    # then
    assert isinstance(output, Callable) is True


def test_unshell_should_return_default_options():
    assert isinstance(Unshell(), Callable) is True


def test_unshell_should_raise_if_script_not_generator():
    # given
    def script():
        return "echo OK"

    # then
    with pytest.raises(TypeError):
        Unshell()(script)


def test_unshell_should_process_command():
    # given
    opt = {"env": {}}
    cmd = "echo OK"
    stdout = "result of echo OK"
    stderr = ""

    def script():
        yield f"{cmd}"

    # mock
    builtins.print = MagicMock()
    asyncio.create_subprocess_shell = MagicMock(return_value=make_future_process(0, stdout, stderr))

    # when
    Unshell(opt)(script)

    # then
    asyncio.create_subprocess_shell.assert_called_once_with(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    assert builtins.print.mock_calls == [
        call(f"• {cmd}"),
        call(f"➜ {stdout}"),
    ]


def test_unshell_should_not_process_unvalid_command():
    # given
    opt = {"env": {}}

    def script():
        yield ""

    # mock
    builtins.print = MagicMock()

    # when
    Unshell(opt)(script)

    # then
    builtins.print.assert_not_called()


def test_unshell_should_handle_command_throwing_error():
    # given
    opt = {"env": {}}
    cmd = "echo OK"
    stderr = "cmd error"

    def script():
        yield f"{cmd}"

    # mock
    builtins.print = MagicMock()
    asyncio.create_subprocess_shell = MagicMock(return_value=make_future_process(1, None, stderr))

    # when
    try:
        Unshell(opt)(script)
    except Exception as err:
        # then
        err_msg = f"{cmd}: {stderr}"
        assert str(err) == err_msg
        assert builtins.print.mock_calls == [
            call(f"• {cmd}"),
            call(f"{err_msg}"),
        ]


def test_unshell_should_throw_if_nothing_returns():
    # given
    opt = {"env": {}}
    cmd = "echo OK"

    def script():
        yield f"{cmd}"

    # mock
    builtins.print = MagicMock()
    asyncio.create_subprocess_shell = MagicMock(return_value=make_future_process(None, None, None))

    # when
    try:
        Unshell(opt)(script)
    except Exception as err:
        # then
        err_msg = "unshell: something went wrong"
        assert str(err) == err_msg
        assert builtins.print.mock_calls == [
            call(f"• {cmd}"),
        ]


def test_unshell_should_process_several_command():
    # given
    opt = {"env": {}}
    cmd = "echo OK"
    stdout = "result of echo OK"

    def script():
        yield f"{cmd}"
        yield f"{cmd}"

    # mock
    builtins.print = MagicMock()
    asyncio.create_subprocess_shell = MagicMock(return_value=make_future_process(0, stdout, None))

    # when
    Unshell(opt)(script)

    # then
    assert asyncio.create_subprocess_shell.mock_calls == [
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
    ]
    assert builtins.print.mock_calls == [
        call(f"• {cmd}"),
        call(f"➜ {stdout}"),
        call(f"• {cmd}"),
        call(f"➜ {stdout}"),
    ]


def test_unshell_should_process_yield_and_return_command():
    # given
    opt = {"env": {}}
    cmd = "echo OK"
    stdout = "result of echo OK"

    def script():
        yield f"{cmd}"
        return f"{cmd}"

    # mock
    builtins.print = MagicMock()
    asyncio.create_subprocess_shell = MagicMock(return_value=make_future_process(0, stdout, None))

    # when
    Unshell(opt)(script)

    # then
    assert asyncio.create_subprocess_shell.mock_calls == [
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
    ]
    assert builtins.print.mock_calls == [
        call(f"• {cmd}"),
        call(f"➜ {stdout}"),
        call(f"• {cmd}"),
        call(f"➜ {stdout}"),
    ]


def test_unshell_should_pass_cmd_res_to_next_cmd():
    # given
    opt = {"env": {}}
    cmd1 = "echo 1"
    cmd2 = "echo 2"
    stdout = "result of echo"

    def script():
        cmd1_res = yield f"{cmd1}"
        yield f"{cmd2} {cmd1_res}"

    # mock
    builtins.print = MagicMock()
    asyncio.create_subprocess_shell = MagicMock(return_value=make_future_process(0, stdout, None))

    # when
    Unshell(opt)(script)

    # then
    assert asyncio.create_subprocess_shell.mock_calls == [
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
    ]


def test_unshell_should_pass_args_to_script():
    # given
    opt = {"env": {}}
    cmd = "echo"
    script_args = ['1', '2']
    stdout = "result of echo"

    def script(*args):
        for arg in args:
            yield f"{cmd} {arg}"

    # mock
    builtins.print = MagicMock()
    asyncio.create_subprocess_shell = MagicMock(return_value=make_future_process(0, stdout, None))

    # when
    Unshell(opt)(script, *script_args)

    # then
    assert asyncio.create_subprocess_shell.mock_calls == [
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
    ]
    assert builtins.print.mock_calls == [
        call(f"• {cmd} {script_args[0]}"),
        call(f"➜ {stdout}"),
        call(f"• {cmd} {script_args[1]}"),
        call(f"➜ {stdout}"),
    ]


def test_unshell_should_process_async_command():
    # given
    opt = {"env": {}}
    cmd = "echo OK"
    stdout = "result of echo OK"
    stderr = ""

    async def do_cmd():
        return cmd

    async def script():
        yield f"{await do_cmd()}"
        yield f"{await do_cmd()}"

    # mock
    builtins.print = MagicMock()
    asyncio.create_subprocess_shell = MagicMock(return_value=make_future_process(0, stdout, stderr))

    # when
    Unshell(opt)(script)

    # then
    assert asyncio.create_subprocess_shell.mock_calls == [
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
    ]
    assert builtins.print.mock_calls == [
        call(f"• {cmd}"),
        call(f"➜ {stdout}"),
        call(f"• {cmd}"),
        call(f"➜ {stdout}")
    ]


def test_unshell_should_pass_cmd_res_to_next_async_cmd():
    # given
    opt = {"env": {}}
    cmd1 = "echo 1"
    cmd2 = "echo 2"
    stdout = "result of echo OK"
    stderr = ""

    async def do_cmd1():
        return cmd1

    async def do_cmd2():
        return cmd2

    async def script():
        cmd_res = yield f"{await do_cmd1()}"
        yield f"{await do_cmd2()} {cmd_res}"

    # mock
    builtins.print = MagicMock()
    asyncio.create_subprocess_shell = MagicMock(return_value=make_future_process(0, stdout, stderr))

    # when
    Unshell(opt)(script)

    # then
    assert asyncio.create_subprocess_shell.mock_calls == [
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
    ]
    assert builtins.print.mock_calls == [
        call(f"• {cmd1}"),
        call(f"➜ {stdout}"),
        call(f"• {cmd2} {stdout}"),
        call(f"➜ {stdout}")
    ]
