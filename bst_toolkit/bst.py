from __future__ import annotations
from collections import deque
from typing import Optional, List
from .node import TrialNode


class BST:
    """
    Binary Search Tree keyed by trial score.
    Left child < parent < right child (BST property).
    All operations are O(h) where h = tree height.
    """

    def __init__(self) -> None:
        self.root: Optional[TrialNode] = None
        self._size: int = 0

    # ── Public methods ────────────────────────────────────────────────────────

    def insert(self, score: float, params: dict) -> None:
        before = self._size
        self.root = self._insert(self.root, score, params)
        # _insert returns same root if duplicate — size only grows if new node
        if self._size == before:
            self._size += 1

    def delete(self, score: float) -> None:
        self.root, deleted = self._delete(self.root, score)
        if deleted:
            self._size -= 1

    def search(self, score: float) -> Optional[TrialNode]:
        return self._search(self.root, score)

    def find_min(self) -> Optional[TrialNode]:
        if self.root is None:
            return None
        return self._find_min(self.root)

    def find_max(self) -> Optional[TrialNode]:
        node = self.root
        if node is None:
            return None
        while node.right is not None:
            node = node.right
        return node

    def height(self) -> int:
        return self._height(self.root)

    def is_balanced(self) -> bool:
        return self._check_balanced(self.root) != -1

    def __len__(self) -> int:
        return self._size

    # ── Traversals ────────────────────────────────────────────────────────────

    def inorder(self) -> List[TrialNode]:
        """Left → Node → Right. Returns nodes sorted ascending by score."""
        result = []
        self._inorder(self.root, result)
        return result

    def preorder(self) -> List[TrialNode]:
        """Node → Left → Right. Root comes first."""
        result = []
        self._preorder(self.root, result)
        return result

    def postorder(self) -> List[TrialNode]:
        """Left → Right → Node. Root comes last."""
        result = []
        self._postorder(self.root, result)
        return result

    def level_order(self) -> List[List[TrialNode]]:
        """Breadth-first, level by level. Uses a deque, not recursion."""
        if self.root is None:
            return []
        result = []
        queue = deque([self.root])
        while queue:
            level_size = len(queue)
            level = []
            for _ in range(level_size):
                node = queue.popleft()
                level.append(node)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)
        return result

    # ── Private helpers ───────────────────────────────────────────────────────

    def _insert(self, node, score, params):
        if node is None:
            return TrialNode(score=score, params=params)
        if score < node.score:
            node.left = self._insert(node.left, score, params)
        elif score > node.score:
            node.right = self._insert(node.right, score, params)
        # score == node.score → duplicate, do nothing (first-inserted wins)
        else:
            self._size += 1  # cancel the +1 insert() will add
        return node

    def _delete(self, node, score):
        if node is None:
            return node, False
        if score < node.score:
            node.left, deleted = self._delete(node.left, score)
        elif score > node.score:
            node.right, deleted = self._delete(node.right, score)
        else:
            # Found it — three cases
            deleted = True
            if node.left is None:          # case 0 or 1 child (no left)
                return node.right, deleted
            if node.right is None:         # case 1 child (no right)
                return node.left, deleted
            # case 2 children: replace with in-order successor (min of right)
            successor = self._find_min(node.right)
            node.score = successor.score
            node.params = successor.params
            node.right, _ = self._delete(node.right, successor.score)
        return node, deleted

    def _search(self, node, score):
        if node is None or node.score == score:
            return node
        if score < node.score:
            return self._search(node.left, score)
        return self._search(node.right, score)

    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def _check_balanced(self, node):
        """Returns height if balanced, -1 if not."""
        if node is None:
            return 0
        left_h = self._check_balanced(node.left)
        if left_h == -1:
            return -1
        right_h = self._check_balanced(node.right)
        if right_h == -1:
            return -1
        if abs(left_h - right_h) > 1:
            return -1
        return 1 + max(left_h, right_h)

    def _inorder(self, node, result):
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node)
        self._inorder(node.right, result)

    def _preorder(self, node, result):
        if node is None:
            return
        result.append(node)
        self._preorder(node.left, result)
        self._preorder(node.right, result)

    def _postorder(self, node, result):
        if node is None:
            return
        self._postorder(node.left, result)
        self._postorder(node.right, result)
        result.append(node)