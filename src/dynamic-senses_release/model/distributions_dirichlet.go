package model

import (
  "math"
  "fmt"
  "dynamic-senses_release/data"
)


/* *****************************************************************************************************
 * **************************************         POSTERIOR         ************************************
 * *****************************************************************************************************
 *                          N(k,c) + \beta                                      exp(psi(t,k,f))
 *         P(k|c,f) \propto -----------------  x  N(k) + \alpha   x  \prod_f ------------------------
 *                         N(k,.) + C*\beta                                  \sum_f' exp(psi(t,k,f'))
 */


func (model *Model) Log_Posterior_categories_Dirichlet(doc *data.Document, posterior, pFgKT, pKgT []float64, time int, alpha, beta float64) {
  model.log_pCategoryGivenT_Dirichlet(pKgT, time, alpha)
  model.log_pFeaturesGivenKT_Dirichlet(pFgKT, doc.Context, doc.Time, beta)
  for k,_ := range(pKgT) {
    posterior[k] = pKgT[k] + (pFgKT[k])
  }
  return
}  


/* *************************************************************************
 *                              exp(psi(t,k,f))
 *         P(f|k) \propto -----------------------------
 *                          \sum_f' exp(psi(t,k,f'))
 */


func (m *Model) log_pFeaturesGivenKT_Dirichlet(dist []float64, fs [][2]int, time int, beta float64) {
  for k:=0 ; k<m.Parameters.Num_categories ; k++ {
    num, den := 0.0, 0.0
    nfs := 0.0
    for _,f := range(fs) {
      for nf:=0 ; nf<f[1] ; nf++ {
        num += math.Log(m.N_k_f[k].Get(time,f[0]) + float64(nf)  + beta )
        den += math.Log(m.N_k_sum_f[k].Get(time,1) + float64(nfs) + (float64(m.Parameters.Num_features) * beta) )
        nfs++
      }
    }
    dist[k] = num - den
  }
}


func (m *Model) log_pCategoryGivenT_Dirichlet(dist []float64, time int, alpha float64) {
  for k:=0 ; k<m.Parameters.Num_categories ; k++ {
    dist[k] = math.Log(m.N_k[0].Get(time, k)+alpha)
    if math.IsNaN(dist[k]) {
      fmt.Println("NaN at p(s|t)[s]", k, m.N_k[0].Get(time, k))
    }
  }
}
