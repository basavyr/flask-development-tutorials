import os


def show_system_info():
    return os.uname()


def main():
    x=show_system_info()
    print(x)

if __name__=='__main__':
    main()