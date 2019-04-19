import javalang
import re
import os


class JavaClass:
    def __init__(self, path):
        self.src = JavaClass._extract_code(path)
        self.methods = JavaClass.chunker(self.src)
        self.method_names = [method.method_name for method in self.methods]

    def __iter__(self):
        return iter(self.methods)

    @staticmethod
    def _extract_code(path):
        with open(path, 'r') as content_file:
            contents = content_file.read()
            contents = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", contents)
            contents = re.sub(re.compile("//.*?\n"),  "", contents)
            return contents

    def tokens(self):
        tokens = javalang.tokenizer.tokenize(self.src)
        return [" ".join(token.value for token in tokens)][0]

    @staticmethod
    def find_occurrences(s, ch):
        return [i for i, letter in enumerate(s) if letter == ch]

    @staticmethod
    def chunker(contents):
        s, temp = contents, len(contents)
        regex = r"(public|protected|private|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *(\{?|[^;])"
        ls, chunks = [], []
        while re.search(regex, contents):
            match = re.search(regex, contents)
            contents = (" "*match.end()) + contents[match.end():]
            ls.append(match.start())
        ls.append(temp)
        for x in range(len(ls) - 1):
            chunks.append(s[ls[x]:ls[x+1]])
        chunks[-1] = "}".join(chunks[-1].split("}")[:-1])
        return chunks


class JavaMethod:
    def __init__(self, chunk, polarity="?", risk=-1):
        self.method = chunk
        self.method_name = self.method[:self.method.find("(")].split()[-1]
        self.polarity = polarity
        self.risk = risk

    def tokens(self):
        tokens = javalang.tokenizer.tokenize(self.method)
        return [" ".join(token.value for token in tokens)][0]

    def __str__(self):
        return self.method

    def __iter__(self):
        tokens = javalang.tokenizer.tokenize(self.method)
        return iter([tok.value for tok in tokens])


class CWE4J:
    def __init__(self, root):
        self.data = {}
        self.root = root
        for directory in os.listdir(root):
            self.add(directory)

    def add(self, filepath):
        vuln_name = filepath.split("__")[0]
        if vuln_name in self.data.keys():
            self.data[vuln_name].append(self.root + "/" + filepath)
        else:
            self.data[vuln_name] = [self.root + "/" + filepath]

    def __iter__(self):
        return iter(self.data.keys())

    def __getitem__(self, item):
        return self.data[item]

    def __len__(self):
        return len(self.data.keys())


class Javalect:
    @staticmethod
    def train_models(path, threshold=0):
        cwe4j = CWE4J(path)
        for cwe in cwe4j:
            if len(cwe4j[cwe]) >= threshold:
                Javalect._format_corpus(cwe4j[cwe])

    @staticmethod
    def _format_corpus(cwe_list):
        ls = []
        for cwe_path in cwe_list:
            j = JavaClass(cwe_path)


#     def __init__(self):
#         self.tok = Tokenizer(num_words=MAX_WORDS)
#         df = pd.read_csv(os.path.dirname(__file__) + '/data/java_balanced_data.csv')
#         self.tok.fit_on_texts(df.input)
#
#     def embed(self, flat_method):
#         sequences = self.tok.texts_to_sequences([flat_method])
#         sequences_matrix = sequence.pad_sequences(sequences, maxlen=MAX_LEN)
#         return sequences_matrix
#
#     @staticmethod
#     def execute_routine(files, h5_loc, log_write=False):
#         f, javal = Logger(), Javalect()
#         model = load_model(h5_loc)
#         for file in files:
#             try:
#                 f.log("Analyzing " + file + ":")
#                 contents = JavaJuliet.java_file_cleaner(file)
#                 for chunk in chunker(contents):
#                     method = flatten(chunk)
#
#                     # Filter non-methods from chunks
#                     if method.split(" ")[0] in ["public", "private"]:
#                         focus = " " + get_method_name(method) + "()"
#                         x = javal.embed(method)
#                         pred = model.predict(x)[0][0]
#                         f.log_prediction(focus, pred)
#             except:
#                 pass
#         if log_write:
#             f.write()
#


Javalect.train_models("/Users/Strickolas/Downloads/CWE", threshold=7015)

