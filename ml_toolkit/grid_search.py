import itertools
from typing import Callable, Dict, List, Tuple

from tqdm import tqdm

from bst_toolkit.registry import HyperparamRegistry


def grid_search(
    param_grid: Dict[str, List],
    evaluate_fn: Callable,
    dataset: Tuple,
    verbose: bool = True,
) -> HyperparamRegistry:
    keys = list(param_grid.keys())
    combos = list(itertools.product(*[param_grid[k] for k in keys]))
    registry = HyperparamRegistry()
    iterator = tqdm(combos, desc="Grid Search") if verbose else combos
    for values in iterator:
        params = dict(zip(keys, values))
        score = evaluate_fn(params, dataset)
        registry.add_trial(score, params)
    return registry
