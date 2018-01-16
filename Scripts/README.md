# File description

1. **annotateTuring.py**: this script executes in a sequence tokenizePerseus.py, tokenizeConverted.py, and corporaParser.py.
2. **beta2utf.py**: function converting betacode Greek into Unicode characters.
3. **config.ini**: configuration file containing absolute paths of the file in which the location of text files in the corpus are stored (Excel worksheet), of the folder containing the corpus source files, and the destination folders of the tokenizer, parser, logs, and output files.
4. **convertToLemmata.xsl**: XSLT file transforming annotated corpus files by replacing word forms with lemmata.
5. **corporaParser.py**: parser.
6. **displayConverted.xsl**: XSLT file displaying corpus files containing lemmata instead of word forms as numbered lists of sentences.
7. **displayOriginal.xsl**: XSLT file displaying annotated corpus files as numbered lists of sentences.
8. **grkFrm.py**: Python dictionary containing all analyses of word forms.
9. **grkLemmata.py**: Python dictionary containing all Greek lemmata.
10. **tlgIndex.py**: Python dictionary containing the TLG ids of Greek authors.
11. **tokenizeConverted.py**: tokenizer for other open source corpus files (preliminary converted into XML files).
12. **tokenizePerseus.py**: tokenizer for Perseus GitHub corpus files.
13. **Turing_searchwords.py**: script that counts occurences of words listed in an Excel file throughout the corpus and saves them in the same file.
14. **utf2beta.py**: function converting Unicode Greek characters back into betacode.
