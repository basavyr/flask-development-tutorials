
import random

import os
import psutil
import platform

_MIN_NUMBER = 5
_MAX_NUMBER = 35
_SUMM = 100

GBYTES = 1024 * 1024 * 1024  # transform memory in gbytes


def get_swap_info():
    swap_info = psutil.swap_memory()

    memory = {
        "total": round(swap_info.total / GBYTES, 2),
        "available": round(swap_info.free / GBYTES, 2),
        "used": round(swap_info.used / GBYTES, 2),
        "percent": swap_info.percent,
    }

    return memory


def get_virtual_memory_info():
    mem_info = psutil.virtual_memory()

    memory = {
        "total": round(mem_info.total / GBYTES, 2),
        "available": round(mem_info.available / GBYTES, 2),
        "used": round(mem_info.used / GBYTES, 2),
        "percent": mem_info.percent,
    }

    return memory


def get_disk_info():
    disk_info = psutil.disk_usage('/')

    disk = {
        "total": round(disk_info.total / GBYTES, 2),
        "available": round(disk_info.free / GBYTES, 2),
        "used": round(disk_info.used / GBYTES, 2),
        "percent": disk_info.percent,
    }

    return disk


def get_cpu_info():
    n_cpus = psutil.cpu_count()
    load_average = [round(load * 100 / n_cpus, 2)
                    for load in psutil.getloadavg()]

    return load_average, n_cpus


def get_random_number():
    """ Generates a random number between [_MIN_NUMBER and _MAX_NUMBER]"""
    rng = random.randrange(_MIN_NUMBER, _MAX_NUMBER)
    return rng


def generate_data():
    rand_number = lambda: random.randrange(1, 15)
    data_size = 100
    y_data = [rand_number() for _ in range(data_size)]
    x_data = [idx + 1 for idx in range(data_size)]

    return [x_data, y_data]


def get_platform_arch():
    arch = platform.architecture()[0]
    processor = platform.processor()

    return f'{processor}-{arch}'


def get_node_name():
    node_name = platform.node()

    return f'{node_name}'


def get_sys_info():
    sys_info = platform.uname()

    return sys_info


def main():
    print(f'SWAP: {get_swap_info()}')
    print(f'VMEM: {get_virtual_memory_info()}')
    print(f'DISK: {get_disk_info()}')
    print(f'CPU: usage:{get_cpu_info()[0]} cpu_count:{get_cpu_info()[1]} ')
    print(f'ARCH: {get_platform_arch()}')


if __name__ == '__main__':
    main()
