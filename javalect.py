import javalang
from model import *
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


def collect_data(data_path):
    suite = JavaJulietSuite(data_path)
    suite.write_good()
    suite.write_bad()


# Maps each token to value uniquely.
def keymap(tokens, clean_primitives=True):
    d, i = dict(), 0
    ls = set([token.value for token in tokens])
    if clean_primitives:
        sanitize(ls)
    for token in ls:
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


class JavaJulietSuite:
    def __init__(self, test_suite_location):
        list_of_paths = get_files(test_suite_location)[1:]
        self.files = []
        for path in list_of_paths:
            self.files.append(JavaJuliet(path))

    def get_good(self):
        ls = []
        for file in self.files:
            ls.extend(file.good)
        return ls

    def get_bad(self):
        ls = []
        for file in self.files:
            ls.extend(file.bad)
        return ls

    def get_chunks(self):
        return self.get_good() + self.get_bad()

    def write_good(self, location="good.txt"):
        good, s = self.get_good(), ""
        for g in good:
            s = s + g + "\n\n\n\n\n"
        file_object = open(location, "w")
        file_object.write(s)
        file_object.close()

    def write_bad(self, location="bad.txt"):
        bad, s = self.get_bad(), ""
        for g in bad:
            s = s + g + "\n\n\n\n\n"
        file_object = open(location, "w")
        file_object.write(s)
        file_object.close()


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
    def execute_routine(files):
        f = Logger()
        for file in files:
            contents = JavaJuliet.java_file_cleaner(file)
            chunks = chunker(contents)
            for chunk in chunks:
                f.log("Analyzing" + file)
                tokens = tokenize(chunk)

