from collections import deque
from typing import List, Optional
from .node import TrialNode


class BST:
    def __init__(self) -> None:
        self.root: Optional[TrialNode] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    # ------------------------------------------------------------------ insert
    def insert(self, score: float, params: dict) -> None:
        if self.root is None:
            self.root = TrialNode(score, params)
            self._size += 1
        else:
            if self._insert(self.root, score, params):
                self._size += 1

    def _insert(self, node: TrialNode, score: float, params: dict) -> bool:
        if score == node.score:
            return False
        if score < node.score:
            if node.left is None:
                node.left = TrialNode(score, params)
                return True
            return self._insert(node.left, score, params)
        else:
            if node.right is None:
                node.right = TrialNode(score, params)
                return True
            return self._insert(node.right, score, params)

    # ------------------------------------------------------------------ search
    def search(self, score: float) -> Optional[TrialNode]:
        return self._search(self.root, score)

    def _search(self, node: Optional[TrialNode], score: float) -> Optional[TrialNode]:
        if node is None or node.score == score:
            return node
        if score < node.score:
            return self._search(node.left, score)
        return self._search(node.right, score)

    # ------------------------------------------------------------------ delete
    def delete(self, score: float) -> None:
        self.root, deleted = self._delete(self.root, score)
        if deleted:
            self._size -= 1

    def _delete(self, node: Optional[TrialNode], score: float):
        if node is None:
            return node, False
        deleted = False
        if score < node.score:
            node.left, deleted = self._delete(node.left, score)
        elif score > node.score:
            node.right, deleted = self._delete(node.right, score)
        else:
            deleted = True
            if node.left is None:
                return node.right, deleted
            if node.right is None:
                return node.left, deleted
            successor = self._min_node(node.right)
            node.score, node.params = successor.score, successor.params
            node.right, _ = self._delete(node.right, successor.score)
        return node, deleted

    # ----------------------------------------------------------------- min/max
    def find_min(self) -> Optional[TrialNode]:
        return self._min_node(self.root)

    def find_max(self) -> Optional[TrialNode]:
        return self._max_node(self.root)

    def _min_node(self, node: Optional[TrialNode]) -> Optional[TrialNode]:
        if node is None or node.left is None:
            return node
        return self._min_node(node.left)

    def _max_node(self, node: Optional[TrialNode]) -> Optional[TrialNode]:
        if node is None or node.right is None:
            return node
        return self._max_node(node.right)

    # ------------------------------------------------------------------ height
    def height(self) -> int:
        return self._height(self.root)

    def _height(self, node: Optional[TrialNode]) -> int:
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    # --------------------------------------------------------------- balanced?
    def is_balanced(self) -> bool:
        return self._check_balanced(self.root) != -1

    def _check_balanced(self, node: Optional[TrialNode]) -> int:
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

    # ------------------------------------------------------------ traversals
    def inorder(self) -> List[TrialNode]:
        result: List[TrialNode] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[TrialNode], result: list) -> None:
        if node:
            self._inorder(node.left, result)
            result.append(node)
            self._inorder(node.right, result)

    def preorder(self) -> List[TrialNode]:
        result: List[TrialNode] = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node: Optional[TrialNode], result: list) -> None:
        if node:
            result.append(node)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self) -> List[TrialNode]:
        result: List[TrialNode] = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node: Optional[TrialNode], result: list) -> None:
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node)

    def level_order(self) -> List[List[TrialNode]]:
        if self.root is None:
            return []
        levels: List[List[TrialNode]] = []
        queue = deque([self.root])
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            levels.append(level)
        return levels
