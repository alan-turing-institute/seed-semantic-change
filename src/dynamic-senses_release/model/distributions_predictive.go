package model

import (
  "math"
  "dynamic-senses_release/data"
  "dynamic-senses_release/util"
)

/* ***************************************************** *
 * Input: - model (<-parameters)                         *
 *        - corpus                                       *
 * Output:                                               *
 * log p(corpus|parameters)                              *
 *   = \sum_d log p(d|parameters)                        *
 *   = \sum_d \sum_k log p(k|parameters)                 *
 *                    + log p(w_d|k,parameters)          *
 *                                                       *
 * ***************************************************** */

func (m *Model) Predict(corpus *data.Corpus) (loglikelihood float64) {
  t_minus_1 := m.Parameters.Num_timestamps - 1
  for _,doc := range(corpus.Documents) {
    /* compute log p(d|model) */
    doc_likelihood := make([]float64, m.Parameters.Num_categories)

    //for g:=0 ; g<1 ; g++ {  //TODO was m.Parameters.Num_genres
      for k:=0 ; k<m.Parameters.Num_categories ; k++ {
        /* compute log p(d|k) */
        doc_likelihood[k] += math.Log(m.Phi[doc.Genre][0].Get(t_minus_1,k))
        for _,w := range(doc.Context) {
          doc_likelihood[k] += (math.Log(m.Psi[k].Get(t_minus_1,w[0]))) * float64(w[1])
        }
      }
    //}

    //for k:=0 ; k<m.Parameters.Num_categories ; k++ {
    //      print("doc_likelihood[k] ", doc_likelihood[k],"\n\n")
    //}
    //print("LOGLIKEHOOD BEFORE ", loglikelihood,"\n\n")
    //loglikelihood = 0
    //print("LOGLIKEHOOD zeroed ", loglikelihood,"\n\n")
    //print("LOGLIKEHOOD temp ", util.SumExp(doc_likelihood),"\n\n")
    loglikelihood += math.Log(util.SumExp(doc_likelihood))
    print("LOGLIKEHOOD AFTER ", loglikelihood,"\n\n")
  }
  return
}
