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
* `flatten(chunk)` - returns a space delimited string tokenized by the Javalang tokenizer.
* `tokenize(contents)` - tokenizer; because javalang.tokenizer.tokenize(contents) was too verbose.
* `get_method_name(flat_string)` - extracts the name of the method from a flattened chunk. The method name is used for display the results to the user.
* `collect_data(data_path)` - extracts the good and bad method data from the Java Juliet Suite from the specified `data_path` and writes it to the data/ directory.
* `is_valid_chunk(s)` - uses the `_blocks` variable to determine if a chunk should be discarded or not. This ensures that we extract the entire method and not just all the blocks within the methods.
* `chunker(contents)` - extracts methods from the contents of a Java file. 

* `JavaJulietSuite.__init__(self, test_suite_location)` - constructor; encapsulates an entire Juliet Suite, stores several JavaJuliet objects.
* `JavaJulietSuite.get_good(self)` - extracts "good" methods from a list of JavaJuliet objects.
* `JavaJulietSuite.get_bad(self)` - extracts "bad" methods from a list of JavaJuliet objects.
* `JavaJulietSuite.get_chunks(self)` - extracts all methods form a list of JavaJuliet objects.
* `JavaJulietSuite.write_good(self, location="good.txt")` - writes all "good" methods.
* `JavaJulietSuite.write_bad(self, location="bad.txt")` - writes all "bad" methods. 

* `JavaJuliet.__init__(self, path)` - constructor; represents a single Juliet file, and contains a list of "good" chunks and "bad" chunks.
* `JavaJuliet.__str__(self)` - string representation of a single Juliet file.
* `JavaJuliet.chunks(self)` - returns a list of chunks from within the file.
* `JavaJuliet.good_bad_separator(self)` - splits a list of chunks into two distinct lists of "good" and "bad" chunks.
* `JavaJuliet.java_file_cleaner(file_loc)` - calls the helper methods: _comment_stripper, _crush, _allman_to_knr atomically.
* `JavaJuliet._comment_stripper(string)` - strips comments form the Juliet file.
* `JavaJuliet._crush(string)` - flatten a string.
* `JavaJuliet._allman_to_knr(string)` - converts a file from Allman to K&R. *If a file is not in K&R, it will be improperly parsed*. 

* `Javalect.__init__(self)` - constructor; initializes a keras.preprocessing.text tokenizer with the balanced data csv.
* `Javalect.embed(self, flat_method)` - embeds a vector of tokens to a higher dimension.
* `Javalect.execute_routine(files, h5_loc, log_write=False)` - traverse a list of files to be evaluated, loads in Keras h5 model save, and generates a prediction.
* `Javalect.prepare_corpus(language, method_names="preserve", mode="w")` - ingests java_bad.txt and java_good.txt, processes the corpus, and writes a *balanced* data set.
* `Javalect.scrape_corpus(test_suite_location, write_loc="<poliarty>.txt")` - repopulates good.txt and bad.txt. You ideally would use this if you add more Java classes to a raw data directory.

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
