import psutil
import platform
from datetime import datetime


def get_uname():
    return f'{platform.uname()}'


def get_time():
    return f'{str(datetime.utcnow())[:-7]}'


def main():
    uname = get_uname()
    time = get_time()
    print(f'{time}')


if __name__ == '__main__':
    main()
