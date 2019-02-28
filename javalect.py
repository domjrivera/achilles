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
        # print(token, i)
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
    for _ in range(int(len(guide) / 2) - 1):
        # This assumes that the first occurrence of a "}" will be prefixed by a "{".
        i = guide.find("}")
        l, r = l_braces[i - 1], r_braces[0]
        l_braces.remove(l)
        r_braces.remove(r)
        ln = contents[0:l].rfind("\n")
        temp = contents[ln:r + 1]
        if is_valid_chunk(temp):
            chunks.append(temp)
        guide = guide.replace("{}", "", 1)

    for chunk in chunks:
        contents = contents.replace(chunk, "")
    return [contents] + chunks


class JavaJuliet:
    def __init__(self, path):
        self.contents = JavaJuliet.java_file_cleaner(path)
        self.chunks = chunker(self.contents)
        self.good, self.bad = self.good_bad_separator()

    def __str__(self):
        return self.contents

    def chunks(self):
        return iter(self.chunks)

    def good_bad_separator(self):
        g, b = [], []
        for chunk in self.chunks:
            split_chunks, signature = chunk.split("\n"), None
            for line in split_chunks:
                if "{" in line:
                    signature = line
                    break
            if signature is None:
                pass
            elif "good" in signature:
                g.append(chunk)
            elif "bad" in signature:
                b.append(chunk)
        return g, b

    @staticmethod
    def java_file_cleaner(file_loc):
        c = read_file(file_loc)
        c = JavaJuliet._comment_stripper(c)
        c = JavaJuliet._crush(c)
        c = JavaJuliet._allman_to_knr(c)
        return c

    @staticmethod
    def _comment_stripper(string):
        if "/*" not in string:
            return string
        s, t = string.index("/*"), string.index("*/")
        return JavaJuliet._comment_stripper(string.replace(string[s:t + 2], ""))

    @staticmethod
    def _crush(string):
        string = string.split("\n")
        s = ""
        for line in string:
            line = line.rstrip()
            if len(line.lstrip()) != 0:
                s = s + line + "\n"
        return s

    @staticmethod
    def _allman_to_knr(string):
        string, s = string.split("\n"), []
        for i in range(len(string)):
            if string[i].strip() == "{":
                string[i - 1] = string[i - 1] + " {"
                string[i] = ""
        for i in range(len(string)):
            if len(string[i].strip()) > 0:
                if string[i].strip()[-1] == ",":
                    string[i] = string[i] + " " + string[i + 1].lstrip()
                    string[i + 1] = ""
        while "" in string:
            string.remove('')
        string = "\n".join(string)
        string = string.replace("}", "}\n")
        return string


class Javalect:
    @staticmethod
    def execute_routine(file):
        # === Read File
        contents = read_file(file)

        # === Chunker
        chunks = chunker(contents)
        v = "\x1b[34m\"\x1b[m"
        # for chunk in chunks:
        #     print(v, chunk, v)
        #     print("\n\n\n\n\n")

        # === Sanitize

        # === Tokenize

        # === Feed LSTM


f = "juliet_java/CWE698_Redirect_Without_Exit/CWE698_Redirect_Without_Exit__Servlet_03.java"
jj = JavaJuliet(f)