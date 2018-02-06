package model

import (
  "math"
  "fmt"
  "dynamic-senses_release/data"
  "dynamic-senses_release/util"
  "github.com/gonum/floats"
)


/* *****************************************************************************************************
 * **************************************         POSTERIOR         ************************************
 * *****************************************************************************************************
 *                          N(k,c) + \beta                                      exp(psi(t,k,f))
 *         P(k|c,f) \propto -----------------  x  N(k) + \alpha   x  \prod_f ------------------------
 *                         N(k,.) + C*\beta                                  \sum_f' exp(psi(t,k,f'))
 */
func (model *Model) Posterior_categories(doc *data.Document, posterior, pFgKT, pKgT []float64, time int) {
  model.pCategoryGivenT_distribution(pKgT, time)
  util.Normalize(pKgT, floats.Sum(pKgT))
  model.pFeaturesGivenKT_distribution(pFgKT, doc.Context, doc.Time)
  util.Normalize(pFgKT, floats.Sum(pFgKT))
  for k,_ := range(pKgT) {
    posterior[k] = pKgT[k]  * pFgKT[k]
  }
  util.Normalize(posterior, floats.Sum(posterior))
  return
}  

func (model *Model) Log_Posterior_categories(doc *data.Document, posterior, pFgKT, pKgT []float64, time int, regularizer float64) {
  model.log_pCategoryGivenT_distribution(pKgT, time)
  model.log_pFeaturesGivenKT_distribution(pFgKT, doc.Context, doc.Time)
  for k,_ := range(pKgT) {
    posterior[k] = pKgT[k] + (regularizer * pFgKT[k])
  }
  return
}  


/* *************************************************************************
 *                              exp(psi(t,k,f))
 *         P(f|k) \propto -----------------------------
 *                          \sum_f' exp(psi(t,k,f'))
 */

func (m *Model) pFeaturesGivenKT_distribution(dist []float64, fs [][2]int, time int) {
  for k:=0 ; k<m.Parameters.Num_categories ; k++ {
    dist[k] = 1.0
    for _,feature := range(fs) {
     dist[k] *= math.Pow(m.Psi[k].Get(time,feature[0]), float64(feature[1]))
    }
  }
}



func (m *Model) log_pFeaturesGivenKT_distribution(dist []float64, fs [][2]int, time int) {
  for k:=0 ; k<m.Parameters.Num_categories ; k++ {
    dist[k] = 0.0
    for _,feature := range(fs) {
      dist[k] += (float64(feature[1]) * math.Log(m.Psi[k].Get(time,feature[0])))
      if math.IsNaN(dist[k]) {
	fmt.Println("NaN at p(w|s,t)[s][t]", k, time, feature[0], m.Psi[k].RowCopy(time)[feature[0]])
      }
    }
  }
}




func (m *Model) pCategoryGivenT_distribution(dist []float64, time int) {
  for k:=0 ; k<m.Parameters.Num_categories ; k++ {
    dist[k] = m.Phi[0].Get(time,k)
  }
}



func (m *Model) log_pCategoryGivenT_distribution(dist []float64, time int) {
  for k:=0 ; k<m.Parameters.Num_categories ; k++ {
    dist[k] = math.Log(m.Phi[0].Get(time,k))
    if math.IsNaN(dist[k]) {
      fmt.Println("NaN at p(s|t)[s]", k, m.Phi[k].RowCopy(time))
    }
  }
}
