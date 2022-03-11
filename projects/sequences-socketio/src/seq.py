import random


def get_sequence():
    rd_limit = random.randrange(10, 40)
    sequence = [random.choice([1, 0]) for _ in range(rd_limit)]

    return sequence
