package data

import (
  "math/rand"
  "fmt"
  "bytes"
  "strings"
  "strconv"
  "encoding/gob"
  "os"
  "dynamic-senses_release/util"
)

type Document struct {
  Label int
  Time int
  Target int
  Context[][2]int
}


type Corpus struct {
  Documents []*Document
  TargetFeatures *CodeMap
  ContextFeatures *CodeMap
}


/* Creates a corpus object and initializes all fields as empty  */
func NewCorpus() (corpus *Corpus) {
  corpus = new(Corpus)
  corpus.Documents = make([]*Document, 0)
  corpus.TargetFeatures = new(CodeMap)
  corpus.ContextFeatures = new(CodeMap)
  corpus.TargetFeatures.IDtoString = make(map[int]string)
  corpus.ContextFeatures.IDtoString = make(map[int]string)
  corpus.TargetFeatures.StringtoID = make(map[string]int)
  corpus.ContextFeatures.StringtoID = make(map[string]int)
  return
}

func NewDocument() (doc *Document){
    doc=new(Document)
    doc.Context = make([][2]int,0)
    return doc
}


/* Randomly initialized document labels of a corpus
 *   Seed < 1 means no randomization */
func (corpus *Corpus) InitializeLabeling(numTop int, seed int) {
  rand.Seed(int64(seed))
  for idx, _ := range(corpus.Documents) {
    corpus.Documents[idx].Label =  rand.Intn(numTop)
  }
}



func (corpus *Corpus) RandomizeOrder(seed int) {
  c2 := corpus.Copy()
  rand.Seed(int64(seed))
  order := rand.Perm(len(c2.Documents))
  for idx, _ := range(c2.Documents) {
    corpus.Documents[idx] = c2.Documents[order[idx]]
  }
}




/* Input text file YEAR /tab/ text
                   YEAR /tab/ text
                   ...
         target word list (one word per line)
         context window size
   Output binary corps with all 'documents' for each target concept. Time-tagged. */
func Create_corpus_from_text(txt_corpus_path, target_concept_path string, window_size int) (corpus *Corpus) {


    corpus = NewCorpus()

    /* read text corpus */
    txt_lines, err := util.Read_lines(txt_corpus_path)
    if err !=nil {panic(err)}

    /* create dictionary of target words */
    target_words, err := util.Read_lines(target_concept_path)
    target_word_dict  := make(map[string]int, len(target_words))
    for _, word := range(target_words) {
        target_word_dict[word] = 0
    }
    if err !=nil {panic(err)}

    /* fill corpus with target-word specific, time-stamped documents */
    for _, line := range(txt_lines) {
        if len(strings.Split(line, "\t")) == 2 {
            year_s, text := strings.Split(line, "\t")[0], strings.Split(line, "\t")[1]
            year, err    := strconv.Atoi(year_s)
            if err != nil {panic(err)}

            words        := strings.Split(text, " ")
            /* iterated through text in line and record a document whenever we find a target word */
            for wIdx:=0 ; wIdx < len(words) ; wIdx++ {
                if _, ok := target_word_dict[words[wIdx]] ;  ok {
                    if wIdx > window_size && wIdx < len(words)-window_size {
                    //if wIdx > 0 && wIdx < len(words) {    // VP: for partial window
                        doc := NewDocument()
                        doc.Target = corpus.TargetFeatures.Lookup(words[wIdx])
                        doc.Time   = year
                        cxt := make(map[int]int)
                        for i:=wIdx-window_size ; i<wIdx+window_size+1 ; i++ {
                            if i != wIdx {
                            //if i != wIdx && i >= 0 && i < len(words) { // VP: for partial window
                                cxt[corpus.ContextFeatures.Lookup(words[i])]++
                            }
                        }
                        for k,v := range(cxt) {
                            doc.Context = append(doc.Context, [2]int{k,v})
                        }
                        corpus.Documents = append(corpus.Documents, doc)
                    }
                }
            }
        }
    }
    return
}









/* takes the full document set and prints all documents
 * whose target word is in the targetWord list (parameter) */
