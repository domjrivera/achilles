# No longer necessary, corpus has been cleaned up.

# import os
# import fnmatch
#
#
# def get_files(path, language="java"):
#     ls = []
#     for root, _, files in os.walk(path):
#         for item in fnmatch.filter(files, "*"):
#             extension_mark = find_occurrences(item, ".")
#             if len(extension_mark) > 0:
#                 extension_mark = extension_mark[-1]
#                 if item[extension_mark:] in languages[language]:
#                     ls.append(root + "/" + item)
#     return [language] + list(set(ls))
#
#
#
# class JavaJulietSuite:
#     def __init__(self, test_suite_location):
#         list_of_paths = get_files(test_suite_location, "java")[1:]
#         self.files = []
#         for path in list_of_paths:
#             print(path)
#             self.files.append(JavaJuliet(path))
#
#     def get_good(self):
#         ls = []
#         for file in self.files:
#             ls.extend(file.good)
#         return ls
#
#     def get_bad(self):
#         ls = []
#         for file in self.files:
#             ls.extend(file.bad)
#         return ls
#
#     def get_chunks(self):
#         return self.get_good() + self.get_bad()
#
#     def write_good(self, location="good.txt"):
#         good, s = self.get_good(), ""
#         for g in good:
#             s = s + g + "\n\n\n\n\n"
#         file_object = open(location, "w")
#         file_object.write(s)
#         file_object.close()
#
#     def write_bad(self, location="bad.txt"):
#         bad, s = self.get_bad(), ""
#         for g in bad:
#             s = s + g + "\n\n\n\n\n"
#         file_object = open(location, "w")
#         file_object.write(s)
#         file_object.close()
#
#
# class JavaJuliet:
#     def __init__(self, path):
#         self.contents = JavaJuliet.java_file_cleaner(path)
#         self.chunks = chunker(self.contents)
#         self.good, self.bad = self.good_bad_separator()
#
#     def __str__(self):
#         return self.contents
#
#     def chunks(self):
#         return iter(self.chunks)
#
#     def good_bad_separator(self):
#         g, b = [], []
#         for chunk in self.chunks:
#             split_chunks, signature = chunk.split("\n"), None
#             for line in split_chunks:
#                 if "{" in line:
#                     signature = line
#                     break
#             if signature is None:
#                 pass
#             elif "good" in signature:
#                 g.append(chunk)
#             elif "bad" in signature:
#                 b.append(chunk)
#         return g, b
#
#     @staticmethod
#     def java_file_cleaner(file_loc):
#         c = read_file(file_loc)
#         c = JavaJuliet._comment_stripper(c)
#         c = JavaJuliet._crush(c)
#         c = JavaJuliet._allman_to_knr(c)
#         return c
#
#     @staticmethod
#     def _comment_stripper(string):
#         if "/*" not in string:
#             return string
#         s, t = string.index("/*"), string.index("*/")
#         return JavaJuliet._comment_stripper(string.replace(string[s:t + 2], ""))
#
#     @staticmethod
#     def _crush(string):
#         string = string.split("\n")
#         s = ""
#         for line in string:
#             line = line.rstrip()
#             if len(line.lstrip()) != 0:
#                 s = s + line + "\n"
#         return s
#
#     @staticmethod
#     def _allman_to_knr(string):
#         string, s = string.split("\n"), []
#         for i in range(len(string)):
#             if string[i].strip() == "{":
#                 string[i - 1] = string[i - 1] + " {"
#                 string[i] = ""
#         for i in range(len(string)):
#             if len(string[i].strip()) > 0:
#                 if string[i].strip()[-1] == ",":
#                     string[i] = string[i] + " " + string[i + 1].lstrip()
#                     string[i + 1] = ""
#         while "" in string:
#             string.remove('')
#         string = "\n".join(string)
#         string = string.replace("}", "}\n")
#         return string
#
#
# @staticmethod
# def prepare_corpus(language, method_names="preserve", mode="w"):
#     g = read_data("good", language)
#     b = read_data("bad", language)
#     ls_g, ls_b = [], []
#     for good in g:
#         for chunk in chunker(good):
#             target = flatten(chunk)
#             tokens = target.split(" ")
#             if tokens[0] in ["public", "private"]:
#                 if method_names == "random":
#                     tokens[2] = str(random.randint(1000000, 9999999))
#                 elif method_names == "uniform":
#                     tokens[2] = "someMethod"
#                 target = " ".join(tokens)
#                 ls_g.append([target, "0"])
#                 print([target, "0"])
#     for bad in b:
#         for chunk in chunker(bad):
#             target = flatten(chunk)
#             tokens = target.split(" ")
#             if tokens[0] in ["public", "private"]:
#                 if method_names == "random":
#                     tokens[2] = str(random.randint(1000000, 9999999))
#                 elif method_names == "uniform":
#                     tokens[2] = "someMethod"
#                 target = " ".join(tokens)
#                 ls_b.append([target, "1"])
#                 print([target, "1"])
#     size = min(len(ls_g), len(ls_b))
#     ls = ls_g[:size] + ls_b[:size]
#     shuffle(ls)
#     with open(os.path.dirname(__file__) + "/data/" + language + "_balanced_data.csv", mode) as h:
#         writer = csv.writer(h)
#         writer.writerows([["input", "label"]] + ls)
#     h.close()