"""
The monoid-al version of `naive.py`, accomplishing the same thing but IMO much cleaner, even if there is more code overall. Also, we build on this in the next post, so have faith ;)

"""
from __future__ import annotations

import math
import random
from collections.abc import Iterable
from dataclasses import dataclass


def run_config(config: dict) -> Summary:
    if random.random() < 0.1:
        return Summary()
    val = random.random()
    return Summary.of(loss=val)


@dataclass(frozen=True)
class Summary:
    """Summary statistics over a set of validation losses.

    This is a monoid:
      - Identity: `Summary()` an empty summary
      - Associative: we've defined + as an associative binary op
      - Closed: `+` over Summaries is always a Summary
    """
    count: int = 0
    total: float = 0.0
    total_sq: float = 0.0
    minimum: float = math.inf

    @classmethod
    def of(cls, loss: float) -> Summary:
        """Lift a single loss into a one-element Summary."""
        return cls(count=1, total=loss, total_sq=loss * loss, minimum=loss)

    def __add__(self, other: Summary) -> Summary:
        return Summary(
            count=self.count + other.count,
            total=self.total + other.total,
            total_sq=self.total_sq + other.total_sq,
            minimum=min(self.minimum, other.minimum),
        )

    # Derived quantities, read off once at the very end.
    @property
    def mean(self) -> float:
        return self.total / self.count if self.count else math.nan

    @property
    def variance(self) -> float:
        # E[x^2] - E[x]^2
        return self.total_sq / self.count - self.mean ** 2 if self.count else math.nan


# ---------------------------------------------------------------------------
# Reducing. Every node in the tree runs the *same* combine.
# ---------------------------------------------------------------------------
def summarize(per_worker_res: Iterable[Summary]) -> Summary:
    """A worker turns its raw losses into a single Summary."""
    accum = Summary()                              # start from the identity
    for i, worker_res in enumerate(per_worker_res):
        accum = accum + worker_res
    return accum


def reduce(summaries: Iterable[Summary]) -> Summary:
    """A reducer combines Summaries into one. The identity lets `sum` just work."""
    return sum(summaries, Summary())


if __name__ == "__main__":
    random.seed(0)

    # 100 workers, each running 10 configs; some runs fail.
    workers: list[list[Summary]] = [[run_config({}) for _ in range(10)] for _ in range(100)]
    per_worker = [summarize(w) for w in workers]

    groups = [reduce(per_worker[i:i + 10]) for i in range(0, 100, 10)]

    final = reduce(groups)

    print(f"runs:     {final.count}")
    print(f"min loss: {final.minimum:.4f}")
    print(f"mean:     {final.mean:.4f}")
    print(f"variance: {final.variance:.6f}")
