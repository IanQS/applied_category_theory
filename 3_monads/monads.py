"""
The monad version:


thread a run through a pipeline of steps that can each fail,
carrying *why* it failed instead of collapsing it to a None or an empty Summary.

There are two parts here: a `Report`, which encapsulates the results of various runs, and a `Writer`, which
accumulates result logs.

`Report`:
    This is the culmination of all our work, so we import the Summary monoid and the
    LossTree functor from the copies in this repo.

    Note: we've augmented `LossTree` in `functors.py` (marked "New for post 3"): the
        `of` and `__add__`, that transform it from a functor to a monoid, which
        lets a `Report` full of trees fold up post 1's reduction tree, unchanged

`Writer`:
    threads a value while accumulating a log on the side. The log is any monoid,
    so the Summary from post 1 drops straight in: a monoid living inside a monad.
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, replace

from result import Ok, Err, Result  # the Result monad, defined in the same dir
from monoids import Summary  # the monoid from post 1
from functors import LossTree  # the functor from post 2, but augmented with a new op


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
    # Pure packaging: give a non-erroring result its loss.
    return Ok(replace(run, loss=round(random.random(), 4)))


def evaluate(config: dict) -> Result:
    """
    The outcome of any step failing, OR the result getting a loss
    """
    return load_shard(config).bind(train).bind(validate).bind(score)


# ---------------------------------------------------------------------------
# Where the three posts meet: the monad's outcomes feed a monoid (Report) that
# carries a functor (LossTree, promoted to a monoid over in functors.py).
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Report:
    """A product of three monoids: combine the stats, merge the survivors, add up
    the failure counts. That is why the whole thing still folds up post 1's tree."""

    stats: Summary
    survivors: LossTree
    failures: Mapping[str, int]

    @classmethod
    def empty(cls) -> Report:
        return cls(Summary(), LossTree(), {})

    def __add__(self, other: Report) -> Report:
        combined_failures = dict(self.failures)
        for reason, count in other.failures.items():
            combined_failures[reason] = combined_failures.get(reason, 0) + count
        return Report(
            self.stats + other.stats,
            self.survivors + other.survivors,
            combined_failures,
        )


def fold_outcome(outcome: Result) -> Report:
    """
    In post 1 we sidestepped failures (code errors, machine errors, etc.) but just
    creating an empty monoid. Here, we track the actual reason (wrapped in the identity)
    """
    if isinstance(outcome, Err):
        return Report(Summary(), LossTree(), {outcome.reason: 1})
    run = outcome.value
    return Report(Summary.of(run.loss), LossTree.of(run), {})


def reduce(reports: Iterable[Report]) -> Report:
    return sum(reports, Report.empty())


# ---------------------------------------------------------------------------
# The Writer monad: thread a value while accumulating a log. The log is any
# monoid (combined with +), so the Summary above slots in as easily as a list.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Writer:
    value: object
    log: object

    def bind(self, step: Callable[[object], Writer]) -> Writer:
        """
        From the second avenue, from `result.py`, we know that `bind` is
        derived by applying the function (leaving a Writer inside a Writer),
        then joining. A Writer's join merges the logs, so both halves are
        inlined below.
        """
        stepped = step(self.value)
        return Writer(stepped.value, self.log + stepped.log)

    def map(self, f: Callable[[object], object]) -> Writer:
        return Writer(f(self.value), self.log)


def load_traced(config: dict) -> Writer:
    return Writer(Run(config), [f"loaded shard for lr={config['lr']}"])


def train_traced(run: Run) -> Writer:
    num_epochs = random.randint(2, 10)
    return Writer(run, [f"trained {num_epochs} epochs"])


def score_traced(run: Run) -> Writer:
    scored = replace(run, loss=round(random.random(), 4))
    return Writer(scored, [f"scored: loss={scored.loss}"])


def measured(loss: float) -> Writer:
    """Same Writer, but the log is a Summary: a monoid riding inside a monad."""
    return Writer(loss, Summary.of(loss))


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
    # associativity: nesting the binds on either side lands in the same place
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

    # 1000 configs threaded through the fallible pipeline; each lands as a Result.
    outcomes = [evaluate({"lr": round(random.random(), 3)}) for _ in range(1000)]

    # Fold each outcome into a Report, then reduce up the same tree as post 1.
    per_config = [fold_outcome(outcome) for outcome in outcomes]
    groups = [reduce(per_config[i : i + 100]) for i in range(0, 1000, 100)]
    final = reduce(groups)

    print(f"survivors: {len(final.survivors)}")
    print(f"best loss: {final.survivors.best().loss}")
    print(f"mean:      {final.stats.mean:.4f}")
    print(f"failures:  {final.failures}")

    # The Writer: thread one run through the pipeline and collect a trace for free.
    traced = load_traced({"lr": 0.05}).bind(train_traced).bind(score_traced)
    print("\ntrace:")
    for line in traced.log:
        print(f"  {line}")

    # Swap the list log for a Summary log and Writer threads statistics instead.
    stats = measured(0.31).bind(lambda _: measured(0.12)).bind(lambda _: measured(0.48))
    print(f"\nWriter with a Summary log: mean={stats.log.mean:.4f}")

    print()
    test_monad_laws()
    test_bind_short_circuits()
