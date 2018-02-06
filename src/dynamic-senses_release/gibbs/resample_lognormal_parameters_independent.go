package gibbs

import ( 
"fmt"
"math/rand"
"math"
"time"
"dynamic-senses_release/model"
"github.com/skelterjohn/go.matrix"
"errors"
)



func Sample_logisticnormal_parameters_independent(mode string, generator *rand.Rand, t, k, v int, kappa float64, iterations int, 
                                      logNormals, psi map[int]*matrix.DenseMatrix, n_k_f, n_k_sum_f map[int]*matrix.SparseMatrix) (err error) {
  for ii:=0 ; ii<iterations ; ii++ {
    
    semaphore := make(chan int , k)
    for kk:=0 ; kk<k ; kk++ {
      go func(kk int) {
        var new_phi float64
        
        generator := rand.New(rand.NewSource(time.Now().UTC().UnixNano()))
        for tt:=0 ; tt < t ; tt++ {
          total_data := n_k_sum_f[kk].Get(tt,0)
          
          /* compute full constant */
          c_full := compute_constant_full(logNormals[kk].RowCopy(tt))
          
          /* struct for storing tmp beta updates before updating the vector in the end after updating each component */
          tmp_betas := make([]float64, psi[kk].Cols())
          /* pre-compute threshold denominator */
          denom:=0.0        
          for _,val := range(logNormals[kk].RowCopy(tt)) {denom+=math.Exp(val)}
          
          for vv:=0 ; vv<v ; vv++ {
            
            upper_bound, lower_bound := 0.0, 0.0
            var mu, sigma float64
            
            mu    = 0
            sigma = 0.5
            
            threshold := math.Exp(logNormals[kk].Get(tt,vv))/denom
            c := c_full - math.Exp(logNormals[kk].Get(tt,vv))
            
                          
              lower_bound, upper_bound = Sample_uniform(generator, kk, tt, vv, threshold, total_data, n_k_f)

              upper_bound = math.Log(c*upper_bound/(1.0-upper_bound))
              lower_bound = math.Log(c*lower_bound/(1.0-lower_bound))
              
              if lower_bound >= upper_bound {
                fmt.Println(ii, t, k,upper_bound, lower_bound,total_data)
                panic("lowerbound >= upperbound!")
              }
              
              new_phi = SampleTruncatednormal(generator, 1, mu, sigma, lower_bound, upper_bound)[0]
              
              if math.IsNaN(new_phi) || math.IsNaN(upper_bound) || math.IsNaN(lower_bound) || math.IsNaN(mu) || math.IsNaN(sigma) || math.IsNaN(threshold){
                fmt.Println(kk, tt, vv, n_k_f[kk].Get(tt,vv), total_data)
                fmt.Println(logNormals[kk].RowCopy(tt))
                fmt.Printf("phi %.3f, lo %.3f, up %.3f, mu %.3f, sigma %.3f, c %.3f, c_full %.3f, thres %.3f\n\n", new_phi, lower_bound, upper_bound, mu, sigma, c, c_full, threshold)
                err = errors.New("NaN in lognormal resampling!")
                panic(err)
              }

            tmp_betas[vv] = new_phi
            
          }
          logNormals[kk].FillRow(tt, tmp_betas)
          psi_k := model.Additive_logistic_transform(logNormals[kk].RowCopy(tt))
          psi[kk].FillRow(tt, psi_k)
        }
        semaphore <- 1
      }(kk);
    }
    for ss:=0 ; ss<k ; ss++ {<- semaphore}
  }
  return err
}
