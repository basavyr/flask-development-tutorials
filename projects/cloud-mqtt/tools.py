import time
from datetime import date, datetime
import os


def show_system_info():
    return os.uname()


def detalied_info_stats():
    stats = show_system_info()
    my_dict = {"machine": stats.machine,
               "user": stats.nodename,
               "system": stats.sysname,
               "root": stats.release, }

    return my_dict


def get_time():
    return datetime.utcnow()


def main():
    x = detalied_info_stats()
    for key in x:
        print(x[key])


if __name__ == '__main__':
    main()
