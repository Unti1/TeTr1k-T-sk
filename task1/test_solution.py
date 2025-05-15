import pytest
from task1.solution import strict

@strict
def sum_two(a: int, b: int) -> int:
    return a + b

@strict
def concat_strings(s1: str, s2: str) -> str:
    return s1 + s2

@strict
def multiply_float(x: float, y: float) -> float:
    return x * y

@strict
def check_bool(b: bool) -> bool:
    return b

def test_sum_two_valid():
    assert sum_two(1, 2) == 3

def test_sum_two_invalid():
    with pytest.raises(TypeError):
        sum_two(1, 2.4)

def test_concat_strings_valid():
    assert concat_strings("Hello, ", "World!") == "Hello, World!"

def test_concat_strings_invalid():
    with pytest.raises(TypeError):
        concat_strings("Hello, ", 123)

def test_multiply_float_valid():
    assert multiply_float(2.5, 3.0) == 7.5

def test_multiply_float_invalid():
    with pytest.raises(TypeError):
        multiply_float(2.5, 3)

def test_check_bool_valid():
    assert check_bool(True) is True

def test_check_bool_invalid():
    with pytest.raises(TypeError):
        check_bool(1) 