# Note:

Please read through [The monoid](https://ianq.ai/cats-big-data-monoid/) and then [The functor](https://ianq.ai/cats-big-data-functor/) post first. The scenario itself is unchanged (copy-pasted from the first post):

> We have many worker machines each run a handful of training configs. Those reports are combined to make a final report.

In the post on monoids, I left a (rather) big plot-hole in the story - machines crash for a variety of reasons

> what if we wanted to store why a run failed, instead of swapping it for the identity Summary()?

The `monoid` post discarded information on **why** a machine would fail, and the functor code sidestepped this entirely. This post builds up the pipeline with a `Result` monad; In the fourth post, we will tie do a deep integration with our existing pipeline, with a `Summary` monoid and the `LossTree` functor, all wrapped into a monad.

As before, `naive.py` is the hand-rolled version, which will thread the failure reason through the steps by hand. `result.py` defines the `Result` monad, discussing the two ways of deriving `bind` in its preamble. `monads.py` builds the pipeline on top of it and checks the monad laws.
