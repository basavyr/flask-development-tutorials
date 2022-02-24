from re import L
import time
from datetime import date, datetime
import os
import psutil


Gbytes = pow(10, 9)


def show_system_info():
    return os.uname()


def detalied_info_stats():
    stats = show_system_info()
    my_dict = {"machine": stats.machine,
               "user": stats.nodename,
               "system": stats.sysname,
               "root": stats.release, }

    return my_dict


def show_disk_info():
    disk_partitions = [p.device for p in psutil.disk_partitions()]
    disk_usage = psutil.disk_usage('/').percent

    return [disk_partitions, disk_usage]


def show_MEM_info():
    # MEM
    virtual_memory = psutil.virtual_memory()
    virt_memory = {
        "total": float(virtual_memory.total / Gbytes),
        "used": float(virtual_memory.used / Gbytes),
        "percentage": virtual_memory.percent,
    }

    return virt_memory


def show_SWAP_info():
    swap_memory = psutil.swap_memory()
    swap_memory = {
        "total": float(swap_memory.total / Gbytes),
        "used": float(swap_memory.used / Gbytes),
        "percentage": swap_memory.percent,
    }

    return swap_memory


def show_CPU_info():
    # CPU
    cpu_count = psutil.cpu_count()
    cpugetloadavg = psutil.getloadavg()
    cpu_times = {
        "cpu-count": cpu_count,
        "load-average": cpugetloadavg,
        "cpu-percent": psutil.cpu_percent(),
        "cpu-freq": psutil.cpu_freq().current,
    }

    return cpu_times


def get_time():
    return datetime.utcnow()


def main():
    cpu = show_MEM_info()
    print(cpu)


if __name__ == '__main__':
    main()
