package gibbs

import (
  "dynamic-senses_release/model"
  "dynamic-senses_release/data"
  "encoding/gob"
  "bytes"
  "os"
  "time"
  "fmt"
  "math/rand"
   )

type Sampler struct {
  Model *model.Model
  Corpus *data.Corpus
  iterations int
  lag int
  burnin int
  generator *rand.Rand
  post_reg float64
}

func New_sampler()  (s *Sampler) {
  s            = new(Sampler)
  s.Model      = new(model.Model)
  s.Corpus     = new(data.Corpus)
  s.post_reg   = 0.0
  return
}

func (s *Sampler) Initialize(m *model.Model, corpus *data.Corpus,  iterations, lag, burnin int){
  s.Model      = m
  s.Corpus     = corpus
  s.iterations = iterations
  s.lag        = lag
  s.burnin     = burnin
  s.generator  = rand.New(rand.NewSource(time.Now().UTC().UnixNano())) //rand.New(rand.NewSource(int64(1)))
  return
}


func (s *Sampler) Set_iterations(it int) {
  s.iterations = it
}

func (sampler *Sampler) Store(filename string) {
  b := new(bytes.Buffer)
  g := gob.NewEncoder(b)
  err := g.Encode(sampler)
  if err != nil {fmt.Println(err)}
  fh, eopen := os.OpenFile(filename, os.O_CREATE|os.O_WRONLY, 0666)
  defer fh.Close()
  if eopen != nil {fmt.Println(eopen)}
  n,ewrite := fh.Write(b.Bytes())
  if ewrite != nil {fmt.Println(ewrite)}
  fmt.Fprintf(os.Stderr, "%d bytes successfully written to file\n", n)
}

func LoadSampler(filename string) (sampler *Sampler){
  fh, err := os.Open(filename)
  if err != nil {fmt.Println(err)}
  dec := gob.NewDecoder(fh)
  err = dec.Decode(&sampler)
  if err != nil {fmt.Println(err)}
  return
}
