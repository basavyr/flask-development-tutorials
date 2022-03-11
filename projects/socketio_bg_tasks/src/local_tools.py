import platform
import psutil


def get_uname():
    return f'{platform.uname()}'


def main():
    get_uname()


if __name__ == '__main__':
    main()
