# [WIP]Project Achilles
![Achilles](assets/logo.jpg)

## Calling Achilles from the Terminal
In your terminal `nano ~/.bash_profile`, then add the line `alias achilles="python3 <path-to-achilles.py>"`
* `achilles <file>` - Achilles will attempt to automatically decide the language to use based on the file extension. 

* `achilles <language> <file>` - Intended for use with source code that may have an obscure file extension.

* `achilles <language> <folder>` - This command will recursively traverse an entire folder and evaluate any files
 with extensions pertaining to the language specified. If more than 100 compatible files are found, Achilles will 
 prompt the user before continuing.

* `achilles train <language>` - Retrains the model on <language>_balanced_data.csv; this command does not automatically
 re-balance the training data.

* `achilles balance <language>` - Rebalance raw <language>_good.txt and <language>_bad.txt, generating the
 <language>_balanced_data.csv used to train the model.


## Building Achilles Support for Other Languages
Project Achilles was designed with crowd-sourcing in mind.
In theory, adding additional language support should be relatively simple.
1. Add an entry to the dictionary `languages` such that the key is the name of
the language, and the value is a list of the possible file extensions for files
of that type. Note that the key of this dictionary will be the language keyword 
used in the command line when calling Achilles. Multiple different language 
variants can be added by repeating the same value list for a different key,
effectively representing the same language in more than one different ways.
This may be useful if a language may be tedious to type out in terminal, for instance,
C++, Visual Basic, Objective-C, c#, and other languages with punctuations that slow
down typing... 
1. Modify the if-statement in the main() method of achilles.py by adding:
    ```
    elif lang == <name of language key>:
        <Name of language key>lect.execute_routine(files)
    ```
1. Create a &lt;name of language key&gt;lect.py file with the necessary functions
to transform the code in that language as required by the neural network.
Follow the conventions in achilles.py as a guide.

https://www.kaggle.com/kredy10/simple-lstm-for-text-classification/notebook

# Litterarum Ad Nauseam
## Todo
1. Get F1-Score, Accuracy & Precision of Model

## achilles.py
This file serves as the entry point for the Achilles tool. If you wish to run Achilles in an IDE on a dummy Java file,
make sure to change the parameter in the main invoking method.
```python
if __name__ == "__main__":
    main(testing=True)
```
While `testing=True`, Achilles will point to Test.java in the relative directory. When you are ready to deploy, or call
Achilles from command line, change `testing=False`.


## contants.py
* Several hyperparameters used by the LSTM model
* `SAVE_MODEL_AS` - the save location of the model
* `version_info` and `__version__ ` - Displayed when Achilles is invoked.
* `languages` - a dictionary containing the name of the language as the key, and a list of extensions used by that
language as the value. The key of this dictionary will become how that language is referred to by Achilles. It is *very*
important to keep this in mind.


## javalect.py
* `flatten(chunk)` -
* `tokenize(contents)` -
* `get_method_name(flat_string)` -
* `collect_data(data_path)` -
* `is_valid_chunk(s)` -
* `chunker(contents)` -
* `JavaJulietSuite.__init__(self, test_suite_location)` -
* `JavaJulietSuite.get_good(self)` -
* `JavaJulietSuite.get_bad(self)` -
* `JavaJulietSuite.get_chunks(self)` -
* `JavaJulietSuite.write_good(self, location="good.txt")` -
* `JavaJulietSuite.write_bad(self, location="bad.txt")` -

* `JavaJuliet.__init__(self, path)` -
* `JavaJuliet.__str__(self)` -
* `JavaJuliet.chunks(self)` -
* `JavaJuliet.good_bad_separator(self)` -
* `JavaJuliet.java_file_cleaner(file_loc)` -
* `JavaJuliet._comment_stripper(string)` -
* `JavaJuliet._crush(string)` -
* `JavaJuliet._allman_to_knr(string)` -

* `Javalect.__init__(self)` -
* `Javalect.embed(self, flat_method)` -
* `Javalect.execute_routine(files, h5_loc, log_write=False)` -
* `Javalect.prepare_corpus(language, method_names="preserve", mode="w")` -
* `Javalect.scrape_corpus(test_suite_location, write_loc="<poliarty>.txt")` -

## model.py
* `AchillesModel.RNN()` -
* `AchillesModel.train()` -

## utility.py
* `read_file(path)` -
* `get_cmd_args()` -
* `find_occurrences(s, ch)` -
* `parse_cmd_args(goals)` -
* `get_files(path, language="java")` -
* `read_data(polarity, language="java")` -
* `generate_data(language="java")` -

* `Logger.__init__(self)` -
* `Logger.log_prediction(self, s, p)` -
* `Logger.log(self, s)` -
* `Logger.escape_ansi(line)` -
* `Logger.write(self)` -
