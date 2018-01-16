annotateTuring.py: this script executes in a sequence tokenizePerseus.py, tokenizeConverted.py, and corporaParser.py.

beta2utf.py: function converting betacode Greek into Unicode characters.

config.ini: configuration file containing absolute paths of the file in which the location of text files in the corpus are stored (Excel worksheet), of the folder containing the corpus source files, and the destination folders of the tokenizer, parser, logs, and output files.

convertToLemmata.xsl: XSLT file transforming annotated corpus files by replacing word forms with lemmata.

corporaParser.py: parser.

displayConverted.xsl: XSLT file displaying corpus files containing lemmata instead of word forms as numbered lists of sentences.

displayOriginal.xsl: XSLT file displaying annotated corpus files as numbered lists of sentences.

grkFrm.py: Python dictionary containing all analyses of word forms.

grkLemmata.py: Python dictionary containing all Greek lemmata.

tlgIndex.py: Python dictionary containing the TLG ids of Greek authors.

tokenizeConverted.py: tokenizer for other open source corpus files (preliminary converted into XML files).

tokenizePerseus.py: tokenizer for Perseus GitHub corpus files.

Turing_searchwords.py: script that counts occurences of words listed in an Excel file throughout the corpus and saves them in the same file.

utf2beta.py: function converting Unicode Greek characters back into betacode.
