import pytest

from data_structures.tree import BSTNode, BST


def test_BSTNode():
    b = BSTNode(3)
    assert b.value == 3
    assert b.left is None
    assert b.right is None
    assert b.height == 1

    with pytest.raises(TypeError):
        b.left = BSTNode('a')
    with pytest.raises(TypeError):
        b.right = BSTNode('a')

    b.left = BSTNode(1)
    b.right = BSTNode(2)
    assert b.left.value == 1
    assert b.right.value ==2

    with pytest.raises(AttributeError):
        BSTNode(object())


def test_BST_construction():
    with pytest.raises(TypeError):
        BST(1)

    with pytest.raises(TypeError):
        BST("asg;lkj;lfkja")

    b = BST([5])
    assert b.root.value == 5

    b = BST([4, 3, 5])
    assert b.root.value == 4
    assert b.root.left.value == 3
    assert b.root.right.value == 5


def test_BST_find():
    b = BST(list(range(10)))

    assert b.find(5)
    assert not b.find(15)
    assert 5 in b
    assert 15 not in b
