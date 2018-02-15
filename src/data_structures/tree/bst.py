from typing import Iterable, Union
from collections import deque

from data_structures import BaseNode, EmptyNode


class EmptyBSTNode(EmptyNode):

    def __init__(self):
        super().__init__()
        self.height = 0

    def __repr__(self):
        return "EmptyBSTNode()"


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
        super().__init__(value)
        self._left = EmptyBSTNode()
        self._right = EmptyBSTNode()
        self.height = 1

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, new_node):
        self._left = self._set_child(self.value, new_node)

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, new_node):
        self._right = self._set_child(self.value, new_node)

    @staticmethod
    def _set_child(current_value, new_child):
        if isinstance(new_child, EmptyBSTNode) or new_child is None:
            return EmptyBSTNode()

        if isinstance(new_child, BSTNode):
            try:
                _ = new_child.value < current_value
                return new_child
            except TypeError:
                raise TypeError("A node and it's children must have comparable data types")

        raise TypeError("Invalid Node type {}".format(new_child.__class__))

    def __repr__(self):
        """Returns the 'official' string representation of this node.

        This method's goal is to provide an unambiguous description of the object in question.
        """
        out = "BSTNode(value={}, ".format(self.value)
        for child in ['left', 'right']:
            if getattr(self, child):
                out += "{}=BSTNode({}), ".format(child, getattr(self, child).value)
            else:
                out += "{}=EmptyNode()"
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
        self.root = self._make_node(None)

        if isinstance(values, Iterable) and not isinstance(values, str):
            for v in values:
                self.insert(v)
        else:
            raise TypeError("{} object is not iterable".format(values))

    @staticmethod
    def _make_node(value):
        if value is not None:
            return BSTNode(value)
        return EmptyNode()

    def insert(self, value):
        """Inserts the given value into the tree."""
        new_node = self._make_node(value)
        if not self.root:  # Fencepost if we have an empty tree.
            self.root = new_node
        else:
            self._insert(self.root, new_node)

    def _insert(self, current_node, new_node):
        if new_node <= current_node:
            if not current_node.left:
                current_node.left = new_node
            else:
                self._insert(current_node.left, new_node)
        else:
            if not current_node.right:
                current_node.right = new_node
            else:
                self._insert(current_node.right, new_node)

        current_node.height = max(current_node.left.height, current_node.right.height) + 1

    def remove(self, value):
        if value == self.root.value:
            if not self.root.left and not self.root.right:
                self.root = None
            elif not self.root.left:
                self.root = self.root.right
            elif not self.root.right:
                self.root = self.root.left
            else:
                max_value = self._get_max(self.root.left).value
                self.root.value = max_value
                self._remove(max_value, self.root, self.root.left)

    def _remove(self, value, parent_node, current_node):
        if not current_node:
            raise LookupError(f"Value {value} is not in the tree.")

        elif current_node.value == value:
            if not current_node.left and not current_node.right:
                if current_node is parent_node.left:
                    parent_node.left = self._make_node(None)
                elif current_node is parent_node.right:
                    parent_node.right = self._make_node(None)

            # Case 2: Only right child
            elif not current_node.left:
                if current_node is parent_node.left:
                    parent_node.left = current_node.right
                elif current_node is parent_node.right:
                    parent_node.right = current_node.right

            # Case 3: Only left child
            elif not current_node.right:
                if current_node is parent_node.left:
                    parent_node.left = current_node.left
                elif current_node is parent_node.right:
                    parent_node.right = current_node.left

            # Case 4: Both children
            else:
                max_value = self._get_max(current_node.left).value
                current_node.value = max_value
                self._remove(max_value, current_node, current_node.left)

        elif value <= current_node.value:
            self._remove(value, current_node, current_node.left)

        else:  # value > current_node.value
            self._remove(value, current_node, current_node.right)

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

    def minimum(self):
        min_node = self._get_min(self.root)
        return min_node.value

    def _get_min(self, node):
        if not node.left:
            return node
        return self._get_min(node.left)

    def maximum(self):
        max_node = self._get_max(self.root)
        return max_node.value

    def _get_max(self, node):
        if not node.right:
            return node
        return self._get_max(node.right)

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
        if not self.root:
            return ''
        return self._old_repr()

    def _old_repr(self):
        em_dash = '\u2014'
        blank_char = ' '

        max_depth = min(5, self.root.height)
        value_width = 3  # Must be odd.
        node_width = value_width + 2  # Add space for parentheses
        print_width = (node_width + 1) * 2 ** (max_depth - 1) - 1
        center = print_width // 2 + 1

        level = [self.root]

        out = ""
        for i in range(max_depth):
            next_level = []
            for n in level:
                if n:
                    next_level.extend([n.left, n.right])
                else:
                    next_level.extend([None, None])
            end_width = center // 2 ** i - (node_width // 2 + 1)
            end_space = blank_char * end_width
            interstitial_width = (print_width - 2 * end_width - node_width * len(level)) // (len(level) - 1) if len(
                level) > 1 else 0
            interstitial_space = blank_char * interstitial_width
            out += end_space
            out += interstitial_space.join(
                [f'({node.value: ^3})' if node else blank_char * node_width for node in level])
            out += end_space + '\n'

            out += end_space
            for n in level:
                if n:
                    if n.left:
                        out += blank_char * (node_width // 2 - 1) + '/' + blank_char
                    else:
                        out += blank_char * (node_width // 2 + 1)
                    if n.right:
                        out += '\\' + blank_char * (node_width // 2 - 1)
                    else:
                        out += blank_char * (node_width // 2)
                else:
                    out += blank_char * node_width
                out += interstitial_space
            out = out[:-interstitial_width] if interstitial_width else out
            out += end_space + '\n'

            if i == max_depth - 1:
                break

            next_end_width = center // 2 ** (i + 1) - (node_width // 2 + 1)
            dash_end_width = next_end_width + node_width // 2 + 1
            next_interstitial_width = (print_width - 2 * next_end_width - node_width * len(next_level)) // (
            len(next_level) - 1)
            dash_width = (next_interstitial_width + 2 * (node_width // 2) - 3) // 2
            dash_interstitial_width = interstitial_width - 2 * (dash_width - node_width // 2 + 1)
            out += blank_char * dash_end_width
            for n in level:
                if n:
                    if n.left:
                        out += em_dash * dash_width + blank_char * 3
                    else:
                        out += blank_char * (3 + dash_width)
                    if n.right:
                        out += em_dash * dash_width
                    else:
                        out += blank_char * dash_width
                    out += blank_char * dash_interstitial_width
                else:
                    out += blank_char * (2 * dash_width + 3 + dash_interstitial_width)
            out = out[:-dash_interstitial_width] if interstitial_width else out
            out += blank_char * dash_end_width + '\n'

            out += blank_char * (next_end_width + node_width // 2)
            for n in level:
                if n:
                    out += '/' if n.left else blank_char
                    out += blank_char * (next_interstitial_width + 2 * (node_width // 2))
                    out += '\\' if n.right else blank_char
                    out += blank_char * (next_interstitial_width + 2 * (node_width // 2))
                else:
                    out += blank_char * 2 * (next_interstitial_width + 2 * (node_width // 2) + 1)
            out = out[:-(next_interstitial_width + 2 * (node_width // 2))]
            out += blank_char * (next_end_width + node_width // 2) + '\n'

            level = next_level

        return out[:-1]


    # Doing some stuff to clean up the repr.  Not done though.
    def _build_repr(self, node: Union[BSTNode, EmptyBSTNode], remaining_levels: int):
        em_dash = '\u2014'
        blank_char = ' '

        out = self._make_node_string(node, blank_char)

        if node:
            left = self._build_repr(node.left, remaining_levels - 1)
            right = self._build_repr(node.right, remaining_levels - 1)
        else: # Probably don't want to pass the node itself.  Maybe none.
            left = self._build_repr(node, remaining_levels - 1)
            right = self._build_repr(node, remaining_levels - 1)

        child_padding = ((len(left[0]) - 1) // 2) * blank_char

        if node.left:
            mid_line = [child_padding + blank_char + em_dash * (len(left[0]) - len(child_padding) - 1)]
            in_line = [child_padding + '/' + child_padding]
            left = mid_line + in_line + left
        else:
            left = [blank_char * len(left[0]), blank_char * len(left[0])] + left

        if node.right:
            mid_line = [em_dash * (len(right[0]) - len(child_padding) - 1) + blank_char + child_padding]
            in_line = [child_padding + '\\' + child_padding]
            right = mid_line + in_line + right
        else:
            right = [blank_char * len(right[0]), blank_char * len(right[0])] + right

        base = [blank_char.join([l, r]) for l, r in zip(left, right)]

        width = len(base[0])
        padding = ((width - len(out[0])) // 2) * blank_char

        out = [padding + l + padding for l in out] + base

        return out

    def _make_node_string(self, node: Optional[BSTNode], blank_char: str):
        value_width = 3  # Must be odd.
        node_width = value_width + 2  # Add space for parentheses

        empty_template = blank_char * node_width
        node_template = '{{:{0}^{1}}}'.format(blank_char, value_width)

        if node:
            out = [node_template.format(node.value)]
            temp = ''
            padding = ((node_width - 3) // 2) * blank_char
            if node.left:
                temp += '{0}/{1}'.format(padding, blank_char)
            else:
                temp += padding + 2 * blank_char
            if node.right:
                temp += '\\{}'.format(padding)
            else:
                temp += blank_char + padding
            out.append(temp)
        else:
            out = [empty_template, empty_template]
        return out
