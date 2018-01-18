import string
import random

import pytest

from data_structures.linked_list import LinkedListNode, LinkedList, BaseNode

_non_nodes = [5, BaseNode(None), 13.5, int, pytest, 'banana']
_orderable_lists = [list(range(10)), [c for c in string.ascii_letters], [], [1, 3, 1.1, -50, 0, 3.1415639]]
_unorderable_lists = [['banana', 50, BaseNode(None)], [1, 2, 3, None],
                      [c for c in string.ascii_letters] + list(range(10))]
_constructor_args = _unorderable_lists + _orderable_lists


@pytest.fixture(params=_non_nodes, ids=repr)
def not_a_node(request):
    return request.param


@pytest.fixture(params=_constructor_args, ids=repr)
def constructor_arg(request):
    return request.param


def test_node_construction():
    # See test_node.py for a more thorough testing of base construction.
    node = LinkedListNode(5)
    assert node.value == 5
    assert node.next_node is None


def test_node_next_pass():
    node = LinkedListNode('base')

    test_node = LinkedListNode(7)
    node.next_node = test_node
    assert node.next_node is test_node

    test_node = None
    node.next_node = test_node
    assert node.next_node is test_node


def test_node_next_fail(not_a_node):
    node = LinkedListNode('base')

    with pytest.raises(TypeError):
        node.next_node = not_a_node


def test_linked_list_empty_constructor():
    ll = LinkedList()
    assert ll.head is None

def test_linked_list_None_constructor():
    with pytest.raises(TypeError):
        LinkedList(None)


def test_linked_list_constructor(constructor_arg):
    assert bool(LinkedList(constructor_arg)) == bool(constructor_arg)


def test__get(constructor_arg):
    ll = LinkedList(constructor_arg)
    if constructor_arg:
        for index, item in enumerate(constructor_arg):
            assert isinstance(ll._get(index), LinkedListNode)
            assert ll._get(index).value == item
    else:
        assert ll.head is None


def test_insert(constructor_arg):
    max_index = len(constructor_arg) if constructor_arg else 0
    idx = random.randint(0, max_index)

    # Test a valid index
    ll = LinkedList(constructor_arg)
    ll.insert(idx, 'test')
    assert ll._get(idx) == LinkedListNode('test')

    # Test some invalid cases
    if max_index:
        ll = LinkedList(constructor_arg)
        with pytest.raises(IndexError):
            ll.insert(2*max_index, 'test')

        ll = LinkedList(constructor_arg)
        with pytest.raises(IndexError):
            ll.insert(-max_index, 'test')

    ll = LinkedList(constructor_arg)
    with pytest.raises(IndexError):
        ll.insert('Um, an index', 'test')

    ll = LinkedList(constructor_arg)
    with pytest.raises(IndexError):
        ll.insert(None, 'test')


def test_append(constructor_arg):
    ll = LinkedList(constructor_arg)
    ll.append('test')
    assert ll._get(len(ll) - 1) == LinkedListNode('test')


def test_pop(constructor_arg):
    max_index = len(constructor_arg) - 1 if constructor_arg else 0
    idx = random.randint(0, max_index)

    ll = LinkedList(constructor_arg)

    if len(ll) == 0:
        with pytest.raises(IndexError):
            ll.pop(idx)
    else:
        node_to_pop = ll._get(idx)
        assert ll.pop(idx) == node_to_pop.value

    ll = LinkedList(constructor_arg)
    with pytest.raises(IndexError):
        ll.pop(2 * max_index)

    ll = LinkedList(constructor_arg)
    with pytest.raises(IndexError):
        ll.pop(-max_index)

    ll = LinkedList(constructor_arg)
    with pytest.raises(IndexError):
        ll.pop('Um, an index')

    ll = LinkedList(constructor_arg)
    if len(ll) == 0:
        with pytest.raises(IndexError):
            ll.pop()
    else:
        node_to_pop = ll.head
        assert ll.pop() == node_to_pop.value


def test_reverse(constructor_arg):
    ll = LinkedList(constructor_arg)
    ll.reverse()
    assert list(ll) == list(reversed(list(constructor_arg)))


def test_bubble_sort():
    test_list = [random.randint(0, 100) for _ in range(100)]
    ll = LinkedList(test_list)
    ll.sorted(method='bubble_sort')
    assert list(ll) == sorted(test_list)

    ll = LinkedList([1])
    ll.sorted(method='bubble_sort')
    assert list(ll) == [1]

    ll = LinkedList()
    ll.sorted(method='bubble_sort')
    assert list(ll) == []


def test_insertion_sort():
    test_list = [random.randint(0, 100) for _ in range(100)]
    ll = LinkedList(test_list)
    ll.sorted(method='insertion_sort')
    assert list(ll) == sorted(test_list)

    ll = LinkedList([1])
    ll.sorted(method='insertion_sort')
    assert list(ll) == [1]

    ll = LinkedList()
    ll.sorted(method='insertion_sort')
    assert list(ll) == []


def test_merge_sort():
    test_list = [random.randint(0, 100) for _ in range(100)]
    ll = LinkedList(test_list)
    ll.sorted(method='merge_sort')
    assert list(ll) == sorted(test_list)

    ll = LinkedList([1])
    ll.sorted(method='merge_sort')
    assert list(ll) == [1]

    ll = LinkedList()
    ll.sorted(method='merge_sort')
    assert list(ll) == []

