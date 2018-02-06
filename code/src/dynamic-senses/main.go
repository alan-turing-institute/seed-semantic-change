package main

import (
  "flag"
  "strings"
  "runtime"
  "time"
  "dynamic-senses_release/util"
  "math/rand"
)

var store            = flag.String("store", "", "store corpus and model?")
var param_file       = flag.String("parameter_file", "", "path to parameter file?")
var mode             = flag.String("mode", "joint", "joint or independent")
var create_corpus    = flag.Bool("create_corpus", false, "Create go binary from text corpus?")

func main() {
    
  flag.Parse()
    
  /* set concurrency and randomness */
  numCPU := runtime.NumCPU()
  runtime.GOMAXPROCS(numCPU)
  rand.Seed(time.Now().Unix())

  parameters := parse_parameters(*param_file)
  if *create_corpus {
    verbose := false
    create_corpus_binary(parameters["text_corpus"], parameters["target_words"], parameters["bin_corpus_store"], parameters["window_size"], verbose)
  } else {
     train_model(*store, *mode, parameters)
  }
}




func parse_parameters(parameter_file string) map[string]string {
    parameters      := make(map[string]string)
    parameter_lines, err := util.Read_lines(parameter_file)
    if err != nil {panic(err)}
    
    for _, line := range(parameter_lines) {
        if len(strings.Split(line ,"\t")) == 2{
            key, val := strings.Split(line ,"\t")[0], strings.Split(line, "\t")[1]
            parameters[key] = val
        }
    }
    return parameters
}
