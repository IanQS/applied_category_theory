"""
Naive version: where we catch the failures and propagate them around manually

Remember that in the first post (monoids) we side-stepped the failures by swapping out the dead run for the identity
`Summary()`, which also threw away information about the machine (or why it died). If we were trying to keep the
information, and assuming we needed a guard block after every step, this turns into a cascade of guards.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Run:
    config: dict
    loss: float = math.nan


MaybeResult = Run | None  # the run if the step succeeded, None if it failed
MaybeFailure = str | None  # why it failed, None if it didn't


def load_shard(config: dict) -> tuple[MaybeResult, MaybeFailure]:
    if random.random() < 0.10:
        return None, "shard missing"
    return Run(config), None


def train(run: Run) -> tuple[MaybeResult, MaybeFailure]:
    if random.random() < 0.10:
        return None, "diverged (NaN loss)"
    return run, None


def validate(run: Run) -> tuple[MaybeResult, MaybeFailure]:
    if random.random() < 0.10:
        return None, "OOM"
    return run, None


def score(run: Run) -> tuple[MaybeResult, MaybeFailure]:
    return Run(run.config, loss=round(random.random(), 4)), None


def evaluate(config: dict) -> tuple[MaybeResult, MaybeFailure]:
    """(run, None) on success, (None, reason) at the first failure. Every step
    has to be unpacked and checked before the next one can run: the cascade the
    module docstring warned about."""
    shard, reason = load_shard(config)
    if shard is None:
        return None, reason
    trained, reason = train(shard)
    if trained is None:
        return None, reason
    validated, reason = validate(trained)
    if validated is None:
        return None, reason
    return score(validated)


if __name__ == "__main__":
    random.seed(0)
    configs = [{"lr": round(random.random(), 3)} for _ in range(1000)]

    survivors = []
    failures = {}
    for config in configs:
        run, reason = evaluate(config)
        if run is None:
            failures[reason] = failures.get(reason, 0) + 1
        else:
            survivors.append(run)

    print(f"survivors: {len(survivors)}")
    print(f"failures:  {failures}")
