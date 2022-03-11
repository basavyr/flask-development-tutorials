import platform
import psutil


def get_uname():
    return f'{platform.uname()}'


def generate_vm_list():
    return [f'vm-{idx}' for idx in range(5)]


def main():
    get_uname()


if __name__ == '__main__':
    main()
