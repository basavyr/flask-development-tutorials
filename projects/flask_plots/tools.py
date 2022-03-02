from dataclasses import dataclass
from datetime import datetime


def get_current_time():
    return f'{datetime.utcnow()}'


def get_node_list():
    node_list = [f'node-{idx}' for idx in range(6)]

    return node_list
