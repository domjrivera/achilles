# [WIP]Project Achilles
![Achilles](assets/logo.jpg)

## Calling Achilles from the Terminal
In your terminal, enter `nano ~/.bash_profile`, then add the line `alias achilles="python3 <path-to-achilles.py>"`
* `achilles analyze <file>` -  analyzes a source file, using the appropriate vulnerability models
* `achilles train <language> <folder> <threshold>` - trains a model on a given directory of example files for a language.
 Achilles will ignore any vulnerability classes that have fewer entries than the provided threshold number.
* `achilles ls <language>` - lists the vulnerability models for a given language.

## Building Achilles Support for Other Languages
1. In constants.py, add file extensions to the `languages` dictionary, with the target language as the value.
1. Create a new python file of similar form to javalect.py, fit with functions that parse your language appropriately.
 As input, AchillesRNN takes a sequence of tokens by method; with the method name replaced by a random string of characters.
1. Replace instances of `# Add language support here.` in achilles.py with an elif block, calling the appropriate static
functions for training and predicting.
