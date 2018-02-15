"""An implementation of a data structure `Node` for use in linked data structures."""


class BaseNode:
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __bool__(self):
        # A node, empty or not, is truthy
        return True

    def __repr__(self):
        return "BaseNode(value={})".format(self.value)


class EmptyNode:

    def __bool__(self):
        return False

    def __repr__(self):
        return "EmptyNode()"
