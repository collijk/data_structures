from .bst import BST


class AVLTree(BST):

    def __init__(self, values=()):
        self._visited = []
        super().__init__(values)

    def insert(self, value):
        super().insert(value)
        self.rebalance()

    def _insert(self, current_node, new_node):
        self._visited.append(current_node)
        super()._insert(current_node, new_node)

    def remove(self, value):
        super().remove(value)
        self.rebalance()

    def _remove(self, value, parent_node, current_node):
        self._visited.append(parent_node)
        super()._remove(value, parent_node, current_node)

    def rebalance(self):
        while self._visited:
            current_node = self._visited.pop()
            parent = self._visited[-1] if self._visited else None

            balance = current_node.right.height - current_node.left.height
            if balance > 1:  # double right heavy
                right_balance = current_node.right.right.height - current_node.right.left.height
                right_node = current_node.right
                if right_balance >= 0:
                    self.left_rotate(current_node, parent)
                    current_node.height = max(current_node.left.height, current_node.right.height) + 1
                    right_node.height = max(right_node.left.height, right_node.right.height) + 1
                else:
                    rl_node = right_node.left
                    self.right_rotate(current_node.right, current_node)
                    self.left_rotate(current_node, parent)
                    current_node.height = max(current_node.left.height, current_node.right.height) + 1
                    right_node.height = max(right_node.left.height, right_node.right.height) + 1
                    rl_node.height = max(rl_node.left.height, rl_node.right.height) + 1

            elif balance < -1:  # double left heavy
                left_balance = current_node.left.right.height - current_node.left.left.height
                left_node = current_node.left
                if left_balance <=0:
                    self.right_rotate(current_node, parent)
                    current_node.height = max(current_node.left.height, current_node.right.height) + 1
                    left_node.height = max(left_node.left.height, left_node.right.height) + 1
                else:
                    lr_node = left_node.right
                    self.left_rotate(current_node.left, current_node)
                    self.right_rotate(current_node, parent)
                    current_node.height = max(current_node.left.height, current_node.right.height) + 1
                    left_node.height = max(left_node.left.height, left_node.right.height) + 1
                    lr_node.height = max(lr_node.left.height, lr_node.right.height) + 1

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
