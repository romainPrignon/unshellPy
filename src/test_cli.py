import unittest
import os
from unittest.mock import patch, call

# test
from src.cli import cli
from src.utils import colors


# mock
# loop = asyncio.get_event_loop()

class TestCli(unittest.TestCase):

    @patch('builtins.print')
    def test_cli_should_display_help_on_help_command(self, print_mock):
        # given
        argv = ['cli.py', 'help']
        env = {}

        # when
        cli(argv, env)

        print_mock.assert_called_once_with("""
Execute script through unshell runtime

Usage:
unshell COMMAND [SCRIPT_PATH] [ARGS...]

Commands:
help      Print this help message
run       run a script through unshell runtime
    """)

    @patch('builtins.print')
    def test_cli_should_display_help_if_called_with_nothing(self, print_mock):
        # given
        argv = ['cli.py']
        env = {}

        # when
        cli(argv, env)

        # then
        print_mock.assert_called_once()

    @patch('builtins.print')
    def test_cli_should_display_help_if_called_with_no_script(
        self,
        print_mock
    ):
        # given
        argv = ['cli.py', 'run']
        env = {}

        # when
        cli(argv, env)
        print_mock.assert_called_once()

    @patch('builtins.print')
    def test_cli_should_display_help_on_invalid_command(self, print_mock):
        # given
        argv = ['cli.py', 'invalid', 'foo']
        env = {}

        # when
        cli(argv, env)

        # then
        print_mock.assert_called_once()

    @patch('builtins.print')
    def test_cli_should_display_error_on_unresolvable_script(self, print_mock):
        # given
        argv = ['cli.py', 'run', 'unresolvable']
        env = {}

        # when
        try:
            cli(argv, env)
        except Exception:
            # then
            print_mock.assert_called_once_with(
                f"{colors.red('✘')} unshell: Invalid SCRIPT_PATH"
            )

    @patch('builtins.print')
    def test_cli_should_display_error_on_errored_script(self, print_mock):
        # given
        abs_test_path = os.path.dirname(os.path.abspath(__file__))
        scriptPath = f"{abs_test_path}/../fixtures/scripts/notCompatibleCmd.py"
        argv = ['cli.py', 'run', scriptPath]
        env = {}

        # when
        try:
            cli(argv, env)
        except Exception:
            # then
            print_mock.assert_called_once_with(
                f"{colors.red('✘')} unshell: something went wrong"
            )

    @patch('builtins.print')
    def test_cli_should_execute_script_on_run_command(self, print_mock):
        # given
        abs_test_path = os.path.dirname(os.path.abspath(__file__))
        scriptPath = f"{abs_test_path}/../fixtures/scripts/yieldAndReturnCommand.py"
        argv = ['cli.py', 'run', scriptPath]
        env = {}

        # when
        cli(argv, env)

        # then
        self.assertEqual(print_mock.mock_calls, [
            call(f"• echo hello"),
            call(f"➜ hello\n"),
            call(f"• echo world"),
            call(f"➜ world\n"),
        ])