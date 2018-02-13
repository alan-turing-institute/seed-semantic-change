# Quick start
[annotateTuring.py](annotateTuring.py) must be run first in order to tokenize and annotate the whole corpus; folder paths are to be configured in [config.ini](config.ini). Data is extracted through [asLemmata_oneFile.py](asLemmata_oneFile.py) into the output folder (`output` in [config.ini](config.ini)). Output options are selected via user prompt. The output is processed by Valerio's script, whose output is converted into human-readable form by [make_data_readable.py](make_data_readable.py).

The file prefixed with `TT_` are related to TreeTagger. 

# File descriptions
## Scripts
1. **[annotateTuring.py](annotateTuring.py)**: this script executes in a sequence [tokenizePerseus.py](tokenizePerseus.py), [tokenizeConverted.py](tokenizeConverted.py), and [corporaParser.py](corporaParser.py). This script compiles the whole corpus.
2. **[asLemmata_oneFile.py](asLemmata_oneFile.py)**: this script converts annotated XML files into a single text file with a each sentence on a new line and lemmata instead of words; the stop word filter can be (de)activated in [config.ini](config.ini). Each sentence is preceded by the year to which the work is dated. The user can decide if ID and location are to be included. The user can also filter files by metadata and filter sentences by loading a list of target words (identified by their ID).
3. **[corporaParser.py](corporaParser.py)**: this script parses tokenized corpus files.
4. **[make_data_readable.py](make_data_readable.py)**: converts IDs into Greek lemmata (and retains ID information) in output of Valerio's script.
5. **[tokenizeConverted.py](tokenizeConverted.py)**: tokenizer for other open source corpus files (preliminary converted into XML files).
6. **[tokenizePerseus.py](tokenizePerseus.py)**: tokenizer for [Perseus GitHub](https://github.com/PerseusDL/canonical-greekLit/tree/master/data) corpus files.
7. **[TT_training_create_lexicon.py](TT_create_lexicon.py)**: converts [grkLemmata.py](grkLemmata.py) into a [lexicon](TreeTaggerData/lexicon.txt) for TreeTagger.
8. **[TT_training_create_openclass.py](TT_training_create_openclass.py)**: extract the POS tagset from [grkLemmata.py](grkLemmata.py) and saves it into [TreeTaggerData/openclass.txt](TreeTaggerData/openclass.txt) for TreeTagger.
9. **[TT_training_prepare_set.py](TT_training_prepare_set.py)**: transforms the PROIEL and Perseus Ancient Greek treebanks into [training sets](TreeTaggerData/training_set.txt) for TreeTagger. The paths of the treebanks are to be specified in 
10. **[Turing_searchwords.py](Turing_searchwords.py)**: script that counts and stores occurences of words listed in an Excel document. _USED FOR PRELIMINARY DATA EXPLORATION_

## Modules
1. **[beta2utf.py](beta2utf.py)**: function converting betacode Greek into Unicode characters.
2. **[utf2beta.py](utf2beta.py)**: function converting Unicode Greek characters into betacode.

## Dictionaries
1. **[grkFrm.py](grkFrm.py)**: Python dictionary containing all analyses of Greek word forms.
2. **[grkLemmata.py](grkLemmata.py)**: Python dictionary containing all Greek lemmata.
3. **[stop_cltk.py](stop_cltk.py)**: Perseus stop word list (from [CLTK](https://github.com/cltk/cltk/blob/master/cltk/stop/greek/stops.py)); added support for oxia acute accent vowel glyphs and list as IDs.
4. **[tlgIndex.py](tlgIndex.py)**: Python dictionary containing the TLG IDs of Greek authors.

## Configuration
1. **[config.ini](config.ini)**: configuration file. It stores the paths (1) of the Excel document listing corpus files and storing metadata, (2) of the folder containing the corpus source files, (3) of the destination folders of the tokenizer and of the parser, as well as those of logs and other output files, (4) of the word lists to be used by [asLemmata_oneFile.py](asLemmata_oneFile.py), (5) of the treebanks to be used by [TT_training_prepare_set.py](TT_training_prepare_set.py). It also contains values of parameters (activate/deactivate stop word filter in [asLemmata_oneFile.py](asLemmata_oneFile.py)) and the cell ranges in `file_list.xslx` from which headers and file paths should be extracted and to which data should be written by [tokenizeConverted.py](tokenizeConverted.py), [tokenizePerseus.py](tokenizePerseus.py), [corporaParser.py](corporaParser.py), and [asLemmata_oneFile.py](asLemmata_oneFile.py).
