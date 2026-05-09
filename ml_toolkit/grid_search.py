from itertools import product
from tqdm import tqdm
from bst_toolkit import HyperparamRegistry


def grid_search(param_grid: dict, evaluate_fn: callable, dataset, verbose: bool = True) -> HyperparamRegistry:
    """
    Run all hyperparameter combinations and store results in HyperparamRegistry.

    Parameters
    ----------
    param_grid : dict
        Example: {"n_estimators": [50, 100], "max_depth": [3, 5]}
    evaluate_fn : callable
        Function like evaluate_fn(params, dataset) -> float
    dataset : any
        Dataset used by evaluate_fn
    verbose : bool
        If True, show progress bar.

    Returns
    -------
    HyperparamRegistry
        Registry containing all trial results.
    """

    registry = HyperparamRegistry()

    keys = list(param_grid.keys())
    values = list(param_grid.values())

    combinations = list(product(*values))

    iterator = tqdm(combinations, desc="Grid Search") if verbose else combinations

    for combo in iterator:
        params = dict(zip(keys, combo))

        score = evaluate_fn(params, dataset)
        score = round(float(score), 6)

        registry.add_trial(score, params)

        if verbose:
            iterator.set_postfix(score=score)

    return registry