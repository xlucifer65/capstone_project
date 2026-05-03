from __future__ import annotations
from typing import List, Callable, Tuple
from .registry import HyperparamRegistry
from .node import TrialNode
import random


def rebuild_naive(registry: HyperparamRegistry,
                  evaluate_fn: Callable,
                  new_dataset) -> HyperparamRegistry:
    """
    Strategy 1 — Re-score every trial and insert in sorted order.
    WARNING: produces a degenerate (linked-list) BST → O(n²) total time.
    This is intentional — we measure and demonstrate this problem.
    """
    new_registry = HyperparamRegistry()
    for node in registry.all_trials():          # sorted ascending
        score = evaluate_fn(node.params, new_dataset)
        new_registry.add_trial(round(score, 6), node.params)
    return new_registry


def rebuild_shuffled(registry: HyperparamRegistry,
                     evaluate_fn: Callable,
                     new_dataset) -> HyperparamRegistry:
    """
    Strategy 2 — Shuffle before re-inserting.
    Breaks sorted order → expected O(n log n), but not guaranteed balanced.
    """
    trials = registry.all_trials().copy()
    random.shuffle(trials)
    new_registry = HyperparamRegistry()
    for node in trials:
        score = evaluate_fn(node.params, new_dataset)
        new_registry.add_trial(round(score, 6), node.params)
    return new_registry


def rebuild_balanced(registry: HyperparamRegistry,
                     evaluate_fn: Callable,
                     new_dataset) -> HyperparamRegistry:
    """
    Strategy 3 — Divide & conquer balanced BST.
    Re-scores all, sorts, then builds a perfectly balanced tree.
    Guarantees height = floor(log2 n).
    """
    scored = []
    for node in registry.all_trials():
        score = evaluate_fn(node.params, new_dataset)
        scored.append((round(score, 6), node.params))
    scored.sort(key=lambda x: x[0])

    new_registry = HyperparamRegistry()
    root_node = _build_from_sorted(scored)
    _insert_tree(root_node, new_registry)
    return new_registry


def _build_from_sorted(sorted_trials: List[Tuple[float, dict]]):
    """
    Recursively build a balanced BST from a sorted list of (score, params).
    Mid element becomes root → left half → right half.
    O(n) time, O(log n) stack space.
    """
    if not sorted_trials:
        return None
    mid = len(sorted_trials) // 2
    score, params = sorted_trials[mid]
    node = TrialNode(score=score, params=params)
    node.left = _build_from_sorted(sorted_trials[:mid])
    node.right = _build_from_sorted(sorted_trials[mid + 1:])
    return node


def _insert_tree(node, registry: HyperparamRegistry):
    """Walk the pre-built tree and add every node into the registry."""
    if node is None:
        return
    registry.add_trial(node.score, node.params)
    _insert_tree(node.left, registry)
    _insert_tree(node.right, registry)