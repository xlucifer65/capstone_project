import random
from typing import Callable, Tuple

from .registry import HyperparamRegistry
from .node import TrialNode


def _build_registry_from_nodes(nodes: list, evaluate_fn: Callable, dataset: Tuple) -> HyperparamRegistry:
    reg = HyperparamRegistry()
    for node in nodes:
        score = evaluate_fn(node.params, dataset)
        reg.add_trial(score, node.params)
    return reg


def rebuild_naive(registry: HyperparamRegistry, evaluate_fn: Callable, dataset: Tuple) -> HyperparamRegistry:
    """Re-insert trials in original inorder (ascending score) sequence."""
    nodes = registry.all_trials()
    return _build_registry_from_nodes(nodes, evaluate_fn, dataset)


def rebuild_shuffled(registry: HyperparamRegistry, evaluate_fn: Callable, dataset: Tuple) -> HyperparamRegistry:
    """Re-insert trials in a random order to reduce tree skew."""
    nodes = list(registry.all_trials())
    random.shuffle(nodes)
    return _build_registry_from_nodes(nodes, evaluate_fn, dataset)


def rebuild_balanced(registry: HyperparamRegistry, evaluate_fn: Callable, dataset: Tuple) -> HyperparamRegistry:
    """Re-evaluate all configs and build a balanced BST via divide-and-conquer."""
    nodes = registry.all_trials()
    scored = [(evaluate_fn(n.params, dataset), n.params) for n in nodes]
    scored.sort(key=lambda x: x[0])
    reg = HyperparamRegistry()
    _build_from_sorted(scored, reg)
    return reg


def _build_from_sorted(sorted_pairs: list, reg: HyperparamRegistry) -> None:
    if not sorted_pairs:
        return
    mid = len(sorted_pairs) // 2
    score, params = sorted_pairs[mid]
    reg.add_trial(score, params)
    _build_from_sorted(sorted_pairs[:mid], reg)
    _build_from_sorted(sorted_pairs[mid + 1:], reg)
