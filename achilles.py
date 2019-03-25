from javalect import *
import os


def main():
    # files, lang = get_cmd_args()
    files, lang = ["Test.java"], "java"  # Use while testing

    h5_loc = os.getcwd() + "/" + SAVE_MODEL_AS.replace("<language>", lang)
    if not os.path.isdir(h5_loc):
        print("Unable to locate a trained " + lang + " model.\nTrain the model using " + lang +
              "-specific data with \x1b[33machilles train " + lang + "\x1b[m.")
        quit()

    print("\x1b[36mEvaluating " + str(len(files)) + " files:\x1b[m")
    for file in files:
        print("  ", file)

    # Add language support here
    if lang == "java":
        Javalect.execute_routine(files)
    else:
        quit()


if __name__ == "__main__":
    main()