func (corpus *Corpus) Extract_subcorpus(target string, slicesize, low, up, max_docs_per_slice int) ([]*Document,  *CodeMap,  *CodeMap, int) {

  if _,ok := corpus.TargetFeatures.StringtoID[target] ; ok {

    time_map, max := Year_to_id(low, up, slicesize)

    doc_count := make(map[int]int, len(time_map))

    featuremap := &CodeMap{}
    featuremap.IDtoString = make(map[int]string)
    featuremap.StringtoID = make(map[string]int)

    tgtfeature := &CodeMap{}
    tgtfeature.IDtoString = make(map[int]string)
    tgtfeature.StringtoID = make(map[string]int)
    tgtfeature.StringtoID[target]                        = corpus.TargetFeatures.StringtoID[target]
    tgtfeature.IDtoString[tgtfeature.StringtoID[target]] = target

    corpus2 := make([]*Document,0)
    for _,doc := range(corpus.Documents) {

      if _,ok := time_map[doc.Time] ; ok && doc.Target == corpus.TargetFeatures.StringtoID[target]  {
        if time_map[doc.Time] <= max {
	new_doc := doc.Copy()
	if up > low {
	  new_doc.Time=time_map[doc.Time]
	} else if doc.Time > max {
          max = doc.Time
        }
	if max_docs_per_slice==0 ||  doc_count[new_doc.Time] < max_docs_per_slice {
	  corpus2 = append(corpus2, new_doc)
	  doc_count[new_doc.Time]++

	  // 	fmt.Println(doc.Time, corpus2[len(corpus2)-1].Time)
	  for fIdx,f := range(doc.Context) {
	    corpus2[len(corpus2)-1].Context[fIdx][0] = featuremap.Lookup(corpus.ContextFeatures.IDtoString[f[0]])
	  }
	}
        }
      }
    }
    return corpus2, tgtfeature, featuremap, max+1
  } else {
    fmt.Println("===", target, "===\nTarget not in corpus!")
  }
  return nil, nil, nil, 0
}


/* maps original times to ID's if present in the time_map*/
func (corpus *Corpus) Bin_times(time_map map[int][2]int) {
    for docID:=0 ; docID<len(corpus.Documents) ; {
        mapped := false
        for id,slice := range(time_map) {
            if corpus.Documents[docID].Time >= slice[0] && corpus.Documents[docID].Time <= slice[1] {
                corpus.Documents[docID].Time = id
                mapped = true
                docID++
                break
            }
        }
        if !mapped {
            corpus.Documents = append(corpus.Documents[:docID], corpus.Documents[docID+1:]...)
        }
    }
}







func (document *Document) String(tgtFeatures, cxtFeatures map[int]string) (string_doc string) {
  fmt.Printf("Time:%d , K:%d  ",document.Time, document.Label)
  fmt.Printf("%s\t", tgtFeatures[document.Target])
  string_doc += fmt.Sprintf("Time:%d , K:%d  ",document.Time, document.Label)
  string_doc += fmt.Sprintf("%s\t", tgtFeatures[document.Target])
  if len(tgtFeatures[document.Target]) <=7 {
    fmt.Print("\t")
    string_doc += fmt.Sprint("\t")
  }
  for _,v := range(document.Context) {
    for j:=0 ; j<v[1] ; j++ {
      fmt.Print(cxtFeatures[v[0]], " ")
      string_doc += fmt.Sprint(cxtFeatures[v[0]], " ")
    }
  }
  fmt.Println()
  string_doc += fmt.Sprintln()
  return
}


func (corpus *Corpus) String() {
  for _,doc := range(corpus.Documents) {
    doc.String(corpus.TargetFeatures.IDtoString, corpus.ContextFeatures.IDtoString)
  }
}




func (cp *Corpus) Copy() *Corpus{
  cp2 := *cp
  cp2.Documents = make([]*Document, len(cp.Documents))
  for i,_ := range(cp.Documents) {
    cp2.Documents[i] = cp.Documents[i].Copy()
  }
  return &cp2
}



func (doc *Document) Copy() *Document {
  doc2 := *doc
  return &doc2
}


func (corpus *Corpus) Store(outfile string) {
  b := new(bytes.Buffer)
  g := gob.NewEncoder(b)
  err := g.Encode(corpus)
  if err != nil {
    fmt.Println(err)
  }
  fh, eopen := os.OpenFile(outfile, os.O_CREATE|os.O_WRONLY, 0666)
  defer fh.Close()
  if eopen != nil {
    fmt.Println(eopen)
  }
  n,ewrite := fh.Write(b.Bytes())
  if ewrite != nil {
    fmt.Println(ewrite)
  }
  fmt.Fprintf(os.Stderr, "%d bytes successfully written to file\n", n)
}

/* Read a feature respresentation of a corpus, and the feature lexicon from go .bin */
func Load_corpus(filename string) (crp *Corpus) {
  crp = new(Corpus)
  fh, err := os.Open(filename)
  if err != nil {
    fmt.Println(err)
  }
  dec := gob.NewDecoder(fh)
  err = dec.Decode(&crp)

  if err != nil {
    fmt.Println(err)
  }
  return
}



func Id_to_year(low, up, interval int) (map_to_year map[int]int) {
  map_to_year = make(map[int]int)
  for t:=0 ; low+(t*interval)<=up ; t++ {
    map_to_year[t] = low+(t*interval)
  }
  return
}

func Year_to_id(low, up, interval int) ( map[int]int,  int) {
  var timeslice int
  map_to_id := make(map[int]int)
  if up > low {
    lasttime := low
    for t:=low ; t<=up ; t++ {
      if t-lasttime == interval {
	timeslice++
	lasttime = t
      }
      map_to_id[t] = timeslice
    }
  }
  return map_to_id, timeslice
}
