"""A python linked list implementation."""
from typing import Iterable

from data_structures.node import BaseNode


class LinkedListNode(BaseNode):
    """A node for use in linked lists.

    While this node is usable with arbitrary data values, it also implements rich comparison operators
    which allow for easy comparison with other nodes which carry comparable value data types.

    Attributes
    ----------
    value : Any
        The data this node holds.
    """
    def __init__(self, value):
        """The constructor for the LinkedListNode.

        Parameters
        ----------
        value : Any
           The data this node will hold after initialization.
        """
        super().__init__(value)
        self._next_node = None

    @property
    def next_node(self):
        """A reference to the next node in the linked list, if one exists.

        Properties are used in lieu of getters and setters in `Python` to provide
        custom implementation where necessary.  Here, we've made next_node a property
        so that we can ensure that only other LinkedListNode objects are set.
        """
        return self._next_node

    @next_node.setter
    def next_node(self, new_node):
        """Sets the value of the this node's next node pointer.

        Parameters
        ----------
        new_node : Optional[LinkedListNode]
            The new node to point this node at.

        Raises
        ------
        TypeError :
            If the new_node is not a LinkedListNode or None.
        """
        if isinstance(new_node, LinkedListNode) or new_node is None:
            self._next_node = new_node
        else:
            raise TypeError("The {0}.next_node must also be an instance of {0}".format(LinkedListNode))

    def __str__(self):
        """The informal representation of this node.

        This method is called via `str` or `print` and should provide a human readable representation of the object.
        """
        if self.next_node:
            return "[{} | -]-->".format(self.value, self.next_node.value)
        else:
            return "[{} | -]--> None".format(self.value)

    def __repr__(self):
        """Returns the 'official' string representation of this node.

        This method's goal is to provide an unambiguous description of the object in question.
        """
        if self.next_node:
            return "LinkedListNode(value={}, next_node=LinkedListNode({}))".format(self.value, self.next_node.value)
        else:
            return "LinkedListNode(value={}, next_node=None)".format(self.value)


