import random


def get_sequence():
    rd_limit = random.randrange(10, 40)
    sequence = [int(random.choice([1, 0])) for _ in range(rd_limit)]

    return sequence


def process_sequence(sequence):
    raw_sequence = str(sequence).strip().split(',')
    seq = [int(x) for x in raw_sequence]
    sum_seq = sum_sequence(seq)
    print(sum_seq)


def sum_sequence(sequence):
    return sum(sequence)
