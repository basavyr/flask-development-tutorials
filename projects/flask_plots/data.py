
import random

import psutil

_MIN_NUMBER = 5
_MAX_NUMBER = 35
_SUMM = 100


def get_swap_info():
    swap_info = psutil.swap_memory()

    memory = {
        "total": swap_info.total,
        "used": swap_info.used,
        "free": swap_info.free,
        "percent": swap_info.percent,
    }

    return memory


def get_random_number():
    """ Generates a random number between [5 and 35]"""
    rd_n = random.randrange(_MIN_NUMBER, _MAX_NUMBER)
    return rd_n


def generate_array_fixed_number(total_size, total_sum):
    checker = True

    array = []

    array_sum = 0

    array_size = 0

    while checker:
        rng = get_random_number()
        if(array_sum + rng <= total_sum):
            array.append(rng)
            arr_size = len(array)
            array_sum = sum(array)

            if(arr_size == total_size):
                if(array_sum <= total_sum):
                    array.pop()
                    final_term = total_sum - sum(array)
                    array.append(final_term)
                    array_sum = sum(array)
                checker = False
        else:
            safety_rng = total_sum - array_sum
            array.append(safety_rng)
            array_sum = sum(array)
            checker = False

    return array, array_sum


def generate_data():
    rand_number = lambda: random.randrange(1, 15)
    data_size = 100
    y_data = [rand_number() for _ in range(data_size)]
    x_data = [idx + 1 for idx in range(data_size)]

    return [x_data, y_data]
