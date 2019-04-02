from utility import *
import javalang
import random
from random import shuffle
from keras.models import load_model
from keras.preprocessing.text import Tokenizer


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


def flatten(chunk):
    tokens = tokenize(chunk)
    return str([" ".join(token.value for token in tokens)][0])


def tokenize(contents):
    return javalang.tokenizer.tokenize(contents)


def get_method_name(flat_string):
    flat_string = flat_string.split(" ")
    for x in range(len(flat_string)):
        if flat_string[x] == "(":
            return flat_string[x-1]


def collect_data(data_path):
    suite = JavaJulietSuite(data_path)
    suite.write_good()
    suite.write_bad()


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
    def __init__(self, test_suite_location, ):
        list_of_paths = get_files(test_suite_location, "java")[1:]
        self.files = []
        for path in list_of_paths:
            print(path)
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
    def __init__(self):
        self.tok = Tokenizer(num_words=MAX_WORDS)
        df = pd.read_csv(os.path.dirname(__file__) + '/data/java_balanced_data.csv')
        self.tok.fit_on_texts(df.input)

    def embed(self, flat_method):
        sequences = self.tok.texts_to_sequences([flat_method])
        sequences_matrix = sequence.pad_sequences(sequences, maxlen=MAX_LEN)
        return sequences_matrix

    @staticmethod
    def execute_routine(files, h5_loc):
        f, javal = Logger(), Javalect()
        model = load_model(h5_loc)
        for file in files:
            try:
                f.log("Analyzing " + file + ":")
                contents = JavaJuliet.java_file_cleaner(file)
                for chunk in chunker(contents):
                    method = flatten(chunk)

                    # Filter non-methods from chunks
                    if method.split(" ")[0] in ["public", "private"]:
                        focus = " " + get_method_name(method) + "()"
                        x = javal.embed(method)
                        pred = model.predict(x)[0][0]
                        f.log_prediction(focus, pred)
            except:
                pass
        f.write()

    @staticmethod
    def prepare_corpus(language, method_names="preserve", mode="w"):
        g = read_data("good", language)
        b = read_data("bad", language)
        ls_g, ls_b = [], []
        for good in g:
            for chunk in chunker(good):
                target = flatten(chunk)
                tokens = target.split(" ")
                if tokens[0] in ["public", "private"]:
                    if method_names == "random":
                        tokens[2] = str(random.randint(1000000, 9999999))
                    elif method_names == "uniform":
                        tokens[2] = "someMethod"
                    target = " ".join(tokens)
                    ls_g.append([target, "0"])
                    print([target, "0"])
        for bad in b:
            for chunk in chunker(bad):
                target = flatten(chunk)
                tokens = target.split(" ")
                if tokens[0] in ["public", "private"]:
                    if method_names == "random":
                        tokens[2] = str(random.randint(1000000, 9999999))
                    elif method_names == "uniform":
                        tokens[2] = "someMethod"
                    target = " ".join(tokens)
                    ls_b.append([target, "1"])
                    print([target, "1"])
        size = min(len(ls_g), len(ls_b))
        ls = ls_g[:size] + ls_b[:size]
        shuffle(ls)
        with open(os.path.dirname(__file__) + "/data/" + language + "_balanced_data.csv", mode) as h:
            writer = csv.writer(h)
            writer.writerows([["input", "label"]] + ls)
        h.close()

    @staticmethod
    def scrape_corpus(test_suite_location, write_loc="<poliarty>.txt"):
        jjs = JavaJulietSuite(test_suite_location)
        jjs.write_good(write_loc.replace("<polarity>", "good"))
        jjs.write_bad(write_loc.replace("<polarity>", "bad"))