class LinkedList:
    """A singly linked list."""
    def __init__(self, values=()):
        """The constructor for this LinkedList

        Parameters
        ----------
        values : Optional[Sequence]
            A list, tuple, or set of values to initialize this LinkedList with.
        """
        self._head = None

        if isinstance(values, Iterable) and values:
            # Coerce to a list, in case of a weird container type (this makes sure it's iterable).
            values = list(values)
            # Since we have some values, fencepost.
            # Set the head node to a new list and create a generic node pointer that we can advance.
            self.head = LinkedListNode(values[0])
            current_node = self.head
            # Loop through the remaining values.
            for v in values[1:]:
                # Construct a new node for each value.
                current_node.next_node = LinkedListNode(v)
                # And advance our generic node pointer.
                current_node = current_node.next_node
        elif isinstance(values, Iterable):
            pass  # We didn't get passed anything, construct an empty LinkedList
        else:
            raise TypeError("{} object is not iterable".format(values))

    @property
    def head(self):
        """A reference to the first node in this linked list, if one exists."""
        return self._head

    @head.setter
    def head(self, new_node):
        if isinstance(new_node, LinkedListNode) or new_node is None:
            self._head = new_node
        else:
            raise TypeError("The head value of a LinkedList may only be a LinkedListNode or None")

    def _get(self, index):
        """This is a 'private' method for getting the LinkedListNode at a particular index."""
        if not isinstance(index, int):
            raise IndexError("{} is not a valid index".format(index))
        if index >= len(self) or index < 0:
            raise IndexError("Valid indices are in the range 0:{}, inclusive. "
                             "You requested {}".format(len(self) - 1, index))

        node = self.head
        for i in range(index):
            node = node.next_node

        return node

    def insert(self, index, value):
        """Inserts a value at the given index into the linked list.

        Parameters
        ----------
        index : int
            The index to construct the new node at.
        value : Any
            The value to construct the new node with.

        Raises
        ------
        IndexError :
            If the given index is not an integer or is outside the range of the linked list indices [0 to len(self)]
        """
        if not isinstance(index, int):
            raise IndexError("{} is not a valid index".format(index))

        if index:
            # Grab the immediately preceding node.
            previous = self._get(index - 1)
            # Construct a new node and set its next node pointer to what the preceding node was pointing at.
            new_node = LinkedListNode(value)
            new_node.next_node = previous.next_node
            # Finally, set the preceding node's next pointer to point at the newly constructed node.
            previous.next_node = new_node
        else:  # We want to insert at the head
            new_node = LinkedListNode(value)
            new_node.next_node = self.head
            self.head = new_node

    def append(self, value):
        """Appends a value to the end of the list

        Parameters
        ----------
        value : Any
            Value to append
        """
        self.insert(len(self), value)

    def pop(self, index=None):
        """Removes a node at the given index and returns its value.

        Parameters
        ----------
        index : int
            The index of the node to be removed.

        Raises
        ------
        IndexError :
            If the given index is not an integer or is outside the range of the linked list indices [0 to len(self)]
        """
        #
        if index is None:
            return self.pop(0)
        elif not isinstance(index, int):
            raise IndexError("{} is not a valid index".format(index))

        if not index:  # We want to pop the first value.
            node = self._get(0)
            self.head = node.next_node
            return node.value

        # Otherwise normal operations.
        # Grab the immediately preceding node.
        previous = self._get(index - 1)

        # Two cases: Either the immediately preceding node has a next_node value
        if previous.next_node:
            # In which case, grab it
            node = previous.next_node
            # Set the previous node's next pointer to point at the grabbed nodes next node (even if it is None)
            previous.next_node = node.next_node
            # Then return the grabbed node's value
            return node.value
        else:
            # Otherwise we're off by exactly one
            raise IndexError("You requested an index value one larger than the length of the LinkedList.")

    def print_list(self):
        """Prints out the value of each node in the linked list."""
        for value in self:
            print(value)

    def reverse(self):
        """Reverses the order of the nodes in place."""
        # Grab a reusable reference to the 'previous' node
        previous_node = self.head
        # But check to make sure if it's valid
        if previous_node:
            # If so, grab a reference to the next node and call it the current one.
            current_node = previous_node.next_node
        else:
            # Otherwise our list is empty and we're done.
            return

        # Now, if our list has more than one node, we need to traverse it.
        # While we have a reference to the current node,
        while current_node:
            # Grab a reference to the next one in line so we don't lose it.
            temp = current_node.next_node
            # Reset the current node's pointer to point back at the previous node.
            current_node.next_node = previous_node
            # We're now done with the previous node, so advance its pointer up one.
            previous_node = current_node
            # Then move our current node pointer up one as well.
            current_node = temp

        # Finally, deal with the head node, which is now our tail, so point it at nothing.
        self.head.next_node = None
        # previous_node is holding on to our new head node, so set it.
        self.head = previous_node

    def count(self, value):
        """Counts the number of nodes in the list whose value is equal to the given value.

        Parameters
        ----------
        value : Any
            The value to check for in the nodes of the list.

        Returns
        -------
        int :
            The number of nodes whose value is equal to the given value.
        """
        count = 0
        for val in self:
            if val == value:
                count += 1
        return count

    def index(self, value):
        """Returns the lowest index for of the first item in the linked list whose value is equal to the given value.

        Parameters
        ---------
        value : Any
            The value we want to find the index of.

        Returns
        -------
        int :
            The lowest zero-based index of the given value in the LinkedList, if present.

        Raises
        ------
        ValueError :
            If the given value is not present in the LinkedList
        """
        for idx, val in enumerate(self):
            if val == value:
                return idx
        raise ValueError('{} is not present in the LinkedList'.format(value))

    def extend(self, other):
        """Appends the given iterable to the current LinkedList in place."""
        tail = self._get(len(self) - 1)
        tail.next_node = LinkedList(other).head

    def sorted(self, method='bubble_sort'):
        if method == 'bubble_sort':
            self._bubble_sort()
        elif method == 'insertion_sort':
            self._insertion_sort()
        else:
            raise NotImplementedError()

    def _bubble_sort(self):
        if len(self) <= 1:
            return

        swaps_this_iteration = True
        while swaps_this_iteration:
            swaps_this_iteration = False

            previous = self.head
            current = previous.next_node

            if previous > current:
                self.head = current
                previous.next_node = current.next_node
                current.next_node = previous
                previous, current = current, previous
                swaps_this_iteration = True

            while current.next_node:

                if current > current.next_node:
                    previous.next_node = current.next_node
                    current.next_node = current.next_node.next_node
                    previous.next_node.next_node = current
                    previous = previous.next_node
                    swaps_this_iteration = True
                else:
                    previous = current
                    current = current.next_node

    def _insertion_sort(self):
        length = len(self)

        if length <= 1:
            return

        previous = self.head
        current = previous.next_node

        while current:
            if current >= previous:  # No swaps, just advance. O(n) for already sorted lists.
                previous, current = current, current.next_node

            elif current < self.head:  # Special case, insert at head
                previous.next_node = current.next_node
                current.next_node = self.head
                self.head = current
                current = previous.next_node

            else:  # General case, insert between head and previous, exclusive
                previous.next_node = current.next_node
                comparison_node = self.head
                insertion_point_found = False

                while not insertion_point_found:
                    if current < comparison_node.next_node:
                        insertion_point_found = True
                    else:
                        comparison_node = comparison_node.next_node

                current.next_node = comparison_node.next_node
                comparison_node.next_node = current
                current = previous.next_node

    def __len__(self):
        count = 0
        node = self.head
        while node:
            count += 1
            node = node.next_node
        return count

    def __iter__(self):
        node = self.head
        while node:
            yield node.value
            node = node.next_node

    def __contains__(self, value):
        for v in self:
            if v == value:
                return True
        return False

    def __add__(self, other):
        if isinstance(other, Iterable):
            return LinkedList([value for value in self] + [value for value in other])
        raise ValueError("Can only concatenate a LinkedList with another Iterable container-type.")

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __mul__(self, value):
        if isinstance(value, int):
            return LinkedList([value for value in self]*value)
        raise ValueError("Multiplication with a LinkedList is only supported for integers")

    def __rmul__(self, value):
        return self.__mul__(value)

    def __imul__(self, value):
        return self.__mul__(value)

    def __repr__(self):
        current_node = self.head
        out = 'LinkedList('
        while current_node:
            out += str(current_node.value) + ', '
            current_node = current_node.next_node
        out += ')'
        return out
