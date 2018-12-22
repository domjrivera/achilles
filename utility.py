from constants import *
import argparse
import os


def get_cmd_args():
    parser = argparse.ArgumentParser(description='Parse input string')
    parser.add_argument('goals', help='HELP!', nargs='+')
    args = parser.parse_args()
    goals = ' '.join(args.goals).replace(",", " ").split(" ")

    # Get version information.
    if goals[0].lower() == "version":
        print(version)
        quit(0)

    # Evaluate a single file.
    elif os.path.isfile(goals[0]):
        for language in languages.keys():
            for extension in languages[language]:
                if extension == goals[0][-len(extension):]:
                    return [language, goals[0]]
        # If there isn't language support, default to Java.
        return ["java", goals[0]]

    # Evaluate a file or folder with a certain language.
    elif (len(goals) == 2) and (goals[0].lower() in languages):
        # Evaluate all files of a certain language in folder.
        if os.path.isdir(goals[1]):
            return get_files(goals[1], goals[0])
        # Evaluate a single file.
        elif os.path.isfile(goals[1]):
            return [goals[0].lower, goals[1]]

    print("Invalid arguments.")
    quit(0)


def get_files(path, language="java"):
    files, output = os.listdir(path), []
    for item in os.listdir(path):
        if os.path.isdir(item):
            files.extend(os.listdir(item))
    for item in files:
        for extension in languages[language]:
            if extension == item[-len(extension):]:
                output.append(item)
    return [language] + output
