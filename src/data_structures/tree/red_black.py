from data_structures.node import BaseNode
from .bst import BST


class RedBlackEmptyNode:

    def __init__(self):
        self.height = 0
        self.color = 0

    def __bool__(self):
        return False


class RedBlackNode(BaseNode):

    def __init__(self, value):
        super().__init__(value)
        self._left = RedBlackEmptyNode()
        self._right = RedBlackEmptyNode()
        self.height = 1
        self.color = 1

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, new_node):
        if isinstance(new_node, RedBlackNode):
            try:
                new_node < self
                self._left = new_node
            except TypeError:
                raise TypeError("A node and it's children must have comparable data types")
        elif new_node is None or isinstance(new_node, RedBlackEmptyNode):
            self._left = RedBlackEmptyNode()
        else:
            raise TypeError("The {0}.left must also be an instance of {0}".format(RedBlackNode))

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, new_node):
        if isinstance(new_node, RedBlackNode):
            try:
                new_node < self
                self._right = new_node
            except TypeError:
                raise TypeError("A node and it's children must have comparable data types")
        elif new_node is None or isinstance(new_node, RedBlackEmptyNode):
            self._right = RedBlackEmptyNode()
        else:
            raise TypeError("The {0}.right must also be an instance of {0}".format(RedBlackEmptyNode))

    def __repr__(self):
        """Returns the 'official' string representation of this node.

        This method's goal is to provide an unambiguous description of the object in question.
        """
        out = "BSTNode(value={}, ".format(self.value)
        out += "left=RedBlackNode({}), ".format(self.left.value) if self.left else "left=None, "
        out += "right=RedBlackNode({}))".format(self.right.value) if self.right else "right=None)"
        return out


class RedBlackTree(BST):

    def __init__(self, values):
        self._visited = []
        super().__init__(values)

    def insert(self, value):
        """Inserts the given value into the tree."""
        new_node = RedBlackNode(value)
        if not self.root:  # Fencepost if we have an empty tree.
            self.root = new_node
            self.root.color = 0
        else:
            self._insert(self.root, new_node)

    def _insert(self, current_node, new_node):
        self._visited.append(current_node)
        super()._insert(current_node, new_node)
        self.rebalance()

    def rebalance(self):





