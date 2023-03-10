"""
1) Get the UUIDs associated with each IHM
2) Expose a function, `map_func`, to add arbitrary data to the stored IHM data
3) Expose a function, `filter_on_key`, that allows you to filter arbitrary keys based on some bounds
"""
import uuid
from dataclasses import dataclass
from typing import List, Callable

import numpy as np


@dataclass
class IHM:
    gradient: np.ndarray
    time_taken: np.ndarray
    ihm_uuid: str
    loss: np.ndarray


def ihm_success(num_features: int):
    time_taken = np.random.rand()
    gradient = np.random.rand(num_features)
    ihm_uuid = str(uuid.uuid4())  # TASK 1
    loss = np.random.randint(1, 100) / 100
    return IHM(gradient, time_taken * 10, ihm_uuid, loss)


def ihm_failure():
    return None


def map_func(ihm_list: List[IHM], func_to_map: Callable):  # Task 2
    return list(map(func_to_map, ihm_list))


def filter_by_func(ihm_list: List[IHM], func_to_filter_with: Callable):  # Task 3
    return list(filter(func_to_filter_with, ihm_list))


def prototype(num_ihms: int, crash_proba: float, num_features: int):
    import copy
    def func_to_map(ihm: IHM, key: str) -> IHM:
        new_x = copy.deepcopy(ihm)
        setattr(new_x, key, np.random.choice([True, False]))
        return new_x

    def func_to_filter(ihm: IHM) -> bool:
        return ihm.keep

    ihm_results = simulate_ihm(num_ihms, crash_proba, num_features)
    print(f"Length of original: {len(ihm_results)}")
    mapped_over = map_func(ihm_results, lambda x: func_to_map(x, "keep"))
    filtered_out = filter_by_func(mapped_over, lambda x: func_to_filter(x))
    print(f"Length of filtered: {len(filtered_out)}")


################################################
# Unnecessary to read
################################################


def simulate_ihm(
    num_ihms: int,
    prob_ihm_crash: float,
    num_features: int
) -> List:
    ihm_results = []
    for i in range(num_ihms):
        if np.random.random() < prob_ihm_crash:
            ihm_results.append(ihm_failure())
        else:
            ihm_results.append(ihm_success(num_features))
    return ihm_results
