import csv
import argparse
import os
import fnmatch
from random import shuffle
from model import *


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
                print("Balancing training data.")
                balance_data("data/" + goals[1] + "_data.csv")
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
    return read_file("data/" + language + "_" + polarity + ".txt").split("\n\n\n\n\n")


def flatten(s):
    s = s.replace("\t", " ")
    s = s.split("\n")
    for x in range(len(s)):
        s[x] = s[x].strip()
    return " ".join(s)


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

    with open("data/" + language + "_" + "data.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerows([["input", "label"]] + ls)
    f.close()


def balance_data(language="java"):
    g, b = [], []
    with open("data/" + language + "_data.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == "1":
                b.append(row)
            elif row[1] == "0":
                g.append(row)
    size = min(len(g), len(b))
    ls = g[0:size] + b[0:size]
    shuffle(ls)
    with open("data/" + language + "_" + "balanced_data.csv", 'w') as h:
        writer = csv.writer(h)
        writer.writerows([["input", "label"]] + ls)
    h.close()


# Courtesy of interactivepython.org
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


class Logger:
    def __init__(self):
        self.data = ""

    def log(self, s):
        self.data = self.data + s + "\n"
        print(s)