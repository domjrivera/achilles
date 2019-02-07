import javalang
from utility import *


_primitive_types = {"Literal": "<lit>",
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


# Debating whether ENUM should be ignored...
_blocks = ["enum",
           "finally",
           "catch",
           "do",
           "else",
           "for",
           "if",
           "try",
           "while",
           "switch",
           "synchronized"]


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
        if dtype in _primitive_types:
            token = _primitive_types[dtype]
    return token_list


def is_valid_chunk(s):
    first_line = s.strip().split("\n")[0]
    for block in _blocks:
        if block in first_line:
            return False
    return True


def chunker(contents):
    guide, chunks = "", []
    contents = contents.replace("\r\n", "\n")
    l_braces = find_occurrences(contents, "{")
    r_braces = find_occurrences(contents, "}")

    # Build a string to guide chunking process.
    for line in contents:
        if "{" in line:
            guide += "{"
        elif "}" in line:
            guide += "}"

    # This assumes that every opening brace has a closer.
    for _ in range(int(len(guide)/2) - 1):
        # This assumes that the first occurrence of a "}" will be prefixed by a "{".
        i = guide.find("}")
        l, r = l_braces[i-1], r_braces[0]
        l_braces.remove(l)
        r_braces.remove(r)
        ln = contents[0:l].rfind("\n")
        temp = contents[ln:r+1]
        if is_valid_chunk(temp):
            chunks.append(temp)
        guide = guide.replace("{}", "", 1)

    for chunk in chunks:
        contents = contents.replace(chunk, "")
    return [contents] + chunks


class Javalect:
    @staticmethod
    def execute_routine(file):
        # === Read File
        contents = read_file(file)

        # === Chunker
        chunks = chunker(contents)
        # for chunk in chunks:
        #     print(chunk)
        #     print("\n\n\n\n\n")

        # === Sanitize


        # === Tokenize

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

