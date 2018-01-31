from typing import Iterable
from collections import deque

from data_structures.node import BaseNode


class BSTNode(BaseNode):
    """A node for use in binary search trees.

    While this node is usable with arbitrary data values, it also implements rich comparison operators
    which allow for easy comparison with other nodes which carry comparable value data types.

    Attributes
    ----------
    value : Any
        The data this node holds.
    """
    def __init__(self, value):
        """The constructor for the BSTNode.

        Parameters
        ----------
        value : Any
           The data this node will hold after initialization.
        """
        if not hasattr(value, '__le__'):
            raise AttributeError('BSTNode values must be comparable.')
        super().__init__(value)
        self._left = None
        self._right = None
        self.height = 1

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, new_node):
        if isinstance(new_node, BSTNode) or new_node is None:
            self._left = new_node
        else:
            raise TypeError("The {0}.left must also be an instance of {0}".format(BSTNode))

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, new_node):
        if isinstance(new_node, BSTNode) or new_node is None:
            self._right = new_node
        else:
            raise TypeError("The {0}.right must also be an instance of {0}".format(BSTNode))

    def __repr__(self):
        """Returns the 'official' string representation of this node.

        This method's goal is to provide an unambiguous description of the object in question.
        """
        out = "BSTNode(value={}, ".format(self.value)
        out += "left=BSTNode({}), ".format(self.left.value) if self.left else "left=None, "
        out += "right=BSTNode({}))".format(self.right.value) if self.right else "right=None)"
        return out


class BST:
    """A naive binary search tree."""
    def __init__(self, values=()):
        """BST constructor.

        Parameters
        ----------
        values : Iterable
            A list of values to initialize the BST with.  Values will be inserted in the order provided.
        """
        self.root = None

        if isinstance(values, Iterable) and not isinstance(values, str):
            for v in values:
                self.insert(v)
        else:
            raise TypeError("{} object is not iterable".format(values))

    def insert(self, value):
        """Inserts the given value into the tree."""
        new_node = BSTNode(value)
        if not self.root:  # Fencepost if we have an empty tree.
            self.root = new_node
        else:
            self._insert(self.root, new_node)

    def _insert(self, current_node, new_node):
        if new_node <= current_node:
            if not current_node.left:
                current_node.left = new_node
                height_adjustment = not bool(current_node.right)
            else:
                height_adjustment = self._insert(current_node.left, new_node)
        else:
            if not current_node.right:
                current_node.right = new_node
                height_adjustment = not bool(current_node.left)
            else:
                height_adjustment = self._insert(current_node.right, new_node)

        current_node.height += height_adjustment
        return height_adjustment

    def find(self, value):
        """Returns True if the value is contained in the tree and False otherwise."""
        return self._find(self.root, value)

    def __contains__(self, value):
        """Support for `value in tree`."""
        return self._find(self.root, value)

    def _find(self, node, value):
        if value == node.value:
            return True
        if value < node.value and node.left:
            return self._find(node.left, value)
        if value > node.value and node.right:
            return self._find(node.right, value)
        return False

    def get_height(self):
        """Returns the height of the tree."""
        return self.root.height

    def to_list(self, order='in_order'):
        orders = {'pre_order': ['append', 'left', 'right'],
                  'in_order': ['left', 'append', 'right'],
                  'post_order': ['left', 'right', 'append']}
        if order == 'level_order':
            return self._to_list_level_order()
        elif order in orders:
            return self._to_list(self.root, [], orders[order])
        else:
            raise ValueError('You specified the invalid ordering {}'.format(order))

    def _to_list(self, node, current_list, order):
        functions = {'append': lambda n, l, o: l + [n.value],
                     'left': lambda n, l, o: self._to_list(n.left, l, o) if n.left else l,
                     'right': lambda n, l, o: self._to_list(n.right, l, o) if n.right else l}
        for operation in order:
            current_list = functions[operation](node, current_list, order)
        return current_list

    def _to_list_level_order(self):
        queue = deque([self.root])
        out = []
        while queue:
            current = queue.popleft()
            if not current:
                continue
            queue.extend([current.left, current.right])
            out.append(current.value)
        return out

    def __repr__(self):
        em_dash = '\u2014'
        max_depth = min(5, self.root.height - 1)
        value_width = 3  # Must be odd.
        node_width = value_width + 2  # Add space for parentheses
        print_width = (node_width + 1) * 2**(max_depth - 1) - 1
        center = print_width // 2 + 1
        level = [self.root]
        blank_char = ' '
        out = ""
        for i in range(max_depth):
            next_level = []
            for n in level:
                if n:
                    next_level.extend([n.left, n.right])
                else:
                    next_level.extend([None, None])
            end_width = center // 2**i - (node_width // 2 + 1)
            end_space = blank_char*end_width
            interstitial_width = (print_width - 2*end_width - node_width*len(level)) // (len(level) - 1) if len(level) > 1 else 0
            interstitial_space = blank_char*interstitial_width
            out += end_space
            out += interstitial_space.join([f'({node.value: ^3})' if node else blank_char*node_width for node in level])
            out += end_space + '\n'

            out += end_space
            for n in level:
                if n:
                    if n.left:
                        out += blank_char*(node_width // 2 - 1) + '/' + blank_char
                    else:
                        out += blank_char*(node_width // 2 + 1)
                    if n.right:
                        out += '\\' + blank_char*(node_width // 2 - 1)
                    else:
                        out += blank_char*(node_width // 2)
                else:
                    out += blank_char*node_width
                out += interstitial_space
            out = out[:-interstitial_width] if interstitial_width else out
            out += end_space + '\n'

            if i == max_depth - 1:
                break

            next_end_width = center // 2**(i + 1) - (node_width // 2 + 1)
            dash_end_width = next_end_width + node_width//2 + 1
            next_interstitial_width = (print_width - 2*next_end_width - node_width*len(next_level)) // (len(next_level) - 1)
            dash_width = (next_interstitial_width + 2 * (node_width // 2) - 3) // 2
            dash_interstitial_width = interstitial_width - 2*(dash_width - node_width // 2 + 1)
            out += blank_char*dash_end_width
            for n in level:
                if n:
                    if n.left:
                        out += em_dash*dash_width + blank_char*3
                    else:
                        out += blank_char*(3 + dash_width)
                    if n.right:
                        out += em_dash*dash_width
                    else:
                        out += blank_char*dash_width
                    out += blank_char*dash_interstitial_width
                else:
                    out += blank_char*(2*dash_width + 3 + dash_interstitial_width)
            out = out[:-dash_interstitial_width] if interstitial_width else out
            out += blank_char*dash_end_width + '\n'

            out += blank_char*(next_end_width + node_width//2)
            for n in level:
                if n:
                    out += '/' if n.left else blank_char
                    out += blank_char*(next_interstitial_width + 2*(node_width//2))
                    out += '\\' if n.right else blank_char
                    out += blank_char*(next_interstitial_width + 2*(node_width//2))
                else:
                    out += blank_char*2*(next_interstitial_width + 2*(node_width//2) + 1)
            out = out[:-(next_interstitial_width + 2*(node_width//2))]
            out += blank_char*(next_end_width + node_width//2) + '\n'

            level = next_level

        return out[:-1]
