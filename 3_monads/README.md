# Note:

Please read through [The monoid](https://ianq.ai/cats-big-data-monoid/) and then [The functor](https://ianq.ai/cats-big-data-functor/) functor post first. The scenario itself is unchanged (copy-pasted from the first post):

> We have many worker machines each run a handful of training configs. Those reports are combined to make a final report.

In the post on monoids, I left a (rather) big plot-hole in the story - machines crash for a variety of reasons

> what if we wanted to store why a run failed, instead of swapping it for the identity Summary()?

The `monoid` post discarded information on **why** a machine would fail, and the functor code sidestepped this entirely (and was a bit of a tangent that we tie back in). This post will build up the pipeline with a `Result` monad, then bring the `Summary` monoid and the `LossTree` functor into the mix.

As before, `naive.py` is the hand-rolled version. It threads the failure reason(s) through the machines by hand, and at the end it threads a running log the same way, so it lines up one to one with the two monads. `result.py` holds the `Result` monad on its own. `monads.py` imports it, builds the combined `Report`, and finishes with the `Writer` monad.

`monoids.py` and `functors.py` here are copies of the files from the first two posts, kept alongside `monads.py` so it can import the `Summary` monoid and the `LossTree` functor directly rather than restating them. The one addition, marked "New for post 3" in `functors.py`, is the pair of ops that make `LossTree` a monoid (`of` and `__add__`), so it can be folded into the `Report`.
