from utility import *
from javalect import *


def main():
    # files, lang = get_cmd_args()
    files = ["/Volumes/CoreBlue/Programming/Projects/swe_research/Java/src/testcases/CWE15_External_Control_of_System_or_Configuration_Setting/CWE15_External_Control_of_System_or_Configuration_Setting__connect_tcp_01.java"]
    lang = "java"
    for file in files:
        print(file)


if __name__ == "__main__":
    main()
