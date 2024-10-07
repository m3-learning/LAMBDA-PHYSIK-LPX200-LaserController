import pytest

from lpx.skeleton import fib, main

__author__ = "erinakin"
__copyright__ = "erinakin"
__license__ = "MIT"


def test_fib():
    pass


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["7"])
    captured = capsys.readouterr()
    assert "The 7-th Fibonacci number is 13" in captured.out
