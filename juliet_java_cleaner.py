from javalect import *


class JulietFile:
    def __init__(self, path):
        self.contents = read_file(path)
        self.chunks = chunker(self.contents)
        self.metadata = self.extract_metadata()
        self.good, self.bad = self.good_bad_sorter()

    def good_bad_sorter(self):
        good, bad = [], []
        for chunk in self.chunks:
            chunk_data = chunk.strip().split("\n")[0]
            if "good" in chunk_data:
                good.append(self.clean_block_comments(chunk))
            elif "bad" in chunk_data:
                bad.append(self.clean_block_comments(chunk))

        return good, bad

    def clean_block_comments(self, string):
        if string.count("/*") == 0:
            print(string)
            return string
        s, t = string.index("/*"), string.index("*/")
        newline = find_occurrences(string[:s], "\n")[-1]
        subst = string[newline+1: t+3]
        return self.clean_block_comments(string.replace(subst, ""))

    def extract_metadata(self):
        header = self.chunks[0]
        del self.chunks[0]
        self.chunks = chunker(header) + self.chunks
        meta = self.chunks[0].split("\n")

        i = 0
        for x in range(len(meta)):
            line = meta[x]
            if " * */" in line:
                i = x + 1
                break
        self.chunks[0] = self.chunks[0].replace("\n".join(meta[:i]), "")
        meta = meta[:i]

        for x in range(len(meta)):
            line = meta[x]
            if "@description" in line:
                i = x + 1
                break

        meta = [meta[:i][1]] + meta[i:]
        meta_out = []
        for line in meta:
            temp = line.replace("*", "").replace("/", "").strip()
            if len(temp) > 0:
                meta_out.append(temp)
        return "\n".join(meta_out)


p = "juliet_java/CWE15_External_Control_of_System_or_Configuration_Setting/CWE15_External_Control_of_System_or_Configuration_Setting__connect_tcp_01.java"
h = JulietFile(p)

# for file in files:
#     print(file.split("/")[1:])
#     print(read_file(file))
