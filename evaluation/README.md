## Evaluation notebook

### Notebook
The notebook is documented and quite straightforward. To go from normal to debug mode, comment lines 12-13 and uncomment lines 16-17.

### Files

- `evaluation_script.py` is the python script 
- `evaluation_script_genre-naive_with_NOT.py` is the python script for the evaluation of the genre-naïve model ("NOT" filter)




To run an evaluation, the evaluation script should be edited in the following way:

- `genre` determines the genre of the corpus. By default, `all`.
- `s_senses` is the path to the expert-annotated data, that serves as ground-truth.
- `k_senses` is the path to the model output.
- `parameter_file` is the path to the parameter file used to train the model specified in `k_senses`.

The results of the evaluation is stored in a `.txt` file in `dir_out`, its naming follows that logic: `target_id+param_name+"genre_"+genre+"_i"+str(iterations)+"_k"+str(num_top)+"_time_interval"+str(time_interval)+".txt"`. Resulting plots (expert input as well as model output) are stored according to the same naming scheme, in the same folder.

Other scripts that are not part of the evaluation but are in this folder:

- `copora_genre_ids.ipynb` creates genre-specific corpus files for target words. 
- `new_output_to_single_output.py` transforms the output of the genre-topic model into an output readable by `evaluation_script.py` (i.e. the original SCAN output format).