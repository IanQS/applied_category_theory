# Note:

Please read through [The monoid](https://ianq.ai/cats-big-data-monoid/) and then [The functor](https://ianq.ai/cats-big-data-functor/) functor post first. The scenario itself is unchanged (copy-pasted from the first post):

> We have many worker machines each run a handful of training configs. Those reports are combined to make a final report.

In the post on monoids, I left a (rather) big plot-hole in the story - machines crash for a variety of reasons

> what if we wanted to store why a run failed, instead of swapping it for the identity Summary()?

The `monoid` post discarded information on **why** a machine would fail, and the functor code sidestepped this entirely (and was a bit of a tangent that we tie back in). This post will build up the pipeline with a `Result` monad, then bring the `Summary` monoid and the `LossTree` functor into the mix.

As before, `naive.py` is a naive attempt at threading the failure reason(s) through the machines and aggregators. `monads.py` is the `Result` monad, the combined `Report`, and the `Writer` monad at the end.

`monoids.py` and `functors.py` here are verbatim copies of the files from the first two posts, kept alongside `monads.py` so it can import the `Summary` monoid and the `LossTree` functor directly rather than restating them. The only new thing `monads.py` adds to `LossTree` is the pair of ops that make it a monoid (`of` and `__add__`), so it can be folded into the `Report`.
