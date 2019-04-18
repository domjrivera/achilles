from keras.models import load_model
from keras.preprocessing.text import Tokenizer
import javalang
import re


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
        r_brace = JavaClass.find_occurrences(contents, "}")
        l_brace = JavaClass.find_occurrences(contents, "{")
        tokens = javalang.tokenizer.tokenize(contents)
        guide, chunks = "", []
        _blocks = ["enum", "finally", "catch", "do", "else", "for",
                   "if", "try", "while", "switch", "synchronized"]

        for token in tokens:
            if token.value in ["{", "}"]:
                guide += token.value

        while len(guide) > 0:
            i = guide.find("}")
            l, r = l_brace[i - 1], r_brace[0]
            l_brace.remove(l)
            r_brace.remove(r)

            ln = contents[0:l].rfind("\n")
            chunk = contents[ln:r + 1]
            if chunk.split()[0] in ["public", "private", "protected"]:
                chunks.append(JavaMethod(chunk))
            guide = guide.replace("{}", "", 1)
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

#
# class Javalect:
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
