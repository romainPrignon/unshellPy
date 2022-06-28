# type: ignore
import os
from unittest.mock import call, MagicMock
# mock
import builtins
# test
from .cli import cli
from .utils import colors


def test_cli_should_display_help_on_help_command():
    # given
    argv = ['cli.py', 'help']
    env = os.environ

    # mock
    builtins.print = MagicMock()

    # when
    cli(argv, env)

    builtins.print.assert_called_once_with("""
Execute script through unshell runtime

Usage:
unshell COMMAND [SCRIPT_PATH] [ARGS...]

Commands:
help      Print this help message
run       run a script through unshell runtime
""")


def test_cli_should_display_help_if_called_with_nothing():
    # given
    argv = ['cli.py']
    env = os.environ

    # mock
    builtins.print = MagicMock()

    # when
    cli(argv, env)

    # then
    builtins.print.assert_called_once()


def test_cli_should_display_help_if_called_with_no_script():
    # given
    argv = ['cli.py', 'run']
    env = os.environ

    # mock
    builtins.print = MagicMock()

    # when
    cli(argv, env)
    builtins.print.assert_called_once()


def test_cli_should_display_help_on_invalid_command():
    # given
    argv = ['cli.py', 'invalid', 'foo']
    env = os.environ

    # mock
    builtins.print = MagicMock()

    # when
    cli(argv, env)

    # then
    builtins.print.assert_called_once()


def test_cli_should_display_error_on_unresolvable_script():
    # given
    argv = ['cli.py', 'run', 'unresolvable']
    env = os.environ

    # mock
    builtins.print = MagicMock()

    # when
    try:
        cli(argv, env)
    except Exception:
        # then
        builtins.print.assert_called_once_with(
            f"{colors.red('✘')} unshell: Invalid SCRIPT_PATH"
        )


def test_cli_should_display_error_on_errored_script():
    # given
    abs_test_path = os.path.dirname(os.path.abspath(__file__))
    scriptPath = f"{abs_test_path}/../fixtures/scripts/notCompatibleCmd.py"

    argv = ['cli.py', 'run', scriptPath]
    env = os.environ

    # mock
    builtins.print = MagicMock()

    # when
    try:
        cli(argv, env)
    except Exception:
        # then
        builtins.print.assert_called_once_with(
            f"{colors.red('✘')} unshell: something went wrong"
        )


def test_cli_should_execute_script_on_run_command():
    # given
    abs_test_path = os.path.dirname(os.path.abspath(__file__))
    scriptPath = f"{abs_test_path}/../fixtures/scripts/yieldAndReturnCommand.py"
    argv = ['cli.py', 'run', scriptPath]
    env = os.environ

    # mock
    builtins.print = MagicMock()

    # when
    cli(argv, env)

    # then
    assert builtins.print.mock_calls == [
        call("• echo hello"),
        call("➜ hello\n"),
        call("• echo world"),
        call("➜ world\n"),
    ]
