from typing import Any, Dict, List, Optional
from .bst import BST
from .node import TrialNode


class HyperparamRegistry:
    def __init__(self) -> None:
        self._bst = BST()

    # --------------------------------------------------------- add / retrieve
    def add_trial(self, score: float, params: Dict[str, Any]) -> None:
        self._bst.insert(score, params)

    def best(self) -> Optional[TrialNode]:
        return self._bst.find_max()

    def worst(self) -> Optional[TrialNode]:
        return self._bst.find_min()

    def top_k(self, k: int) -> List[TrialNode]:
        return list(reversed(self._bst.inorder()))[:k]

    def all_trials(self) -> List[TrialNode]:
        return self._bst.inorder()

    # ----------------------------------------------------------- range / prune
    def range_query(self, lo: float, hi: float) -> List[TrialNode]:
        result: List[TrialNode] = []
        self._range(self._bst.root, lo, hi, result)
        return result

    def _range(self, node: Optional[TrialNode], lo: float, hi: float, result: list) -> None:
        if node is None:
            return
        if node.score > lo:
            self._range(node.left, lo, hi, result)
        if lo <= node.score <= hi:
            result.append(node)
        if node.score < hi:
            self._range(node.right, lo, hi, result)

    def prune_below(self, threshold: float) -> int:
        to_delete = [n.score for n in self._bst.inorder() if n.score < threshold]
        for score in to_delete:
            self._bst.delete(score)
        return len(to_delete)

    # ----------------------------------------------------------- introspection
    def inorder(self) -> List[TrialNode]:
        return self._bst.inorder()

    def is_balanced(self) -> bool:
        return self._bst.is_balanced()

    def height(self) -> int:
        return self._bst.height()

    def summary(self) -> Dict[str, Any]:
        trials = self._bst.inorder()
        best = self.best()
        worst = self.worst()
        return {
            "count": len(self._bst),
            "best_score": best.score if best else None,
            "worst_score": worst.score if worst else None,
            "height": self._bst.height(),
            "balanced": self._bst.is_balanced(),
        }

    def _reverse_inorder(self) -> List[TrialNode]:
        return list(reversed(self._bst.inorder()))
