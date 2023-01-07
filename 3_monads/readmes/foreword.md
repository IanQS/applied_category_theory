# Foreword

We can motivate monads by first discussing purity and what purity gives us.

## Purity and Impurity

A pure function does not change its given input. Think of this like how we might do in math, where once we have defined
a
variable, we do not "change" it; instead, we declare a new variable and "assign" to it.

This is useful because if we run a function N-times with the same input, we always get the same result. And because we
always get the same result, we have reduced cognitive load. We do not need to track the program's state in our minds.

TL;DR See [preface_purity_impurity.py](preface_purity_impurity.py) for some code examples (looking at our previously
developed
code) showcasing `purity` and `impurity`.

This all sounds great, but where do monads come in?

## Motivation for `Monads`

Although languages like `Haskell` (and other FPs) are made to
be pure, they are only "pure" insofar as their language constructs. This would make them useless in real-world
scenarios e.g., in ML, where we deal with datasets, where we accept some user input, or where we deal with io. So,
that's
where `Monad's come into play.

TL;DR `Monads` allow us to "wrap" the "impure" into a "pure" object via a container (not unlike our `functor's) from
earlier.

[Back to main](README.md)