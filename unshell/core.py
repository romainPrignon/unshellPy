from typing import Any, Callable, List, Union, cast, Type, Optional, Awaitable
from .type import CommandResult, Script, Command, Engine, \
    AsyncScript, Options, Commands, AsyncCommands, Args

import inspect
import asyncio

AsyncSend = Callable[[Optional[Union[str, List[str]]]], Awaitable[Union[str, List[str]]]]
Send = Callable[[Optional[Union[str, List[str]]]], Union[str, List[str]]]

defaultOptions: Options = {
    "env": {}
}


def Unshell(opt: Optional[Options] = defaultOptions) -> Engine:
    async def engine(script: Union[Script, AsyncScript], *args: Args) -> Any:
        if is_async_generator(script):
            commands = script(*args)
            commands = cast(AsyncCommands, commands)

            return await iter(commands.asend, StopAsyncIteration, True)

        if is_generator(script):
            commands = script(*args)
            commands = cast(Commands, commands)

            return await iter(commands.send, StopIteration, False)

        raise TypeError('unshell: Invalid SCRIPT')

    return lambda script, *args: asyncio.run(engine(script, *args))


async def iter(
    send: Union[Send, AsyncSend],
    exception: Union[Type[StopIteration], Type[StopAsyncIteration]],
    is_async: bool
) -> None:
    cmd_res: CommandResult = None
    command: Command = ""

    while True:
        try:
            if is_async:
                send = cast(AsyncSend, send)
                command = await send(cmd_res)
            else:
                send = cast(Send, send)
                command = send(cmd_res)

            if not isValidCmd(command):
                continue

            if isinstance(command, list):
                cmd_res = await asyncio.gather(*[exec(cmd) for cmd in command])
            else:
                cmd_res = await exec(command)

        except exception as command:
            if not hasattr(command, "value"):  # if there is no return
                break

            if not isValidCmd(command.value):
                break

            if isinstance(command, list):
                cmd_res = await asyncio.gather(*[exec(cmd) for cmd in command.value])
            else:
                cmd_res = await exec(command.value)
            break


async def exec(command: Command) -> str:
    print(f"• {command}")

    process_result = await asyncio.create_subprocess_shell(
        cast(str, command),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await process_result.wait()

    stdout, stderr = await process_result.communicate()
    return_code = process_result.returncode

    stdoutDecoded = stdout.decode('utf-8')
    stderrDecoded = stderr.decode('utf-8')

    if stderrDecoded and return_code:
        err = f"{command}: {stderrDecoded}"

        print(err)
        raise Exception(err)

    if stdoutDecoded:
        print(f"➜ {stdoutDecoded}")

        return stdoutDecoded

    raise Exception("unshell: something went wrong")


def is_generator(fn: Any) -> bool:
    return inspect.isgeneratorfunction(fn)


def is_async_generator(fn: Any) -> bool:
    return inspect.isasyncgenfunction(fn)


def isValidCmd(cmd: Union[str, List[str]]) -> bool:
    return bool(cmd)
