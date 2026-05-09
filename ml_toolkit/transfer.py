def _params_key(params: dict) -> tuple:
    """
    Convert params dictionary into a hashable key.
    Example: {"a": 1, "b": 2} -> (("a", 1), ("b", 2))
    """
    return tuple(sorted(params.items()))


def analyse_transfer(registry_A, registry_B) -> list:
    """
    Compare hyperparameter rankings between Dataset A and Dataset B.

    Returns a list of dictionaries:
    params, score_A, score_B, rank_A, rank_B, drift, transfer

    drift = rank_A - rank_B
    Positive drift means the configuration improved on Dataset B.
    """

    trials_A = registry_A.all_trials()
    trials_B = registry_B.all_trials()

    # Highest score should be rank 1, so reverse the ascending list
    ranked_A = list(reversed(trials_A))
    ranked_B = list(reversed(trials_B))

    lookup_A = {}
    lookup_B = {}

    for rank, node in enumerate(ranked_A, start=1):
        key = _params_key(node.params)
        lookup_A[key] = {
            "params": node.params,
            "score": node.score,
            "rank": rank,
        }

    for rank, node in enumerate(ranked_B, start=1):
        key = _params_key(node.params)
        lookup_B[key] = {
            "params": node.params,
            "score": node.score,
            "rank": rank,
        }

    report = []

    for key in lookup_A:
        if key not in lookup_B:
            continue

        item_A = lookup_A[key]
        item_B = lookup_B[key]

        rank_A = item_A["rank"]
        rank_B = item_B["rank"]

        drift = rank_A - rank_B

        report.append({
            "params": item_A["params"],
            "score_A": item_A["score"],
            "score_B": item_B["score"],
            "rank_A": rank_A,
            "rank_B": rank_B,
            "drift": drift,
            "transfer": "✓ good" if drift >= 0 else "✗ poor",
        })

    report = sorted(report, key=lambda x: x["drift"], reverse=True)

    return report