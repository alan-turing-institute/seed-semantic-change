package model

import (
  "dynamic-senses_release/data"
  "dynamic-senses_release/util"
  "github.com/gonum/floats"
  "github.com/skelterjohn/go.matrix"
)


func (m *Model) hard_sense_clustering(t int) (hard_senses map[int]map[int]float64) {
    /* init hard cluster struct */
    hard_senses = make(map[int]map[int]float64, m.Parameters.Num_categories)
    for s:=0 ; s<m.Parameters.Num_categories ; s++ {
        hard_senses[s] = make(map[int]float64, 0)
    }

    /* return argmax_s p(f|s,t) for every f given t */
    for f:=0 ; f<m.Parameters.Num_features ; f++ {
        max_sense := 0
        max_prob  := 0.0
        for s:=0 ; s<m.Parameters.Num_categories ; s++ {
            if m.Psi[s].Get(t, f) > max_prob {
                max_prob = m.Psi[s].Get(t, f)
                max_sense= s
            }
        }
        hard_senses[max_sense][f] = max_prob
    }
    return
}

/* Input:   - model                                               *
 *          - time of interest                                    *
 *                                                                *
 *  Output:  - hard word-cluster assignments for time of interest *
 *          - map[sense] : matrix(1 x num_features)               */

func (m *Model) Hard_sense_clustering_matrix(t int) (hard_senses map[int]*matrix.DenseMatrix) {
    /* init hard cluster struct */
    hard_senses = make(map[int]*matrix.DenseMatrix, m.Parameters.Num_categories)
    for s:=0 ; s<m.Parameters.Num_categories ; s++ {
        hard_senses[s] = matrix.Zeros(1, m.Parameters.Num_features)
    }

    /* return argmax_s p(f|s,t) for every f given t */
    for f:=0 ; f<m.Parameters.Num_features ; f++ {
        max_sense := 0
        max_prob  := 0.0
        for s:=0 ; s<m.Parameters.Num_categories ; s++ {
            if m.Psi[s].Get(t, f) > max_prob {
                max_prob = m.Psi[s].Get(t, f)
                max_sense= s
            }
        }
        hard_senses[max_sense].Set(0,f,max_prob)
    }
    return
}
















func (m *Model) Top_features_given_k_t (k, t int, mode string) (psi []float64, indices []int) {
  if mode == "p_w_given_s" {
    psi = m.P_w_given_s(k)
  } else {
    for g:=0 ; g<m.Parameters.Num_genres ; g++ {   // TODO new
    //psi = Additive_logistic_transform(m.LogNormals_f[k].RowCopy(t)) //TODO old
       psi = Additive_logistic_transform(m.LogNormals_f[g][k].RowCopy(t)) //TODO old
    }
  }
  indices = make([]int, len(psi))
  floats.Argsort(psi, indices)
  return psi, indices
}

/* ***************************************************** *
 * Input: - model                                        *
 *        - document = [ target, {features...} ]         *
 * (1) p(w,s|t) = p(w|s,t) p(s|t)  // from model         *
 * (2) p(w|t)   = \sum_s p(t,s|w)  // marginalize senses *
 * (3) p(t|doc) = \prod_w p(w|t)   // from (2)           *
 *                                                       *
 * Output: (3)                                           *
 * ***************************************************** */

func (m *Model) P_t_given_doc(document *data.Document) (dist []float64) {
  dist = make([]float64, m.Phi[0].Rows())
  for t:=0 ; t<m.Phi[0].Rows() ; t++ {
    p_doc_given_t := 1.0
    for _,f := range(document.Context) {
      p_w_given_t := 0.0
      for k:=0 ; k<m.Phi[0].Cols() ; k++ {
        p_k_given_t  := m.Phi[0].Get(t,k)
        p_w_given_st := m.Psi[k].Get(t,f[0])
        p_w_given_t  += p_k_given_t * p_w_given_st
        // 	fmt.Println(p_k_given_t, p_w_given_st, p_w_given_t)
      }
      p_doc_given_t *= p_w_given_t
    }
    dist[t] = p_doc_given_t
  }
  return util.Normalize(dist, floats.Sum(dist))
}



/* ***************************************************** *
 * Input: - model                                        *                                                       *
 * Output: p(w|s) = \sum_t p(w|t,s)                      *
 * ***************************************************** */
func (m *Model) P_w_given_s(k int) (dist []float64) {
  dist = make([]float64, m.Psi[0].Cols())
  for w:=0 ; w<m.Psi[0].Cols() ; w++ {
    for t:=0 ; t<m.Phi[0].Rows() ; t++ {
      dist[w] += m.Psi[k].Get(t,w)
    }
  }
  return util.Normalize(dist, floats.Sum(dist))
}


/* ***************************************************** *
 * Input: - model                                        *                                                       *
 * Output: p(w|s) = \sum_t p(w|t,s)                      *
 * ***************************************************** */
func (m *Model) P_t_given_w(document *data.Document) (dist []float64) {
  dist = make([]float64, m.Phi[0].Rows())
  for t:=0 ; t<m.Phi[0].Rows() ; t++ {
    p_doc_given_t := 0.0
    for k:=0 ; k<m.Phi[0].Cols() ; k++ {
      p_w_given_tk := 1.0
      for _,f := range(document.Context) {
        p_w_given_tk  *= m.Psi[k].Get(t,f[0])
      }
      p_doc_given_t += p_w_given_tk
    }
    dist[t] = p_doc_given_t
  }
  return util.Normalize(dist, floats.Sum(dist))
}
