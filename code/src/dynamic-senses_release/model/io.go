/*
 *  Takes a model and, for storing turns all *DenseMatrices 
 *  to [][]float64 (model_storable type)
 *  (because DenseMatrices have only private fields)
 * 
 *  Conversely, it reads a model_storable into a byte array and from 
 *  that reconstructs a prober model with *DenseMatrces
 */
package model

import (
  "fmt"
  "bytes"
  "encoding/gob"
  "github.com/skelterjohn/go.matrix"
  "os"
)

type model_storable struct {
  //parameters
  Parameters *Model_parameters
  LogNormals_k map[int][][]float64 
  LogNormals_f map[int][][]float64
  Phi        map[int][][]float64
  Psi        map[int][][]float64
  N_k        map[int][][]float64 
  N_sum_k    map[int][][]float64 
  N_k_f      map[int][][]float64 
  N_k_sum_f  map[int][][]float64 
}


func (model *Model) to_storable() (m *model_storable) {
  
  m                 = new(model_storable)
  m.Parameters      = model.Parameters
  m.LogNormals_k    = map[int][][]float64{0:model.LogNormals_k[0].Arrays()}
  m.Phi             = map[int][][]float64{0:model.Phi[0].Arrays()}
  m.N_k             = map[int][][]float64{0:model.N_k[0].DenseMatrix().Arrays()}
  m.N_sum_k         = map[int][][]float64{0:model.N_sum_k[0].DenseMatrix().Arrays()}
  
  m.LogNormals_f    = make(map[int][][]float64 , m.Parameters.Num_categories)
  m.Psi             = make(map[int][][]float64 , m.Parameters.Num_categories)
  m.N_k_f           = make(map[int][][]float64 , m.Parameters.Num_categories)
  m.N_k_sum_f       = make(map[int][][]float64 , m.Parameters.Num_categories)
  
  for k:=0 ; k<m.Parameters.Num_categories ; k++ {
    m.LogNormals_f[k] = model.LogNormals_f[k].Arrays()
    m.Psi[k]          = model.Psi[k].Arrays()
    m.N_k_f[k]        = model.N_k_f[k].DenseMatrix().Arrays()
    m.N_k_sum_f[k]    = model.N_k_sum_f[k].DenseMatrix().Arrays()
  }
  return
}


func (model *model_storable) to_model() (m *Model) {
  m                 = New_model(model.Parameters)
  m.Parameters      = model.Parameters
  m.LogNormals_k    = map[int]*matrix.DenseMatrix{0:matrix.MakeDenseMatrixStacked(model.LogNormals_k[0])}
  m.Phi             = map[int]*matrix.DenseMatrix{0:matrix.MakeDenseMatrixStacked(model.Phi[0])}
  m.N_k             = map[int]*matrix.SparseMatrix{0:matrix.MakeDenseMatrixStacked(model.N_k[0]).SparseMatrix()}
  m.N_sum_k         = map[int]*matrix.SparseMatrix{0:matrix.MakeDenseMatrixStacked(model.N_sum_k[0]).SparseMatrix()}
  
  for k:=0 ; k<m.Parameters.Num_categories ; k++ {
    m.LogNormals_f[k] = matrix.MakeDenseMatrixStacked(model.LogNormals_f[k])
    m.Psi[k]          = matrix.MakeDenseMatrixStacked(model.Psi[k])
    m.N_k_f[k]        = matrix.MakeDenseMatrixStacked(model.N_k_f[k]).SparseMatrix()
    m.N_k_sum_f[k]    = matrix.MakeDenseMatrixStacked(model.N_k_sum_f[k]).SparseMatrix()
  }
  return
}


// Storing a go struct containing a codemap (for lemmas or c5 tags) in a file
func (m *Model) Store(filename string) {
  
  storable := m.to_storable()
  
  b := new(bytes.Buffer)
  g := gob.NewEncoder(b)
  err := g.Encode(storable)
  if err != nil {
    fmt.Println(err)
  }
  fh, eopen := os.OpenFile(filename, os.O_CREATE|os.O_WRONLY, 0666)
  defer fh.Close()
  if eopen != nil {
    fmt.Println(eopen)
  }
  _,ewrite := fh.Write(b.Bytes())
  if ewrite != nil {
    fmt.Println(ewrite)
  }
}

func Load_model(filename string) (model *Model){
  
  storable := new(model_storable)
  
  fh, err := os.Open(filename)
  if err != nil {
    fmt.Println(err)
  }
  dec := gob.NewDecoder(fh)
  err = dec.Decode(&storable)
  if err != nil {
    fmt.Println("loading model failed: ", err)
    return nil
  }
  return storable.to_model()
}
