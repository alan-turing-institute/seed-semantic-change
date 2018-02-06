package main

import (
  "dynamic-senses_release/data"
  "strconv"
  "fmt"
)

func create_corpus_binary(corpus, targets, store_path, window_size_s string, verbose bool) {
    /* assumes a text file (or multiple) with text of the form
     *   YEAR /tab/ sentence
     *   YEAR /tab/ sentence
     *   YEAR /tab/ sentence
     *   ...
     * returns a binary corpus representation from which target-word specific corpora can be estracted. */
    
        
    println(corpus)
    println(targets)
    println(window_size_s)
    
    window_size, err := strconv.Atoi(window_size_s)
     if err != nil{panic(err)}
     
     binary_corpus := data.Create_corpus_from_text(corpus, targets, window_size)
     binary_corpus.Store(store_path)
     
     if verbose {
         binary_corpus.String()
         for i:=0 ; i<len(binary_corpus.TargetFeatures.IDtoString) ; i++ {
             fmt.Println(i, binary_corpus.TargetFeatures.IDtoString[i])
         }
         fmt.Println()
         for i:=0 ; i<15 ; i++ {
             fmt.Println(i, binary_corpus.ContextFeatures.IDtoString[i])
         }
     }
}
