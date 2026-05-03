from __future__ import annotations
from typing import List, Optional
from .bst import BST
from .node import TrialNode


class HyperparamRegistry:
    """
    High-level interface around BST for managing hyperparameter trials.
    Provides range queries, top-k retrieval, pruning, and summaries.
    """

    def __init__(self) -> None:
        self._bst = BST()
        self._history = []

    def add_trial(self, score: float, params: dict) -> None:
        score = round(score, 6)
        self._bst.insert(score, params)
        self._history.append({"score": score, "params": params})

    def best(self) -> Optional[TrialNode]:
        return self._bst.find_max()

    def worst(self) -> Optional[TrialNode]:
        return self._bst.find_min()

    def top_k(self, k: int) -> List[TrialNode]:
        result = []
        self._reverse_inorder(self._bst.root, result, k)
        return result

    def range_query(self, lo: float, hi: float) -> List[TrialNode]:
        result = []
        self._range(self._bst.root, lo, hi, result)
        return result

    def prune_below(self, threshold: float) -> int:
        to_delete = [n.score for n in self._bst.inorder()
                     if n.score < threshold]
        for score in to_delete:
            self._bst.delete(score)
        return len(to_delete)

    def all_trials(self) -> List[TrialNode]:
        return self._bst.inorder()

    def summary(self) -> dict:
        nodes = self._bst.inorder()
        if not nodes:
            return {}
        scores = [n.score for n in nodes]
        return {
            "count": len(nodes),
            "best_score": scores[-1],
            "worst_score": scores[0],
            "mean_score": round(sum(scores) / len(scores), 6),
            "tree_height": self._bst.height(),
            "is_balanced": self._bst.is_balanced(),
        }

    # ── Private helpers ───────────────────────────────────────────────────────

    def _reverse_inorder(self, node, result, k):
        """Right → Node → Left, stops when len(result) == k."""
        if node is None or len(result) == k:
            return
        self._reverse_inorder(node.right, result, k)
        if len(result) < k:
            result.append(node)
            self._reverse_inorder(node.left, result, k)

    def _range(self, node, lo, hi, result):
        if node is None:
            return
        if node.score > lo:
            self._range(node.left, lo, hi, result)
        if lo <= node.score <= hi:
            result.append(node)
        if node.score < hi:
            self._range(node.right, lo, hi, result)