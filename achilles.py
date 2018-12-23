from utility import *


def main():
    files, lang = get_cmd_args()
    for file in files:
        print("  " + file)


if __name__ == "__main__":
    main()
