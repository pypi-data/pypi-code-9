import numpy as np


round_number = lambda x: int(round(abs(x)))


def get_percent_change(new_value, old_value):
    if not old_value:
        return np.sign(new_value) * np.inf
    change_difference = new_value - old_value
    change_ratio = change_difference / float(old_value)
    return 100 * change_ratio
