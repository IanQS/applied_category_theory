"""

There are two ways to introduce Monads:

1) deriving it from a functor, a la [Monad - derivation from functors](https://en.wikipedia.org/wiki/Monad_(functional_programming)#Derivation_from_functors)

2) directly from the definition of a monad

Typically, I'd say just take the "direct definition" route (Wikipedia even introduces it that way), but for the purpose of this blog post series, I think it's better to start with the functor and show how we can construct the direct definition from it.

---


1) from a functor, as per [wikipedia](https://en.wikipedia.org/wiki/Monad_(functional_programming)#Derivation_from_functors):

> Though rarer in computer science, one can use category theory directly, which defines a monad as a functor with two added natural transformations:

Just a quick reminder, from `functors` we have a `map` (and `filter`). The two added natural transformations are:

- `unit`: `a -> M a` i.e. the constructor. It is "natural" in that it wraps the value up without looking internally i.e.: `Ok(x).map(f) == Ok(f(x))` for any plain `f`

- `join`: `M (M a) -> M a` i.e. collapses one layer of nesting. This is defined below in the code as `flatten`, because that's what it does!

---

2) From the direct definition: in a sense, a [monad is a burrito](https://blog.plover.com/prog/burritos.html) (this made the rounds during college when people would ask "WTF is a monad?") and I mean this ONLY in the context of it being a container. I promise this will make sense.

A monad requires two things (see my blog post, but we summarize it here):

- a `unit` operation, which wraps a plain value in the container: `a -> M a`. The "identity" part is that `bind`-ing it changes nothing
- a `bind` operation, which applies a function to the contents of our container (applies it to the filling of our burrito)

`bind` has the function signature (from Haskell) of:

`(M a) -> (a -> M b) -> (M b)`

where M is the monadic object. The signature says that we take a monadic object AND a function that is applied to the filling, `a`, and returns a new burrito with the filling transformed.

---

I've given it away already, but the two paths "join" at `bind` 😏 : the first path gives you a `map` (from the functor) and a `join`; composing the two generates your `bind`:  `bind(step) = flatten(map(step))`. On the other hand, the second path directly gives you the operation. Study the `bind` for the `Result` types below and this will all (hopefully) become clear
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Ok:
    value: object

    # From the functors definition
    def map(self, f: Callable[[object], object]) -> Result:
        return Ok(f(self.value))

    def bind(self, step: Callable[[object], Result]) -> Result:
        return flatten(self.map(step))  # map double-wraps the step's Result, flatten undoes it


@dataclass(frozen=True)
class Err:
    reason: str

    # From the functors definition
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
