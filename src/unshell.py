from typing import Awaitable, Any, Callable, NotReturn, Generator, AsyncGenerator

from subprocess import run
from os import system

def Unshell(opt: Options):
    def exec(script: Script, *args: Args) -> Awaitable[Any]:
        assert_unshell_scritpt(script)

        commands = script(*args)

        for command in commands:
            system(cmd)

    return exec

def assert_unshell_scritpt (fn: Callable) -> bool | NotReturn:
  if is_generator(fn): return True
  if is_async_generator(fn): return True

  raise TypeError('unshell: Invalid SCRIPT')

def is_generator (fn: Callable) -> bool:
    # inspect.isgeneratorfunction(fn)
    return isinstance(fn, Generator)

def is_async_generator (fn: Callable) -> bool:
    # inspect.isgeneratorfunction(fn)
    return isinstance(fn, AsyncGenerator)
