package main

import (
    "bufio"
    "dynamic-senses_release/data"
    "dynamic-senses_release/model"
    "dynamic-senses_release/gibbs"
    "dynamic-senses_release/util"
    "strconv"
    "fmt"
    "os"
    "path"
    "strings"
)

func train_model(store, mode string, parameters map[string]string) {

    if store=="" {
        panic("store must be 'True' or 'False'")
    }

    /*** load data and features ***/
    var word_corpus_path, full_corpus_path, full_heldout_path, output_path, concept_path string
    var word_docs []*data.Document
    var word_docs_heldout []*data.Document
    var word_corpus *data.Corpus
    var tgtfeatures, cxtfeatures  *data.CodeMap
    var tgtfeatures_heldout, cxtfeatures_heldout  *data.CodeMap
    var max_slice_id int

    full_corpus_path= parameters["full_corpus_path"]
    full_heldout_path = parameters["full_heldout_path"]
    word_corpus_path= parameters["word_corpus_path"]
    concept_path    = parameters["target_words"]
    output_path     = parameters["output_path"]


    /* ******************************************************************************************** */
    /* ***********          *************        parameters      **********         *************   */
    /* ******************************************************************************************** */
    kappaF,err      := strconv.ParseFloat(parameters["kappaF"], 64)
    kappaK,err      := strconv.ParseFloat(parameters["kappaK"], 64)
    a0,err          := strconv.ParseFloat(parameters["a0"], 64)
    b0,err          := strconv.ParseFloat(parameters["b0"], 64)
    num_top, err    := strconv.Atoi(parameters["num_top"])
    iterations, err := strconv.Atoi(parameters["iterations"])
    /* ******************************************************************************************** */
    start_time,err  := strconv.Atoi(parameters["start_time"])
    end_time, err   := strconv.Atoi(parameters["end_time"])
    time_interval,err := strconv.Atoi(parameters["time_interval"])
    var time_map map[int][2]int
    /* ******************************************************************************************** */
    min_doc_per_word, err := strconv.Atoi(parameters["min_doc_per_word"])
    max_docs_per_slice, err := strconv.Atoi(parameters["max_docs_per_slice"])
    /* ******************************************************************************************** */

    /** read target words **/
    words, err := util.Read_lines(concept_path)
    if err!=nil{panic(err)}

    /** for each word -- create corpus if doesn't exist
     *                -- run model **/
    for wordIdx, word := range(words) {
        if len(word) > 0 {

            word_model_name := "corpus"+"_s"+parameters["start_time"]+"_e"+parameters["end_time"]+"_i"+parameters["time_interval"]+".bin"

            /* if a word-specific / time-specifid corpus exists -- use it! */
            if _,err := os.Stat(path.Join(word_corpus_path, word, word_model_name)) ; err== nil {

                word_corpus = data.Load_corpus(path.Join(word_corpus_path, word, word_model_name))

                fmt.Println(len(word_corpus.Documents),
                            len(word_corpus.TargetFeatures.IDtoString),
                            len(word_corpus.ContextFeatures.IDtoString))

                /* sort time-tagged documents into specified bins */
                max_slice_id = 0
                    for _,d := range(word_corpus.Documents) {
                        if d.Time > max_slice_id {max_slice_id = d.Time}
                    }
                    max_slice_id++

                /* in case |K| is different from what it was during corpus creation */
                word_corpus.InitializeLabeling(num_top, 56)

            /* if no word-specific corpus exists -- create one! */
            } else {

                print("correct case for test likelihood\n")

                full_corpus := data.Load_corpus(path.Join(full_corpus_path))
                full_corpus.InitializeLabeling(num_top, 56)

                full_heldout := data.Load_corpus(path.Join(full_heldout_path))
                full_heldout.InitializeLabeling(num_top, 56)

                /* extract word-specific sub corpus */
                word_docs, tgtfeatures, cxtfeatures, max_slice_id = full_corpus.Extract_subcorpus(word, time_interval, start_time, end_time, max_docs_per_slice)
                word_corpus = &data.Corpus{word_docs, tgtfeatures, cxtfeatures}
                word_corpus.RandomizeOrder(4)

                word_docs_heldout, tgtfeatures_heldout, cxtfeatures_heldout, _ = full_heldout.Extract_subcorpus(word, time_interval, start_time, end_time, max_docs_per_slice)

                if strings.ToLower(store) == "true" {
                    if _,err := os.Stat(path.Join(word_corpus_path, word)) ; err != nil {
                        err := os.Mkdir(path.Join(word_corpus_path, word), 0777)
                        if err != nil {panic(err)}
                    }
                    word_corpus.Store(path.Join(word_corpus_path, word, word_model_name))
                }
            }

            /* start the model */
            fmt.Printf("%s : %d documents\n", word, len(word_corpus.Documents))

            tmp_outputdir := path.Join(output_path, word)
            if _,err := os.Stat(path.Join(tmp_outputdir, "output.dat")) ; err== nil {
                os.Rename(path.Join(tmp_outputdir, "output.dat") ,path.Join(tmp_outputdir, "output_old.dat"))
                os.Rename(path.Join(tmp_outputdir, "model.bin") ,path.Join(tmp_outputdir, "model_old.bin"))
            }

            if len(word_corpus.Documents) >= min_doc_per_word && len(word_corpus.Documents) > 0 {
                fmt.Println("=================\n", wordIdx, word, "\n==================\n")

                var s *gibbs.Sampler
                var tmp_outputfile *os.File

                /*** create output path ***/
                if strings.ToLower(store) == "true" {
                    if _, err := os.Stat(path.Join(tmp_outputdir)); err != nil {
                        err := os.Mkdir(path.Join(tmp_outputdir), 0777)
                        if err!=nil{panic(err)}
                    }

                    tmp_outputfilename := path.Join(tmp_outputdir, "output.dat")
                    tmp_outputfile, err = os.OpenFile(tmp_outputfilename, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0666)
                    if err!= nil{panic(err)}
                }

                /** initialize model **/
                parameters := model.New_model_parameters(a0, b0, kappaF, kappaK, len(word_corpus.Documents), num_top, max_slice_id, len(word_corpus.TargetFeatures.IDtoString), len(word_corpus.ContextFeatures.IDtoString))
                m          := model.New_model(parameters)
                m.Initialize_batch(word_corpus)

                /** initialize sampler **/
                s = gibbs.New_sampler()
                lag, burn_in := 0, 0   // TODO also handle through parameter file
                s.Initialize(m, word_corpus, iterations, lag, burn_in)

                parameter_string := fmt.Sprintf("%d documents , %d concepts , %d context features (%s) \nkappaF %f, kappaK %f, a0 %f, b0 %f, K %d, max_docs_per_slice %d, start %d, end %d, times %d, dT %d, I %d\n\n", len(s.Corpus.Documents), len(s.Corpus.TargetFeatures.IDtoString), len(s.Corpus.ContextFeatures.IDtoString), word, kappaF, kappaK, a0, b0, num_top, max_docs_per_slice, start_time, end_time, max_slice_id, time_interval, iterations)
                parameter_string += "\n"+fmt.Sprintln(time_map)+"\n"
                fmt.Println(parameter_string)

                if strings.ToLower(store) == "true" {
                    _, err = tmp_outputfile.WriteString(parameter_string)
                }

                /*** train model ***/
                fmt.Println("...ready to estimate")
                err = s.Estimate(false, &data.Corpus{word_docs_heldout, tgtfeatures_heldout, cxtfeatures_heldout}, mode)

                fmt.Println("\nFinal test loglikelihood: ", s.Model.Predict(&data.Corpus{word_docs_heldout, tgtfeatures_heldout, cxtfeatures_heldout}))
                fmt.Println("\nFinal train loglikelihood: ", s.Model.Predict(s.Corpus))

                fmt.Println("Saving likelihoods to file")
                f, err := os.Create(path.Join(tmp_outputdir, "final_likelihoods.txt"))
                w := bufio.NewWriter(f)
                _, err = fmt.Fprintf(w, "Train_likelihood: %f", s.Model.Predict(s.Corpus))
                _, err = fmt.Fprintf(w, "\nTest_likelihood: %f", s.Model.Predict(&data.Corpus{word_docs_heldout, tgtfeatures_heldout, cxtfeatures_heldout}))
                w.Flush()
                fmt.Println("Saved likelihoods to file")


                /*** print model ***/
                if strings.ToLower(store) == "true" && err == nil {
                    model_string := s.Model.Print_categories(10, s.Corpus.TargetFeatures.IDtoString, s.Corpus.ContextFeatures.IDtoString)
                    fmt.Println("...storing model")
                    _, err = tmp_outputfile.WriteString(model_string)
                    _, err = tmp_outputfile.WriteString(fmt.Sprintf("\n\n-----------------------\n kappa_c %f , kappa_f %f", s.Model.Parameters.Kappa_c, s.Model.Parameters.Kappa_f))
                    if err != nil{panic(err)}
                    s.Model.Store(path.Join(tmp_outputdir, "model.bin"))
                }
                fmt.Println(word, "done!")
            }
        }
    }
}
