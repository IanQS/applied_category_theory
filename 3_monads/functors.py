# Copy of ../2_functors/functors.py, kept here so monads.py can import the
# LossTree functor without reaching into a sibling directory. One change from
# the functor post: LossTree picks up the two ops that make it a monoid
# (`of` and `__add__`), marked "New for post 3" below.
"""
The functor version: hold the runs in a tree that is keyed by validation loss, rather than a list. That's it, folks.

The only downside of using the BST is that we need to implement a `map` and `filter`, but these are pretty easy, and that's what is so cool about functors! We can just swap out the "backend" - our downstream consumers (other teams, end-users, etc.) don't need to know or CARE what the data structure is. As prompted in the original monoid post (https://ianq.ai/talks/2023-01-01-cats) there's nothing special going on.

---

NOTE: a very cool result is that function composition is https://wiki.haskell.org/index.php?title=Functor#Description

Where we have:

- Functors preserve composition of morphisms
- Functors must preserve identity morphisms

We test this at the end
"""
from __future__ import annotations

import random
from collections.abc import Callable, Iterator
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Run:
    loss: float
    config: dict


def run_config(config: dict) -> Run:
    # No failures here. We assume runs succeed and revisit that in the monad post, where
    # we "pass up" the errors or failures
    return Run(loss=round(random.random(), 4), config=config)


class _Node:

     # Save space for when this scales up. Slots are pretty cool and IMO underused
    __slots__ = ("key", "run", "left", "right") 

    def __init__(self, key: float, run: Run):
        self.key = key
        self.run = run
        self.left: _Node | None = None
        self.right: _Node | None = None


class LossTree:
    """A binary search tree of Runs keyed by validation loss.

    Again, this could be swapped out for an AVL tree, red-black tree, etc. All that matters
    is we implement the "contract" of a `map` and `filter`
    """

    def __init__(self):
        self._root: _Node | None = None
        self._size = 0

    @classmethod
    def from_runs(cls, runs: Iterator[Run]) -> LossTree:
        tree = cls()
        for run in runs:
            tree.insert(run)
        return tree

    def insert(self, run: Run) -> None:
        self._root = self._insert(self._root, run)
        self._size += 1

    def _insert(self, node: _Node | None, run: Run) -> _Node:
        if node is None:
            return _Node(run.loss, run)
        if run.loss < node.key:
            node.left = self._insert(node.left, run)
        else:
            node.right = self._insert(node.right, run)
        return node

    def __len__(self) -> int:
        return self._size

    def items(self) -> Iterator[Run]:
        """Every run, in ascending loss order."""
        yield from self._inorder(self._root)

    def _inorder(self, node: _Node | None) -> Iterator[Run]:
        if node is not None:
            yield from self._inorder(node.left)
            yield node.run
            yield from self._inorder(node.right)

    def best(self) -> Run:
        node = self._root
        if node is None:
            raise ValueError("no runs")
        while node.left is not None:      # leftmost node holds the lowest loss
            node = node.left
        return node.run

    def between(self, low: float, high: float) -> LossTree:
        keep: list[Run] = []
        self._between(self._root, low, high, keep)
        return LossTree.from_runs(iter(keep))

    def _between(self, node: _Node | None, low: float, high: float, out: list[Run]) -> None:
        if node is None:
            return
        if node.key > low:                # anything smaller can only be to the left
            self._between(node.left, low, high, out)
        if low <= node.key <= high:
            out.append(node.run)
        if node.key < high:               # ...and anything larger to the right
            self._between(node.right, low, high, out)

    def map(self, f: Callable[[Run], Run]) -> LossTree:
        """(fmap . f) may change the loss (key), so we rebuild and re-key by the new value."""
        return LossTree.from_runs(f(run) for run in self.items())

    def filter(self, keep: Callable[[Run], bool]) -> LossTree:
        """(filter . f) may change the loss (key), so we rebuild and re-key by the new value."""
        return LossTree.from_runs(run for run in self.items() if keep(run))

    # New for post 3: `of` and `__add__` promote the tree from a functor to a
    # monoid (the identity is the empty LossTree()), so a Report full of trees
    # can fold up post 1's reduction tree unchanged.
    @classmethod
    def of(cls, run: Run) -> LossTree:
        """Lift a single run into a one-element tree, same shape as Summary.of."""
        tree = cls()
        tree.insert(run)
        return tree

    def __add__(self, other: LossTree) -> LossTree:
        # items() yields runs sorted by loss, and inserting sorted keys into a
        # plain BST builds a linked list (and a RecursionError somewhere around
        # a thousand runs). Shuffling keeps the demo tree shallow; the "use an
        # AVL or red-black tree in prod" disclaimer from post 2 still applies.
        merged_runs = [*self.items(), *other.items()]
        random.shuffle(merged_runs)
        return LossTree.from_runs(iter(merged_runs))

def test_composition(tree: LossTree):
    """
    We don't bother to test the:
    
        - Functors must preserve identity morphisms

    because that's pretty trivial.
    """
    def shift(run: Run) -> Run:
        """Transform the underlying data"""
        return replace(run, loss=round(run.loss + 1.0, 4))

    def tag(run: Run) -> Run:
        """Tag the run as reviewed"""
        return replace(run, config={**run.config, "reviewed": True})

    # f . g
    composed = tree.map(lambda run: tag(shift(run)))

    # g .f
    chained = tree.map(shift).map(tag)
    assert list(composed.items()) == list(chained.items())
    print("Composition law + Chaining Holds")
    

if __name__ == "__main__":
    random.seed(0)
    runs = [run_config({"lr": round(random.random(), 3)}) for _ in range(20)]
    tree = LossTree.from_runs(iter(runs))

    print("best:", tree.best().loss)
    print("in [0.2, 0.4]:", sorted(run.loss for run in tree.between(0.2, 0.4).items()))

    penalized = tree.map(lambda run: replace(run, loss=run.loss + 1.0))
    good = tree.filter(lambda run: run.loss < 0.5)
    print("mapped:", len(penalized), "filtered:", len(good))
    test_composition(tree)
