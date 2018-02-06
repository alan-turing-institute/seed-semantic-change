package data

import (
  "fmt"
  "os"
  "encoding/gob"
)

type CodeMap struct {
  IDtoString map[int]string
  StringtoID map[string]int
}


func (code *CodeMap) Lookup(str string) int {
  if _,ok := (*code).StringtoID[str]; !ok {
    (*code).StringtoID[str] = len((*code).IDtoString)
      (*code).IDtoString[len((*code).IDtoString)] = str
  }
  return (*code).StringtoID[str]
}



// Loading a go struct containing a codemap (for lemmas or c5 tags) from file
func LoadCode (filename string) (code CodeMap) {
  fh, err := os.Open(filename)
  if err != nil {
    fmt.Println(err)
  }
  dec := gob.NewDecoder(fh)
  err = dec.Decode(&code)
  if err != nil {
    fmt.Println(err)
  }
  return
}
