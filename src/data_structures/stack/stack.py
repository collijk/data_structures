

class Stack:

    def __init__(self, maxsize=50):
        self._storage = []
        self._maxsize = maxsize

    def peek(self):
        if not len(self._storage):
            raise LookupError("Nothing to peek. Stack is empty")
        return self._storage[-1]

    def pop(self):
        if not len(self._storage):
            raise LookupError("Nothing to pop. Stack is empty")
        return self._storage.pop()

    def push(self, value):
        if len(self._storage) == self._maxsize:
            raise OverflowError(f'Stack trying to exceed max size of {self._maxsize}')
        self._storage.append(value)

    def __len__(self):
        return len(self._storage)


def parentheses_balanced(expression):
    s = Stack(maxsize=len(expression))

    pairs = {
        ')': '(',
        '}': '{',
        ']': '[',
    }

    def pair_on_top_of_stack(char):
        return char in pairs.keys() and len(s) and s.peek() == pairs[char]

    for char in expression:
        if char in pairs.values():
            s.push(char)
        elif pair_on_top_of_stack(char):
            s.pop()
        else:
            return False

    return True
