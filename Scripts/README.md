# Quick start
[annotateTuring.py](annotateTuring.py) must be run first in order to tokenize and annotate the whole corpus; folder paths are to be configured in [config.ini](config.ini). Data is extracted through [asLemmata_oneFile.py](asLemmata_oneFile.py) into the output folder (`output` in [config.ini](config.ini)). Output options are selected via user prompt.

# File descriptions

1. **[annotateTuring.py](annotateTuring.py)**: this script executes in a sequence [tokenizePerseus.py](tokenizePerseus.py), [tokenizeConverted.py](tokenizeConverted.py), and [corporaParser.py](corporaParser.py). This script compiles the whole corpus.
2. **[asLemmata.py](asLemmata.py)**: this script converts annotated XML files into text files with a each sentence on a new line (with ID and location) and lemmata instead of words; the stop word filter can be (de)activated in [config.ini](config.ini).
3. **[asLemmata_oneFile.py](asLemmata_oneFile.py)**: this script converts annotated XML files into a single text file with a each sentence on a new line and lemmata instead of words; the stop word filter can be (de)activated in [config.ini](config.ini). Each sentence is preceded by the year to which the work is dated. The user can decide if ID and location are to be included. The user can also filter files by metadata and filter sentences by loading a list of target words (identified by their ID).
4. **[beta2utf.py](beta2utf.py)**: function converting betacode Greek into Unicode characters.
5. **[config.ini](config.ini)**: configuration file. It stores the path (1) of the Excel document listing corpus files and storing metadata, (2) of the folder containing the corpus source files, (3) of the destination folders of the tokenizer and of the parser, as well as those of logs and other output files. It also contains values of paramters (stop word filter for [asLemmata.py](asLemmata.py)
6. **[convertToLemmata.xsl](convertToLemmata.xsl)**: XSLT file transforming annotated corpus files by replacing word forms with lemmata.
7. **[corporaParser.py](corporaParser.py)**: this script parses tokenized corpus files.
8. **[displayConverted.xsl](displayConverted.xsl)**: XSLT file displaying the output of [convertToLemmata.xsl](convertToLemmata.xsl) as texts with each sentence on a new line (with ID and location) and lemmata instead of words.
9. **[displayOriginal.xsl](displayOriginal.xsl)**: XSLT file displaying annotated corpus files as numbered lists of sentences.
10. **[grkFrm.py](grkFrm.py)**: Python dictionary containing all analyses of Greek word forms.
11. **[grkLemmata.py](grkLemmata.py)**: Python dictionary containing all Greek lemmata.
12. **[stop_cltk.py](stop_cltk.py)**: Perseus stop word list (from [CLTK](https://github.com/cltk/cltk/blob/master/cltk/stop/greek/stops.py)); added support for oxia acute accent vowel glyphs.
13. **[tlgIndex.py](tlgIndex.py)**: Python dictionary containing the TLG IDs of Greek authors.
14. **[tokenizeConverted.py](tokenizeConverted.py)**: tokenizer for other open source corpus files (preliminary converted into XML files).
15. **[tokenizePerseus.py](tokenizePerseus.py)**: tokenizer for [Perseus GitHub](https://github.com/PerseusDL/canonical-greekLit/tree/master/data) corpus files.
16. **[TT_createLexicon](TT_createLexicon)**: converts [grkLemmata.py](grkLemmata.py) into a lexicon for TreeTagger ([TreeTagger Data/lexicon.txt](TreeTagger Data/lexicon.txt)).
17. **[Turing_searchwords.py](Turing_searchwords.py)**: script that counts and stores occurences of words listed in an Excel document.
18. **[utf2beta.py](utf2beta.py)**: function converting Unicode Greek characters into betacode.
