#!/usr/bin/env python

from typing import List, Any, cast
from unshell.type import Args, Script

import os
import sys
import importlib.util
from unshell.core import Unshell
from unshell.utils import colors


def help(argv: Args, env: os._Environ) -> None:
    print("""
Execute script through unshell runtime

Usage:
unshell COMMAND [SCRIPT_PATH] [ARGS...]

Commands:
help      Print this help message
run       run a script through unshell runtime
""")


def run(argv: List[Any], env: os._Environ) -> None:
    [_, __, scriptPath, *args] = argv

    script = resolveScript(scriptPath)
    opt = {
        "env": env
    }

    try:
        Unshell(opt)(script, *args)
    except Exception as err:  # TODO: handle unshell exception
        msg = f"{colors.red('✘')} unshell: something went wrong"

        print(msg)

        raise err


def resolveScript(scriptPath: str) -> Script:
    try:
        spec = importlib.util.spec_from_file_location("script", scriptPath)
        if spec is None:
            raise TypeError("ModuleSpec is None")
        module = importlib.util.module_from_spec(spec)

        loader = spec.loader
        if loader is None:
            raise TypeError("Loader is None")
        loader.exec_module(module)

        return cast(Script, module.script)
    except Exception as err:
        print(f"{colors.red('✘')} unshell: Invalid SCRIPT_PATH")

        raise err


def cli(argv: List[Any], env: os._Environ) -> None:
    try:
        [_, unshell_command, __] = argv
    except Exception:
        return help(argv, env)

    command_switcher = {
        "help": help,
        "run": run
    }

    try:
        return command_switcher[unshell_command](argv, env)
    except KeyError:
        return help(argv, env)


def main() -> None:  # pragma: no cover
    argv = sys.argv
    env = os.environ

    try:
        cli(argv=argv, env=env)

        sys.exit(0)
    except Exception:
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
