# type: ignore

# framework
import os
import subprocess
from unittest.mock import MagicMock
# mock
import builtins


def test_cli_should_display_help_on_help_command():
    # given
    abs_test_path = os.path.dirname(os.path.abspath(__file__))
    cli_path = f"{abs_test_path}/../../unshell/cli.py"
    unshell_command = 'help'

    # mock
    builtins.print = MagicMock()

    # when
    process_result = subprocess.run(
        f"python {cli_path} {unshell_command}",
        capture_output=True
    )
    stdout = process_result.stdout
    # stderr = process_result.stderr
    # return_code = process_result.returncode

    # then
    assert stdout == """
Execute script through unshell runtime

Usage:
unshell COMMAND [SCRIPT_PATH] [ARGS...]

Commands:
help      Print this help message
run       run a script through unshell runtime
"""
