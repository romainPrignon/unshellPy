# type: ignore

# test
from .colors import red, green


def test_red():
    # given
    val = 'value'

    # when
    output = red(val)

    # then
    assert output == f"\x1b[31m{val}\x1b[0m"


def test_green():
    # given
    val = 'value'

    # when
    output = green(val)

    # then
    assert output == f"\x1b[32m{val}\x1b[0m"
