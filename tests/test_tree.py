import random

import pytest

from data_structures.tree import BSTNode, BST, EmptyNode, AVLTree

@pytest.fixture(params=[0, 10, 50, 100])
def AVL(request):
    return AVLTree([random.randint(0, 100) for i in range(request.param)])

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
    assert b.right.value == 2


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


def test_BST_height():
    b = BST([random.randint(0, 50) for i in range(50)])

    to_check = [b.root]
    while to_check:
        node = to_check.pop()
        if node.left:
            to_check.append(node.left)
            left_height = node.left.height
        else:
            left_height = 0
        if node.right:
            to_check.append(node.right)
            right_height = node.right.height
        else:
            right_height = 0
        assert node.height == max(left_height, right_height) + 1


def is_BST(node):
    if not node:
        return True
    else:
        left = node.left <= node if node.left else True
        right = node.right > node if node.right else True
        return left and right and is_BST(node.left) and is_BST(node.right)


def is_AVL(node):
    if not is_BST(node):
        return False

    def _is_AVL(n):
        if isinstance(n, EmptyNode) or n is None:
            return True
        return abs(n.left.height - n.right.height) <= 1 and _is_AVL(n.left) and _is_AVL(n.right)
    return _is_AVL(node)


def test_AVLTree(AVL):
    assert is_AVL(AVL.root)
