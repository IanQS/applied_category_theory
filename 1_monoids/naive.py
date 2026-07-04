"""
Naive version that a dev who is unfamiliar with monoids might write. The
summary-statistics counterpart of `monoids.py`,

The combine logic is repeated at every level, and every new statistic the
boss asks for means editing `summarize`, `reduce`, AND the final read-out at the bottom.
"""
from __future__ import annotations

import math
import random


def run_config(config: dict) -> float | None:
    if random.random() < 0.1:
        return None
    return random.random()


def summarize(losses: list[float | None]) -> dict:
    """A worker folds its raw losses into a collection of partial statistics."""
    minimum, total, total_sq, count = math.inf, 0.0, 0.0, 0
    for loss in losses:
        if loss is None:                 # Check for None
            continue
        minimum = min(minimum, loss)
        total += loss
        total_sq += loss * loss
        count += 1
    return {"count": count, "total": total, "total_sq": total_sq, "min": minimum}


def reduce(reports: list[dict]) -> dict:
    """A reducer folds the collections together"""
    minimum, total, total_sq, count = math.inf, 0.0, 0.0, 0
    for r in reports:                    # repeated accumulations
        minimum = min(minimum, r["min"])
        total += r["total"]
        total_sq += r["total_sq"]
        count += r["count"]
    return {"count": count, "total": total, "total_sq": total_sq, "min": minimum}


if __name__ == "__main__":
    random.seed(0)

    # 100 workers, each running 10 configs; some runs fail.
    workers = [[run_config({}) for _ in range(10)] for _ in range(100)]
    per_worker = [summarize(w) for w in workers]
    groups = [reduce(per_worker[i:i + 10]) for i in range(0, 100, 10)]
    final = reduce(groups)

    # ...and the caller has to know how to turn the bag of accumulators into stats.
    mean = final["total"] / final["count"]
    variance = final["total_sq"] / final["count"] - mean ** 2
    print(f"runs:     {final['count']}")
    print(f"min loss: {final['min']:.4f}")
    print(f"mean:     {mean:.4f}")
    print(f"variance: {variance:.6f}")
