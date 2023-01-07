"""
Let's consider our "simple" tree-node class from before
"""
import copy
from typing import Any


class _TreeNode(object):
    def __init__(self, key, aux_data: Any):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        self.aux_data = aux_data


"""
Purity and impurity often rear their heads when it comes to classes - in fact, this is where the idea of 
"""


def pure_vs_impure():
    def impure(tree_node_inst: _TreeNode) -> _TreeNode:
        """We mutate the input"""
        tree_node_inst.aux_data += 5
        return tree_node_inst

    def pure(tree_node_inst: _TreeNode) -> _TreeNode:
        """We operate on a deepcopy of the input"""
        copy_ = copy.deepcopy(tree_node_inst)
        copy_.aux_data += 5
        return copy_

    # We see how our "pure" and "impure" instances are defined exactly the same
    pure_instance = _TreeNode("some_key", 5)
    impure_instance = _TreeNode("some_key", 5)

    for i in range(5):
        print(f"Pure: {pure(pure_instance).aux_data}\tImpure: {impure(impure_instance).aux_data}")


"""
Our monoids. The below is an example in a "real world" setting where it would have been
extremely easy to incorrectly use the code. 

Our actual implementation (in __add__) was pure as we operated on a new instance,
hence every new call will be pure and "safe". We copy the implementation below and put it into
`pure_add`.

Note: python and other non-functional programming languages aren't necessarily the "best" because
functional programming languages are meant to deal with creating copies or non-mutation of inputs.

Use what is best for your use-case (as sacrilegious as that may sound to FP-ers)
"""

import numpy as np
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class MDC_Monoid():
    accum_grad: np.ndarray = np.empty(())
    accum_sq_grad: np.ndarray = np.empty(())
    num_houses_serviced: int = 0
    num_IHMs_failed: int = 0
    ihm_time_tracker: List[float] = field(default_factory=list)

    def impure_add(self, other: Optional["MDC_Monoid"]) -> "MDC_Monoid":
        """
        Clearly, repeated calls involving our "self" will always yield new results,
        which is dangerous. This makes it very difficult to
        """
        if other is None:
            return self
        self.accum_grad = self.accum_grad + other.accum_grad,
        self.accum_sq_grad = self.accum_sq_grad + other.accum_sq_grad,
        self.num_houses_serviced = self.num_houses_serviced + other.num_houses_serviced,
        self.num_IHMs_failed = self.num_IHMs_failed + other.num_IHMs_failed,
        self.ihm_time_tracker = self.ihm_time_tracker + other.ihm_time_tracker
        return self

    def pure_add(self, other: Optional["MDC_Monoid"]) -> "MDC_Monoid":
        return self + other

    def __add__(self, other: Optional["MDC_Monoid"]) -> "MDC_Monoid":
        if other is None:
            return self
        return MDC_Monoid(
            accum_grad=self.accum_grad + other.accum_grad,
            accum_sq_grad=self.accum_sq_grad + other.accum_sq_grad,
            num_houses_serviced=self.num_houses_serviced + other.num_houses_serviced,
            num_IHMs_failed=self.num_IHMs_failed + other.num_IHMs_failed,
            ihm_time_tracker=self.ihm_time_tracker + other.ihm_time_tracker
        )


if __name__ == '__main__':
    pure_vs_impure()
