import operator

import pytest

from data_structures.node import BaseNode

_base_data = [None, 12, int, 32.5, BaseNode(15), pytest]
_comparison_data = [(None, None), (None, 12), (0, None),
                    (0, 12), (10, 15), (35.7, 22.3), (10, 10),
                    (int, float), ('abc', 'aaa'), (BaseNode(5), BaseNode(3)), (BaseNode(5), BaseNode(5))]
_operators = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt, operator.ge]


@pytest.fixture(params=_base_data, ids=repr)
def base_data(request):
    return request.param


@pytest.fixture(params=_comparison_data, ids=repr)
def comparison_data(request):
    return request.param


@pytest.fixture(params=_operators, ids=lambda p: p.__name__)
def operation(request):
    return request.param


def test_construction(base_data):
    b = BaseNode(base_data)
    assert b.value == base_data


def test_comparison(comparison_data, operation):
    a, b = comparison_data
    A, B = BaseNode(a), BaseNode(b)

    try:
        operation(a, b) == operation(A, B)
    except Exception as e:
        with pytest.raises(e.__class__):
            operation(a, b)


def test_bool(base_data):
    assert bool(BaseNode(base_data))
