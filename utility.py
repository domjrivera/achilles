from constants import *
import argparse
import fnmatch
import os


def get_cmd_args():
    print(version_info)
    parser = argparse.ArgumentParser(description='Parse input string')
    parser.add_argument('goals', help='HELP!', nargs='+')
    args = parser.parse_args()
    goals = ' '.join(args.goals).replace(",", " ").split(" ")
    ls = parse_cmd_args(goals)
    if len(ls) == 1:
        print("No compatible files found.")
        quit(0)
    if len(ls) > 100:
        ans = input("Found " + str((len(ls) - 1)) + " " + ls[0] + " files. Do you want to continue? [y]es, [n]o: ")
        if "y" in ans.lower():
            pass
        else:
            quit()
    return ls[1:], ls[0]


# Courtesy of Marco L. on Stack Overflow
def find_occurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def parse_cmd_args(goals):
    # Get version information.
    if goals[0].lower() == "version":
        print(version_info)
        quit(0)

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

    print("Invalid arguments.")
    quit(0)


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


def read_file(path):
    with open(path, 'r') as content_file:
        return content_file.read()

