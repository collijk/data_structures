import string
import random

import pytest

from data_structures.stack import Stack, parentheses_balanced


def test_stack_init():
    s = Stack()
    assert not s._storage
    assert s._maxsize == 50

    s = Stack(100)
    assert not s._storage
    assert s._maxsize == 100


def test_stack_peek():
    s = Stack()
    with pytest.raises(LookupError):
        s.peek()

    s._storage = [10]
    assert s.peek() == 10


def test_stack_pop():
    s = Stack()
    with pytest.raises(LookupError):
        s.pop()

    s._storage = [10]
    assert s.pop() == 10

    with pytest.raises(LookupError):
        s.pop()


def test_stack_push():
    s = Stack(maxsize=1)
    assert not s._storage
    s.push(10)
    assert s._storage == [10]
    with pytest.raises(OverflowError):
        s.push(10)


def generate_good_expression_only_parens(seed):
    chars = string.printable
    pairs = {
        ')': '(',
        '}': '{',
        ']': '[',
    }
    parens = [item for pair in pairs.items() for item in pair]
    not_parens = [c for c in chars if c not in parens]

    open = Stack()
    closed = Stack()








def test_are_parentheses_balanced_empty():
    assert parentheses_balanced("")



