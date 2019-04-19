import datetime
from javalect import *
import argparse
import os
from constants import *


class Args:
    @staticmethod
    def get():
        parser = argparse.ArgumentParser(description='Parse input string')
        parser.add_argument('goals', help='HELP!', nargs='+')
        args = parser.parse_args()
        goals = ' '.join(args.goals).replace(",", " ").split(" ")
        Args.parse(goals)

    @staticmethod
    def parse(goals):
        if goals[0] in ["version", "-v", "--version"]:
            print(version_info)
            quit(0)

        # Argument actions for Java.
        elif goals[0] == "java":
            if goals[1] == "train":
                print(goals)
            elif goals[1] in ["list", "-ls", "ls"]:
                ls = os.listdir(str(os.path.realpath(__file__).rsplit("/", 1)[0]) + "/data/java/checkpoints/")
                print("\x1b[36mFound " + str(len(ls)) + " Java checkpoints:\x1b[m")
                for cwe in ls:
                    print("  \x1b[36m*\x1b[m", cwe[:-3])


        else:
            print("Invalid parameters.")
            quit(0)


def find_occurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

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
