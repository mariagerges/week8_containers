from containers.BinaryTree import BinaryTree, Node
from containers.BST import BST


class AVLTree(BST):

    def __init__(self, xs=None):
        super().__init__(xs)

    def balance_factor(self):
        return AVLTree._balance_factor(self.root)

    @staticmethod
    def _balance_factor(node):
        if node is None:
            return 0
        return BinaryTree._height(node.left) - BinaryTree._height(node.right)

    def is_avl_satisfied(self):
        return AVLTree._is_avl_satisfied(self.root)

    @staticmethod
    def _is_avl_satisfied(node):
        result = True
        if node is None:
            return result
        if AVLTree._balance_factor(node) not in [-1, 0, 1]:
            result = False
        if node.left:
            result &= AVLTree._is_avl_satisfied(node.left)
        if node.right:
            result &= AVLTree._is_avl_satisfied(node.right)
        return result

    @staticmethod
    def _left_rotate(node):
        if node is None or node.right is None:
            return node
        new = Node(node.right.value)
        new.right = node.right.right
        new.left = Node(node.value)
        new.left.left = node.left
        if node.right.left:
            new.left.right = node.right.left
        return new

    @staticmethod
    def _right_rotate(node):
        if node is None or node.left is None:
            return node
        new = Node(node.left.value)
        new.left = node.left.left
        new.right = Node(node.value)
        new.right.right = node.right
        if node.left.right:
            new.right.left = node.left.right
        return new

    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        if value == self.root.value:
            return
        self.root = AVLTree._insert(self.root, value)

    @staticmethod
    def _insert(node, value):
        if value > node.value:
            if node.right:
                AVLTree._insert(node.right, value)
            else:
                node.right = Node(value)
        elif value < node.value:
            if node.left:
                AVLTree._insert(node.left, value)
            else:
                node.left = Node(value)
        if AVLTree._is_avl_satisfied(node):
            pass
        else:
            node.left = AVLTree._rebalance(node.left)
            node.right = AVLTree._rebalance(node.right)
            node = AVLTree._rebalance(node)
        return node

    @staticmethod
    def _rebalance(node):
        bf = AVLTree._balance_factor(node)
        if bf < -1:
            if AVLTree._balance_factor(node.right) > 0:
                new_node = AVLTree._right_rotate(node.right)
                node.right = new_node
                node = AVLTree._left_rotate(node)
            else:
                node = AVLTree._left_rotate(node)
            return node
        elif bf > 1:
            if AVLTree._balance_factor(node.left) < 0:
                new_node = AVLTree._left_rotate(node.left)
                node.left = new_node
                node = AVLTree._right_rotate(node)
            else:
                node = AVLTree._right_rotate(node)
            return node
        else:
            return node
