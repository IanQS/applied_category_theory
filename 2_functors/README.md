In our monoids post we motivated functors with

> 1. right now we only `count`, `average`, `min`, `variance` the `Summary`. What if our boss also wants to surface the best model so we can poke around, or filter by a loss range, or transform them? Instead of working with just a list (remember, in prod we might be training these over hundreds of thousands of models), we might want to work over a binary tree or AVL tree of some sort. Abstracting over the container is where `functor`s come in.

So lets jump in
