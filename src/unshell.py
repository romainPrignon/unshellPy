from typing import Any, Callable
from type import Options, Script, Args, Commands, Command

import inspect
import subprocess

defaultOptions = Options(env={})


def Unshell(opt: Options = defaultOptions):
    def exec(script: Script, *args: Args) -> Any:
        assert_unshell_script(script)

        commands: Commands = script(*args)
        cmd_res = None

        while True:
            try:
                command: Command = commands.send(cmd_res)

                if not isValidCmd(command):
                    continue

                cmd_res = do_exec(command)

            except StopIteration as command:
                if not command.value:  # if there is no return
                    break

                if not isValidCmd(command.value):
                    continue

                cmd_res = do_exec(command.value)
                break

    return exec


def do_exec(command: Command) -> str:
    print(f"• {command}")

    process_result = subprocess.run(
        command.split(),
        capture_output=True
    )
    stdout = process_result.stdout
    stderr = process_result.stderr
    return_code = process_result.returncode

    if stderr and return_code:
        err = f"{command}: {stderr}"

        print(err)
        raise Exception(err)

        return stderr

    if stdout:
        print(f"➜ {stdout}")

        return stdout

    raise Exception("unshell: something went wrong")


def assert_unshell_script(fn: Callable) -> bool:
    if is_async_generator(fn):
        return True
    if is_generator(fn):
        return True

    raise TypeError('unshell: Invalid SCRIPT')


def is_generator(fn: Callable) -> bool:
    return inspect.isgeneratorfunction(fn)


def is_async_generator(fn: Callable) -> bool:
    return inspect.isgeneratorfunction(fn) and inspect.iscoroutinefunction(fn)


def isValidCmd(cmd: str) -> bool:
    return bool(cmd)
