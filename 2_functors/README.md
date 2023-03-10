# Foreword

## Note: A functor vs. a function

In `C++` (and perhaps other languages), people will occasionally refer to functors in a different light than we will in
this tutorial.
See [funtor vs. function - C++](https://stackoverflow.com/questions/6451866/why-use-functors-over-functions).

This tutorial discusses functors in the category theory sense.

## Scenario

After your big project, you sneak off to Hawaii for a bit. You've been watching "White Lotus". You have always
wanted to go, so after the successful project launch from your monoid work, this was your opportunity. While in Hawaii,
you
run into Santa and Rudolph, and you all get to talking (while relaxing on the
beach, of course).

<img height="300" src="../assets/santa_elf_beach.jpg" width="300"/> 

(Art from Stable Diffusion)

Santa has some big ideas, and you pitched your own to the big guy. It turns out that in the past, Santa used to be a
lead engineer but put away his Engineering cap for the famous red one; his mind is still sharp as ever for these sorts
of problems, and he has some insights and ideas he asked to follow up on when you all get back from vacation.

On the sleigh ride back (first class, woo!), Santa says he'd like to eventually get the loss associated
with each IHM. Santa feels that
some children are trying to game the system where they'd act good at home but are bad outside; getting the IHM loss
would be a great first way to study this problem. You agree to spearhead this project and prototype it.

## MVP: Feb 1st

You decide to start with a reduced problem - your goal is to "intercept" the data at the `MPDC` level and accumulate the
results there. You decide to gather requirements and talk to the various teams:

- **Data Elfgineers**: they have **finally** added the `UUID` to the IHM results, which will make the lookups easy. They
  asked for the ability to add arbitrary data to the tracked objects and modify the existing data.

- **Data Scientists**: they want the ability to "bin" the UUIDs; this would make studying behavior easy: "we want all
  IHMs where the `key` is between `X` and `Y`".

We can assume that none of the IHMs will fail for the prototype. It's just easier to test it that way, but we will have
to come back to it later to fix it up.

### Tasklist

1) Get the UUIDs associated with each IHM
2) Expose a function, `map_func`, to add arbitrary data to the stored IHM data
3) Expose a function, `filter_on_key`, that allows you to filter arbitrary keys based on some bounds

### A Solution

`sol/functors_day_1.py` and `sol/functor_driver.py`, where we changed the code to include a sample

## Expanding the Requirements

So the data scientists are thrilled with the ability to look up the loss values, but they (rightfully) complained
that the lookup was far too slow, especially on large datasets. Sorting the data would be unbelievably painful, so could
you sort something out?

You kick back and think about how you could change it and realize that a quick binary-search tree where the key is the
loss. For the balancing, you decide to use an AVL tree implementation you found online
on [programiz](https://www.programiz.com/dsa/avl-tree).

### Tasklist

1) Modify the system to support a binary search tree. An implementation is provided in `avl_tree.py`, which was modified
   for our problem.

#### Note For the Task

This is the most significant change we will see in this section on functors, so do try and follow along with the logic
in `day_2`. I'll mark out specific areas to note in the code.

### A solution

`sol/functors_day_2.py`

We create a new data structure that will accompany our MDC_Monoid. Thankfully, we can use this to quickly look up the
appropriate values. Please read the comments at the top of the file and just the entire file overall.

## Day 3: Cleaning up our AVL tree

You managed to wrap up your code but weren't too happy with the results. The code looks messy, and your
pattern-matching spidey senses are going off. You decide to call the previous lead, the one who told you
about `monoids.`
and he says that he's been looking at `functors` lately, and they might help you. He said something about "abstracting
over containers," which you think would help.

### Functors

A functor must support, [at the minimum (according to Haskell)](https://wiki.haskell.org/Functor#Syntax), a `fmap`,
which describes how to apply an arbitrary function into the function encapsulated in our class.

#### Further Discussion

See [functors_101.md](functors_101.md) for a more in-depth discussion on functors and their definition, but TL;DR, by
using functors, we can
abstract over "containers" or "structures". Functors and monads provide some tools to operate on a wrapped input.

Compare and contrast how easily we could use a `map` and `filter` on our original code from `sol/functor_day_1.py` and
our code from `sol/functor_day_3_cleanup.py`. The `list` structure
felt natural to think about lists where we can iterate. Still, we see that we could also define a way to map functions
over our `AVLTree` in a manner that makes sense.

### Tasklist

Clean up the code from `sol/functor_day_2.py` and `sol/avl_tree_starter.py` and transform them
into `sol/functor_day_3.py` and `sol/avl_tree_functor.py`

## Closing out

Earlier, we mentioned that we were prototyping.

> We can assume that none of the IHMs will fail for the prototype. It's just easier to test it that way, but we will
have
to come back to it later to fix it up.

But now that we're past that hurdle, we've reached a point where we need to handle the `None` values that might get
returned. Although Python has nice syntax for handling `None`, I'll introduce the following idea: `Maybe`. A `Maybe`
encapsulates the idea of a "This-might-be-something," and if it is not, it is "Nothing". See
how [Rust](https://doc.rust-lang.org/std/option/) handles optional values.

We revisit this idea and logging in our section on `monads` to finish this tutorial.