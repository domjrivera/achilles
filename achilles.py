import argparse
import os
from constants import *


def main():
    # Top-level parser.
    parser = argparse.ArgumentParser(prog='achilles')
    subparsers = parser.add_subparsers(help='sub-command help')

    # achilles analyze file            =>   file='file'
    analyze = subparsers.add_parser('analyze', help='check a given file against vulnerability models')
    analyze.add_argument('file', type=str, help='analyze help')

    # achilles train java folder 30    =>    directory='folder', language='java', 'threshold=30'
    train = subparsers.add_parser('train', help='train models on class files in a given directory')
    train.add_argument('language', type=str, help='the language the corpus is written in')
    train.add_argument('directory', type=str, help='path to a folder containing corpus classes')
    train.add_argument('threshold', type=int, help='drop vulnerability classes with fewer example'
                                                   ' classes than the given threshold.')

    # achilles ls java                 =>    language='java'
    ls = subparsers.add_parser('ls', help='view the list of trained models for a given language')
    ls.add_argument('language', type=str, help='the language to list vulnerability models for')
    args = str(parser.parse_args())[10:-1]

    if "directory=" in args:  # train
        from javalect import Javalect
        directory, language, threshold = args.replace("directory=", "").replace("language=", "")\
                                             .replace("threshold=", "").replace("\'", "").split(", ")
        if os.path.isdir(directory) or True:
            print("\x1b[33mTraining " + language + " vulnerability models using files from \"" +
                  directory + "\" with a threshold of " + threshold + ".\x1b[m")
            Javalect.train_models(directory, threshold=0)
        else:
            print("\x1b[31mUnable to locate folder: " + directory + "\x1b[m")

    elif "file=" in args:  # analyze
        from javalect import Javalect
        args = args.replace("file=", "").replace("\'", "")
        if os.path.isfile(args) or True:
            extension = "." + args.split(".")[-1]
            if extension in languages:
                if languages[extension] == "java":
                    Javalect.analyze(args)
                # Add language support here.
            else:
                print("\x1b[31mNo language support for \"" + extension + "\".\x1b[m")
        else:
            print("\x1b[31mUnable to locate file: " + args + "\x1b[m")

    else:  # ls
        args = args.replace("language=", "").replace("\'", "")
        fpath = str(os.path.realpath(__file__).rsplit("/", 1)[0]) + "/data/" + args + "/checkpoints/"
        if os.path.isdir(fpath):
            ls = os.listdir(fpath)
            print("\x1b[36mFound " + str(len(ls)) + " Java checkpoints:\x1b[m")
            for cwe in ls:
                print("  \x1b[36m*\x1b[m", cwe[:-3])
        else:
            print("\x1b[31mUnable to locate vulnerability models for \"" + args + "\".\x1b[m")


if __name__ == "__main__":
    main()
