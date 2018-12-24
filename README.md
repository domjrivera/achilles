## Project Achilles - A Static Source Code Vulnerability Identifier

#### Using Achilles from the Terminal
`achilles <file>` - Achilles will attempt to automatically decide the language to use based on the file extension. 

`achilles <language> <file>` - Intended for use with source code that may have an obscure file extension.

`achilles <language> <folder>` - This command will recursively traverse an entire folder and evaluate any files
 with extensions pertaining to a language. If more than 100 files are found, Achilles will prompt the user before
 continuing.
