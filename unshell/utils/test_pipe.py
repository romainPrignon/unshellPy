# type: ignore

# type
from typing import Callable

# test
from .pipe import pipe


def test_pipe_should_return_a_function():
    # given
    def echo(x):
        return f"echo {x}"

    # when
    output = pipe(echo)

    # then
    assert isinstance(output, Callable) is True


def test_pipe_should_return_an_empty_string():
    # given
    def echo(x):
        return f"echo {x}"

    # when
    param = "hello world"
    output = pipe(echo)(param)

    # then
    assert output == f"echo {param}"


def test_pipe_should_pipe_two_function():
    # given
    def echo(x):
        return f"echo {x}"

    def grep():
        return "grep world"

    # when
    param = "hello world"
    output = pipe(echo, grep)(param)

    # then
    assert output == f"echo {param} | grep world"
