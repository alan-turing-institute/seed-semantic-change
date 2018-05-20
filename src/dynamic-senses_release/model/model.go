/*
 *  Implementation of the dynamic BayesCat model
 *  Definition of the model type, and functionality for
 *  -initialization
 *  -inference
 *  -modelLikelihood computation
 */
package model

import (
//  "fmt"
  "dynamic-senses_release/data"
  "github.com/skelterjohn/go.matrix"
  "dynamic-senses_release/util"
)

type Model struct {
  //parameters
  Parameters *Model_parameters
  LogNormals_k map[int]*matrix.DenseMatrix

  //LogNormals_f map[int]*matrix.DenseMatrix  //TODO old
  LogNormals_f []map[int]*matrix.DenseMatrix  //TODO new might need to revert this? depends on model we use. shared or different variances? I would say different to have different trajectory variances.

  //Phi        map[int]*matrix.DenseMatrix  //TODO old
  Phi        []map[int]*matrix.DenseMatrix  //TODO old
  Psi        map[int]*matrix.DenseMatrix
  N_k        map[int]*matrix.SparseMatrix //map[int][][]int  //TODO??
  N_sum_k    map[int]*matrix.SparseMatrix //map[int][][]int  //TODO??
  N_k_f      map[int]*matrix.SparseMatrix //map[int][][]int   //TODO ?
  N_k_sum_f  map[int]*matrix.SparseMatrix //map[int][]int  //TODO ?
}

func New_model(parameters *Model_parameters) (m *Model) {
  m                 = new(Model)
  m.Parameters      = new(Model_parameters)
  m.Parameters      = parameters
  m.LogNormals_k    = make(map[int]*matrix.DenseMatrix, 1)
  m.LogNormals_k[0] = matrix.Zeros(m.Parameters.Num_timestamps, m.Parameters.Num_categories)

  //m.LogNormals_f    = make(map[int]*matrix.DenseMatrix, m.Parameters.Num_categories) //TODO old
  m.LogNormals_f    = make([]map[int]*matrix.DenseMatrix, m.Parameters.Num_genres)  //TODO new
  for idx, _ := range(m.LogNormals_f) {  //TODO new
      m.LogNormals_f[idx] = make(map[int]*matrix.DenseMatrix, m.Parameters.Num_categories) //TODO new
  }  //TODO new

  //m.Phi             = make(map[int]*matrix.DenseMatrix, 1) //TODO old
  //m.Phi[0]          = matrix.Zeros(m.Parameters.Num_timestamps, m.Parameters.Num_categories) //TODO old

  m.Phi             = make([]map[int]*matrix.DenseMatrix, m.Parameters.Num_genres)
  for idx, _ := range(m.Phi) {  //TODO new
      m.Phi[idx] = make(map[int]*matrix.DenseMatrix, 1)
      m.Phi[idx][0]          = matrix.Zeros(m.Parameters.Num_timestamps, m.Parameters.Num_categories)
  }




  m.Psi             = make(map[int]*matrix.DenseMatrix, parameters.Num_categories)
  m.N_k             = make(map[int]*matrix.SparseMatrix, 1)
  m.N_sum_k         = make(map[int]*matrix.SparseMatrix, 1)
  m.N_k[0]          = matrix.ZerosSparse(m.Parameters.Num_timestamps, m.Parameters.Num_categories)
  m.N_sum_k[0]      = matrix.ZerosSparse(m.Parameters.Num_timestamps, 1)
  m.N_k_f           = make(map[int]*matrix.SparseMatrix, parameters.Num_categories)
  m.N_k_sum_f       = make(map[int]*matrix.SparseMatrix, parameters.Num_categories)
  for g:=0 ; g<m.Parameters.Num_genres ; g++ {
    print("genre index: ", g, "\n")
    for k:=0 ; k<parameters.Num_categories ; k++ {
      //m.LogNormals_f[k] = matrix.Zeros(m.Parameters.Num_timestamps, m.Parameters.Num_features) //TODO old
      m.LogNormals_f[g][k] = matrix.Zeros(m.Parameters.Num_timestamps, m.Parameters.Num_features) //TODO new
      m.Psi[k]          = matrix.Zeros(m.Parameters.Num_timestamps, m.Parameters.Num_features)
      m.N_k_f[k]        = matrix.ZerosSparse(m.Parameters.Num_timestamps, m.Parameters.Num_features)
      m.N_k_sum_f[k]    = matrix.ZerosSparse(m.Parameters.Num_timestamps,1)
    }
  }
  return
}


func (m *Model) Initialize_batch(corpus *data.Corpus) {
  for _,doc := range(corpus.Documents) {
    m.Update(doc.Label, doc.Target, doc.Context, doc.Time, 1)
  }
  for tt:=0 ; tt<m.Parameters.Num_timestamps ; tt++ {
    for g:=0 ; g<m.Parameters.Num_genres ; g++ {  //TODO new
      for kk:=0 ; kk<m.Parameters.Num_categories ; kk++ {
        m.Phi[g][0].Set(tt, kk, (m.N_k[0].Get(tt,kk)+0.01) / (m.N_sum_k[0].Get(tt,0)+float64(m.Parameters.Num_categories)*0.01))
        for vv:=0 ; vv<m.Parameters.Num_features ; vv++ {
  	m.Psi[kk].Set(tt, vv, (m.N_k_f[kk].Get(tt,vv)+0.01) / (m.N_k_sum_f[kk].Get(tt,0)+float64(m.Parameters.Num_features)*0.01))
        }
        //m.LogNormals_f[kk].FillRow(tt, Inverse_alt(m.Psi[kk].RowCopy(tt))) ///TODO old
        m.LogNormals_f[g][kk].FillRow(tt, Inverse_alt(m.Psi[kk].RowCopy(tt))) ///TODO new
      }
      m.LogNormals_k[0].FillRow(tt, Inverse_alt(m.Phi[g][0].RowCopy(tt)))
    }
  }
}


func (m *Model) Update(category, concept int, features [][2]int, time int, incr float64) {
  util.Increment(m.N_k[0]       , time    , category, incr)
  util.Increment(m.N_sum_k[0]   , time    , 0       , incr)
  for _,f := range(features) {
    util.Increment(m.N_k_f[category]    , time    , f[0]   , incr * float64(f[1]))
    util.Increment(m.N_k_sum_f[category], time    , 0      , incr * float64(f[1]))
  }
}
