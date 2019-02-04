import javalang
from utility import *


__primitive_types__ = {"Literal": "<lit>",
                       "Integer": "<int>",
                       "DecimalInteger": "<byte>",
                       "OctalInteger": "<oct>",
                       "BinaryInteger": "<bint>",
                       "HexInteger": "<hexint>",
                       "FloatingPoint": "<float>",
                       "DecimalFloatingPoint": "<double>",
                       "HexFloatingPoint": "<hexfloat",
                       "Boolean": "<bool>",
                       "Character": "<char>",
                       "String": "<str>",
                       "Null": "<null>"}


def tokenize(contents):
    return javalang.tokenizer.tokenize(contents)


# Maps each token to value uniquely.
def keymap(tokens, clean_primitives=True):
    d, i = dict(), 0
    ls = set([token.value for token in tokens])
    if clean_primitives:
        sanitize(ls)
    for token in ls:
        print(token, i)
        d[token] = i
        i += 1
    return d, {v: k for k, v in d.items()}


def sanitize(token_list):
    for token in token_list:
        dtype = str(token.__class__).replace("<class 'javalang.tokenizer.", "").replace("'>", "")
        if dtype in __primitive_types__:
            token = __primitive_types__[dtype]
    return token_list


def chunker():
    pass


class Javalect:
    @staticmethod
    def execute_routine(file):
        # Read File
        contents = read_file(file)
        # contents = contents.split("\n")
        tokens = tokenize(contents)
        comp_unit = javalang.parse.parse(contents)
        i = 1
        for x, y in comp_unit:
            print(i, x)
            i += 1
        # Chunker

        # Sanitize

        # Tokenize


        # Feed LSTM
        # contents = read_file("Test.java")
        # for token in tokens:
        #     print(token)
        # fwd_map, rev_map = keymap(tokens)

        # for k, v in fwd_map:
        #     print(k, v)

        # parser = javalang.parser.Parser(tokens)
        # for node, path in comp_unit:
        #     print(path)
        # x = parser.parse()

