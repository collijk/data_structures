from enum import Enum
from .bst import BST, EmptyBSTNode, BSTNode


class Color(Enum):
    Black = 0
    Red = 1


class EmptyRedBlackNode(EmptyBSTNode):

    def __init__(self):
        super().__init__()
        self.color = Color.Black

    def __repr__(self):
        return "EmptyRedBlackNode()"


class RedBlackNode(BSTNode):

    def __init__(self, value):
        super().__init__(value)
        self._left = EmptyRedBlackNode()
        self._right = EmptyRedBlackNode()
        self._color = Color.Red

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        if color in Color:
            self._color = color
        else:
            raise ValueError("Color must be one of {}".format([c for c in Color]))


    @staticmethod
    def _set_child(current_value, new_child):
        if isinstance(new_child, EmptyRedBlackNode) or new_child is None:
            return EmptyRedBlackNode()

        elif isinstance(new_child, RedBlackNode):
            try:
                _ = new_child.value < current_value
                return new_child
            except TypeError:
                raise TypeError("A node and it's children must have comparable data types")
        else:
            raise TypeError("Invalid Node type {}".format(new_child.__class__))

    def __repr__(self):
        out = "RedBlackNode(value={}, color={}, ".format(self.value, self.color.name)
        for child in ['left', 'right']:
            if getattr(self, child):
                node = getattr(self, child)
                out += "{}=RedBlackNode({}, {}), ".format(child, child.value, child.color.name)
            else:
                out += "{}=EmptyRedBlackNode({}), ".format
        return out[:-2] + ')'


class RedBlackTree(BST):

    def __init__(self, values):
        self._visited = []
        super().__init__(values)

    @staticmethod
    def _make_node(value):
        if value is not None:
            return RedBlackNode(value)
        return EmptyRedBlackNode()

    def insert(self, value):
        super().insert(value)
        if self.root.color is Color.Red:
            self.root.color = Color.Black
        else:
            self.rebalance(value)

    def _insert(self, current_node, new_node):
        self._visited.append(current_node)
        super()._insert(current_node, new_node)

    def remove(self, value):
        super().remove(value)
        self.rebalance(value)

    def _remove(self, value, parent_node, current_node):
        self._visited.append(parent_node)
        super()._remove(value, parent_node, current_node)

    def rebalance(self, value):
        parent = self._visited.pop()
        current_node = parent.left if value <= parent.value else parent.right

        while self._visited:
            if parent.color is Color.Black:  # We're done
                self._visited = []
                break

            grandparent = self._visited[-1]
            uncle = grandparent.right if parent <= grandparent else grandparent.left

            if uncle.color is Color.Red:  # Re-color case
                parent.color = Color.Black
                uncle.color = Color.Black
                grandparent.color = Color.Red

            else:  # Rotations

                if current_node is parent.left and parent is grandparent.left:
                    








    def right_rotate(self, node, parent):
        if parent is None:
            self.root = node.left
        elif parent.left is node:
            parent.left = node.left
        else:
            parent.right = node.left
        old_left = node.left
        node.left = old_left.right
        old_left.right = node

    def left_rotate(self, node, parent):
        if parent is None:
            self.root = node.right
        elif parent.left is node:
            parent.left = node.right
        else:
            parent.right = node.right
        old_right = node.right
        node.right = old_right.left
        old_right.left = node





