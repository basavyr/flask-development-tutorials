from datetime import datetime
import psutil
import platform


GBYTES = 1024 * 1024 * 1024  # transform memory in gbytes


def get_timestamp():
    return f'{datetime.utcnow()}'


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


def get_platform_arch():
    arch = platform.architecture()[0]
    processor = platform.processor()

    return f'{processor}-{arch}'


def get_node_name():
    node_name = platform.node()

    return f'{node_name}'


def get_sys_info():
    labels = [x for x in platform.uname()._fields]
    # print(labels)

    sys_info = [x for x in platform.uname() if x != '']
    # print(sys_info)

    data_dict = {f'{labels[idx]}': sys_info[idx]
                 for idx in range(len(sys_info))}
    # print(data_dict)
    return data_dict


def main():
    print(f'SWAP: {get_swap_info()}')
    print(f'VMEM: {get_virtual_memory_info()}')
    print(f'DISK: {get_disk_info()}')
    print(f'CPU: usage:{get_cpu_info()[0]} cpu_count:{get_cpu_info()[1]} ')
    print(f'ARCH: {get_platform_arch()}')
    print(f'SYS_INFO: {get_sys_info()}')


if __name__ == '__main__':
    main()
