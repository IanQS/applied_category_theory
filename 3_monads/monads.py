"""
The monad version of `naive.py`: thread a run through a pipeline of steps that can
each fail, carrying *why* it failed instead of collapsing it to a None.

`result.py` holds the `Result` monad itself (and the two-route derivation of `bind`).
This file is the pipeline built on top of it, plus checks that `bind` really does
satisfy the monad laws and short-circuit the way the hand-rolled ladder did.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, replace

from result import Err, Ok, Result


@dataclass(frozen=True)
class Run:
    config: dict
    loss: float = math.nan  # filled in by `score` once the run survives


# ---------------------------------------------------------------------------
# The pipeline. Each step can fail, and each failure carries a reason.
# ---------------------------------------------------------------------------
def load_shard(config: dict) -> Result:
    if random.random() < 0.10:
        return Err("shard missing")
    return Ok(Run(config))


def train(run: Run) -> Result:
    if random.random() < 0.10:
        return Err("diverged (NaN loss)")
    return Ok(run)


def validate(run: Run) -> Result:
    if random.random() < 0.10:
        return Err("OOM")
    return Ok(run)


def score(run: Run) -> Result:
    return Ok(replace(run, loss=round(random.random(), 4)))


def evaluate(config: dict) -> Result:
    """
    The outcome of any step failing, OR the result getting a loss
    """
    return load_shard(config).bind(train).bind(validate).bind(score)


def test_monad_laws():
    """The monad laws are the monoid laws one level up: an identity (Ok) and an
    associative composition (bind)."""

    def grow(n):
        return Ok(n + 1)

    def double(n):
        return Ok(n * 2)

    # left identity: Ok(a).bind(f) == f(a)
    assert Ok(3).bind(grow) == grow(3)
    # right identity: m.bind(Ok) == m
    assert Ok(3).bind(Ok) == Ok(3)
    # associativity: nesting the binds on either side brings us to the same spot
    assert Ok(3).bind(grow).bind(double) == Ok(3).bind(lambda n: grow(n).bind(double))
    print("Monad laws hold (identity + associativity, i.e. a monoid)")


def test_bind_short_circuits():
    """bind is defined as flatten . map over in result.py, so the short-circuit
    is emergent: check the derived form still behaves like naive.py's ladder."""

    def step(n):
        return Ok(n + 1)

    assert Ok(10).bind(step) == Ok(11)
    assert Err("shard missing").bind(step) == Err("shard missing")
    print("bind (= flatten . map) steps on Ok, short-circuits on Err")


if __name__ == "__main__":
    random.seed(0)

    # A handful of configs through the fallible pipeline; each lands as a Result,
    # Ok or Err, with no guard anywhere in evaluate.
    for _ in range(12):
        print(evaluate({"lr": round(random.random(), 3)}))

    print()
    test_monad_laws()
    test_bind_short_circuits()
