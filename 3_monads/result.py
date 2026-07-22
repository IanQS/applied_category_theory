"""

IMO there are two ways to introduce Monads:

1) directly from the definition of a monad

2) deriving it from a functor, a la [Monad - derivation from functors](https://en.wikipedia.org/wiki/Monad_(functional_programming)#Derivation_from_functors)

I'll briefly define the first, but since we're building up from functors to see exactly what a monad is, how we use it in the context of ML, and how it's related to functors, I figure we'll focus on the second instance

---

1) From the direct definition: in a sense, a [monad is a burrito](https://blog.plover.com/prog/burritos.html) (this made the rounds during college when people would ask "WTF is a monad?") and I mean this ONLY in the context of it being a container. I promise this will make sense.

A monad requires two things (see the blog, but we summarize it here):

- a `unit` operation, which wraps a plain value in the container: `a -> M a`. The "identity" part is that `bind`-ing it changes nothing
- a `bind` operation, which applies a function to the contents of our container (applies it to the inside of our burrito)

`bind` has the function signature (from Haskell) of:

`(M a) -> (a -> M b) -> (M b)`

where M is the monadic object. This says that we take a monadic object AND a function that is applied to the contents of the monadic object, `a`, and returns (M b)

---

2) from a functor, as per [wikipedia](https://en.wikipedia.org/wiki/Monad_(functional_programming)#Derivation_from_functors):

> Though rarer in computer science, one can use category theory directly, which defines a monad as a functor with two added natural transformations:

Just a quick reminder, from `functors` we have a `map` (and `filter`). The two added natural transformations are:

- `unit`, the same wrap as in 1): `a -> M a`. For us it's the `Ok` constructor itself, and "natural" just means it wraps without looking: `Ok(x).map(f) == Ok(f(x))` for any plain `f`

- `join`, which collapses one layer of nesting: `M (M a) -> M a`. Defined below as `flatten`, because that's what it does

This route makes `bind` derived rather than primitive, and the code below takes that literally: mapping a step of type `a -> M b` leaves an `M (M b)` behind, `join` unwraps the nested layer, and `bind` is defined as exactly that composite:

`ma.bind(step) == flatten(ma.map(step))`

The short-circuiting we want from `Result` is emergent: `map` leaves an `Err` untouched and `flatten` passes it through, so no `if failed, skip` ever gets written. (`test_bind_short_circuits` over in monads.py checks the derived `bind` still behaves like naive.py's hand-rolled ladder.)


"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Ok:
    value: object

    def map(self, f: Callable[[object], object]) -> Result:
        return Ok(f(self.value))

    def bind(self, step: Callable[[object], Result]) -> Result:
        return flatten(self.map(step))  # map double-wraps the step's Result, flatten undoes it


@dataclass(frozen=True)
class Err:
    reason: str

    def map(self, f: Callable[[object], object]) -> Err:
        return self  # a dead run stays dead, and keeps its reason

    def bind(self, step: Callable[[object], Result]) -> Result:
        return flatten(self.map(step))  # map is a no-op on an Err, so it slides through untouched


Result = Ok | Err


def flatten(nested: Result) -> Result:
    """collapse one Result layer (route 2's `join`):

    - Ok(Ok(x)) -> Ok(x),
    - Ok(Err) -> Err,
    - Err -> Err.

    It undoes exactly the layer `unit` adds, which is why binding `Ok` is a no-op
    (the identity law).
    """
    if isinstance(nested, Err):
        return nested
    return nested.value
