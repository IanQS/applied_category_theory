"""
Naive version: where we catch the failures and propagate them around manually

Remember that in the first post (monoids) we side-stepped the failures by swapping out the dead run for the identity
`Summary()`, which also threw away information about the machine (or why it died). If we were trying to keep the
information, and assuming we needed a guard block after every step, this turns into a cascade.

The end of the file does the same thing for a running log instead of a failure reason, so it lines up one to one with
 the Result and Writer monads over in monads.py.
"""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Run:
    config: dict
    loss: float = float("nan")


def load_shard(config: dict):
    if random.random() < 0.10:
        return None, "shard missing"
    return Run(config), None


def train(run: Run):
    if random.random() < 0.10:
        return None, "diverged (NaN loss)"
    return run, None


def validate(run: Run):
    if random.random() < 0.10:
        return None, "OOM"
    return run, None


def score(run: Run):
    return Run(run.config, loss=round(random.random(), 4)), None


def evaluate(config: dict):
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


# ---------------------------------------------------------------------------
# The same shape, but we pass a running log instead of a failure reason. Each
# step hands back its own line and the caller has to remember to stitch them
# together before moving on. The Writer monad handles this portion
# ---------------------------------------------------------------------------
def load_traced(config: dict):
    return Run(config), [f"loaded shard for lr={config['lr']}"]


def train_traced(run: Run):
    num_epochs = random.randint(2, 10)
    return run, [f"trained {num_epochs} epochs"]


def score_traced(run: Run):
    scored = Run(run.config, loss=round(random.random(), 4))
    return scored, [f"scored: loss={scored.loss}"]


def evaluate_traced(config: dict):
    run, trace = load_traced(config)
    trained, step_trace = train_traced(run)
    trace = trace + step_trace
    scored, step_trace = score_traced(trained)
    trace = trace + step_trace
    return scored, trace


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

    scored, trace = evaluate_traced({"lr": 0.05})
    print("\ntrace:")
    for line in trace:
        print(f"  {line}")
