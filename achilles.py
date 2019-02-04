from utility import *
from javalect import *


def main():
    # files, lang = get_cmd_args()
    files, lang = ["Test.java"], "java"  # Use while testing

    print("\x1b[36mEvaluating the following files:\x1b[m")
    for file in files:
        print("  ", file)
    #
    # if lang == "java":
    #     for file in files:
    #         Javalect.execute_routine(file)


if __name__ == "__main__":
    main()
