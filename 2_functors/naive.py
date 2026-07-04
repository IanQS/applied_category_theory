"""
Naive version: keep every run in a plain list and scan it.

From the monoind post, each config now returns a `Run` that we hold onto (not just fold into a Summary). This way we can surface the best model or filter over a loss range or transform all the data. What's cool is that a `list` already handles all this - it implements a `map` and a `filter`.

The only issue with the `list` is speed: `best` and `between` has to scan the entire list each time, which is painful when we have a few hundreds of thousands of runs.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Run:
    loss: float
    config: dict


def run_config(config: dict) -> Run:
    # No failures here. We assume runs succeed and revisit that in the monad post.
    return Run(loss=round(random.random(), 4), config=config)


def best(runs: list[Run]) -> Run:
    return min(runs, key=lambda run: run.loss)

def between(runs: list[Run], low: float, high: float) -> list[Run]:
    return [run for run in runs if low <= run.loss <= high]    # scans everything


if __name__ == "__main__":
    random.seed(0)
    runs = [run_config({"lr": round(random.random(), 3)}) for _ in range(20)]

    print("best:", best(runs).loss)
    print("in [0.2, 0.4]:", sorted(run.loss for run in between(runs, 0.2, 0.4)))

    # A list is already a functor: map and filter are right there.
    penalized = list(map(lambda run: replace(run, loss=run.loss + 1.0), runs))
    good = list(filter(lambda run: run.loss < 0.5, runs))
    print("mapped:", len(penalized), "filtered:", len(good))
