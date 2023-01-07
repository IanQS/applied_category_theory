# Foreword

We are on to the last portion of our tutorial! Thank you for sticking around and I hope that all of this has been
enlightening so far. Conceptually, this code is the 

## Scenario

Head to the [foreword](foreword.md) and then come back.

After a successful interview with the big man himself (this was mostly a formality at this point), you joined "The
Workshop", Santa's R&D branch. You stare out the window of your office, marveling at how quickly your career has
progressed. Just then Santa comes in saying "oh, when we last talked you mentioned you wanted to take on improving the
debugging? How's that going? The distributed systems team is running into a sack-load of issues".

![Sack of problems](../assets/big_sack_of_problems.jpg)

The question hangs in
the air before you turn around, point to your laptop and sit down to code. You really have to get this out ASAP

## Day 0: Catching up

You ping Noel again, begging to be put in touch with the current lead to find out what has been going wrong. The lead
comes in and shares
that their debugging process has been a nightmare. They've got functions calling functions and they need a way to pass
around logs. Your
`Monoids` and `Functors` have been extremely useful, but the team has ended up passing around lots of data and it is
difficult to maintain. Typically, they'd just overload the `__repr__` and `__str__` methods, but it's a little messy
visualizing
the tree-structure, and passing around the logs at every step is messy.

They tell you that they've used your final iteration of the code on functors and that it would be a fantastic starting
point.

## Day 1: Refactoring

You decide to tackle the issue of having the `None` values being stored in a separate data-structure. Ideally, they all
sit in the same place.

Task list

```
0) Modify the avl_tree class and IHM class to allow None-insertions
1) modify `map` to account for ^
```

### A solution

- `monad_day_1.py`

## Day 2: Logging

Going back to your conversation with Santa, you decide to add in logging to the code. 