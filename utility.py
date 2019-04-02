from javalect import *
from model import *
import os
import csv
import argparse
import re
import datetime
import fnmatch


def read_file(path):
    with open(path, 'r') as content_file:
        return content_file.read()


def get_cmd_args():
    parser = argparse.ArgumentParser(description='Parse input string')
    parser.add_argument('goals', help='HELP!', nargs='+')
    args = parser.parse_args()
    goals = ' '.join(args.goals).replace(",", " ").split(" ")
    ls = parse_cmd_args(goals)
    if len(ls) == 1:
        print("No compatible files found.")
        quit(0)
    if len(ls) > 100:
        while True:
            ans = input("Found " + str((len(ls) - 1)) + " " + ls[0] + " files. Do you want to continue? [y]es, [n]o: ")
            if "y" == ans.lower():
                break
            elif "n" == ans.lower():
                quit()
    print(version_info)
    return ls[1:], ls[0]


# Courtesy of Marco L. on Stack Overflow
def find_occurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def parse_cmd_args(goals):
    try:
        # Get version information.
        if goals[0].lower() == "version":
            print(version_info)
            quit()

        # Evaluate a single file.
        elif os.path.isfile(goals[0]):
            for language in languages.keys():
                for extension in languages[language]:
                    if extension == goals[0][-len(extension):]:
                        return [language, os.getcwd() + goals[0]]
            # If there isn't language support, default to Java.
            return ["java", os.getcwd() + goals[0]]

        # Re-process & balance <language>_<polarity>.txt files
        elif goals[0] == "balance":
            try:
                if goals[1] == "java":
                    try:
                        Javalect.prepare_corpus("java", goals[2])
                    except:
                        Javalect.prepare_corpus("java", "random")
                quit()
            except:
                print("Invalid arguments.")
                quit()

        # Evaluate a file or folder using a specified language.
        elif goals[0].lower() in languages:
            if len(goals) == 2:
                # Evaluate all files of a certain language in folder.
                if os.path.isdir(goals[1]):
                    return get_files(goals[1], goals[0])
                # Evaluate a single file.
                elif os.path.isfile(goals[1]):
                    return [goals[0].lower, goals[1]]
            elif len(goals) == 1:
                # Evaluate all files in the current directory.
                return get_files(os.getcwd(), goals[0].lower())

        # Train neural network.
        elif goals[0].lower() == "train":
            if goals[1].lower() not in languages.keys():
                print("No language support for " + goals[1] + ".")
                quit(0)
            try:
                print("Training model.")
                AchillesModel.train(goals[1])
                quit()
            except:
                print("Unable to locate training data: data/" + goals[0] + "_data.csv")
                quit()
        else:
            print("Invalid arguments.")
            quit()
    except:
        quit()


def get_files(path, language="java"):
    ls = []
    for root, _, files in os.walk(path):
        for item in fnmatch.filter(files, "*"):
            extension_mark = find_occurrences(item, ".")
            if len(extension_mark) > 0:
                extension_mark = extension_mark[-1]
                if item[extension_mark:] in languages[language]:
                    ls.append(root + "/" + item)
    return [language] + list(set(ls))


def read_data(polarity, language="java"):
    return read_file(os.path.dirname(__file__) + "/data/" + language + "_" + polarity + ".txt").split("\n\n\n\n\n")


def generate_data(language="java"):
    g = read_data("good", language=language)
    b = read_data("bad", language=language)
    ls = []
    for good in g:
        f = flatten(good)
        if len(f) > 0:
            ls.append([f, 0])
    for bad in b:
        f = flatten(bad)
        if len(f) > 0:
            ls.append([f, 1])

    with open(os.path.dirname(__file__) + "/data/" + language + "_" + "data.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerows([["input", "label"]] + ls)
    f.close()


class Logger:
    def __init__(self):
        self.data = ""

    def log_prediction(self, s, p):
        if p < 0.001:
            p = "\x1b[m" + " 0.0" + "%\x1b[m"
        elif p < .6:
            p = str(p*100)[0:4]
            if int(p) < 10:
                p = " " + p
        elif p <= .7:
            p = "\x1b[36m" + str(p*100)[0:4] + "%\x1b[m"
        elif p <= .8:
            p = "\x1b[33m" + str(p*100)[0:4] + "%\x1b[m"
        elif p >= .9:
            p = "\x1b[31m" + str(p*100)[0:4] + "%\x1b[m"
        print('{:>20} {:>1}'.format(s + ":", p))
        self.data = self.data + ('{:>20} {:>1}'.format(s + ":", Logger.escape_ansi(p))) + "\n"

    def log(self, s):
        self.data = self.data + Logger.escape_ansi(s) + "\n"
        print(s)

    @staticmethod
    def escape_ansi(line):
        try:
            ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
            return ansi_escape.sub('', line)
        except:
            return line[8:-8]

    def write(self):
        current = str(datetime.datetime.now())[0:19].replace("-", "_").replace(":", "_").replace(" ", "__") + ".log"
        with open(os.path.dirname(__file__) + "/logs/" + current, "w") as f:
            f.write(self.data)
        print("\nThe results of this run can be found in " + os.path.dirname(__file__) + "/achilles/logs/" + current)

