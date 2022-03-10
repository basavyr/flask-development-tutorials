import psutil
import platform


def get_uname():
    return f'{platform.uname()}'


def main():
    uname = get_uname()
    print(uname)


if __name__ == '__main__':
    main()
