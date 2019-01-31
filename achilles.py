from utility import *
from javalect import *


def main():
    # Comment out bash input for now.
    # files, lang = get_cmd_args()
    # for file in files:
    #     print(file)



    contents = read_file("Test.java")
    tokens = tokenize(contents)
    # for token in tokens:
    #     print(token)
    fwd_map, rev_map = keymap(tokens)

    # for k, v in fwd_map:
    #     print(k, v)

    # parser = javalang.parser.Parser(tokens)
    # comp_unit = javalang.parse.parse(contents)
    # for node, path in comp_unit:
    #     print(path)
    # x = parser.parse()


if __name__ == "__main__":
    main()
