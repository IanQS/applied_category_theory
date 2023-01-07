# Monads and Functors Discussion

I'd recommend only reading this section after reading the rest of the material. Here, we highlight the
similarities and differences between monads and functors two.

## What's the diff?

This [excellent answer](https://stackoverflow.com/a/56601178/3532564) describes, at a
very high level, `functors`
and `monads`

> `functors` and `monads` both provide some tool to wrapped input, returning a wrapped output.

- `functor` = map (i.e., the tool)

- `monad` = unit + bind

**Note** we removed the `(>>)` from `Monads` and `(<$)` from `Functor` as they aren't as relevant for our discussion in
this tutorial.

### Recap: Functor

An abstract class definition is like the following:

```
class Functor F where
    fmap :: (a -> b) -> F a -> F b
    (<$) :: a -> F b -> F a
    # ^ we don't cover this
```

> `fmap`

The fmap describes how you can apply a function, `func`, to the contents of the `functor`.

### Recap: Monad

An abstract class definition is like the following:

```
class Monad M where
  (>>=)  :: M a -> (  a -> M b) -> M b
  return ::   a                 -> M a
```

> `>>=`

describes how for a given structure, `M`, we can take a function and operate on the internal contents of the type. Note
that, unlike the `fmap`, our return value is the Monad, not the to-be-wrapped value.

## Further discussion

In the first "line" of both classes, we are "defining an interface" that describes how we "open" the structure and apply
the functions.

