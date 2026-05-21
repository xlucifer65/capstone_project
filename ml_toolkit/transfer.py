from typing import Dict, List

from bst_toolkit.registry import HyperparamRegistry


def analyse_transfer(registry_a: HyperparamRegistry, registry_b: HyperparamRegistry) -> List[Dict]:
    trials_a = registry_a.inorder()
    trials_b = registry_b.inorder()

    rank_a: Dict[str, int] = {}
    for rank, node in enumerate(trials_a, start=1):
        key = _params_key(node.params)
        rank_a[key] = rank

    rank_b: Dict[str, int] = {}
    for rank, node in enumerate(trials_b, start=1):
        key = _params_key(node.params)
        rank_b[key] = rank

    report = []
    for node_b in trials_b:
        key = _params_key(node_b.params)
        rank_in_a = rank_a.get(key)
        rank_in_b = rank_b[key]
        drift = (rank_in_b - rank_in_a) if rank_in_a is not None else None
        report.append({
            "params": node_b.params,
            "score_a": next((n.score for n in trials_a if _params_key(n.params) == key), None),
            "score_b": node_b.score,
            "rank_a": rank_in_a,
            "rank_b": rank_in_b,
            "rank_drift": drift,
        })

    report.sort(key=lambda r: abs(r["rank_drift"]) if r["rank_drift"] is not None else 0, reverse=True)
    return report


def _params_key(params: dict) -> str:
    return str(sorted(params.items()))
