package gibbs

import ( 
"fmt"
"math/rand"
"math"
"time"
"dynamic-senses_release/model"
"github.com/skelterjohn/go.matrix"
"code.google.com/gostat/stat"
"errors"
)



func Sample_logisticnormal_parameters(mode string, generator *rand.Rand, t, k, v int, kappa float64, iterations int, 
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
            
            switch {
              case tt==0:
                mu    = logNormals[kk].Get(tt+1,vv)
                sigma = math.Sqrt(1.0/(1.0*kappa))
              case tt==t-1:
                mu    = logNormals[kk].Get(tt-1,vv)
                sigma = math.Sqrt(1.0/(1.0*kappa))
              default:
                mu    = 0.5*(logNormals[kk].Get(tt-1,vv)+logNormals[kk].Get(tt+1,vv))
                sigma = math.Sqrt(1.0/(2.0*kappa))
            }
            
            threshold := math.Exp(logNormals[kk].Get(tt,vv))/denom
            c := c_full - math.Exp(logNormals[kk].Get(tt,vv))
            
                          
              lower_bound, upper_bound = Sample_uniform(generator, kk, tt, vv, threshold, total_data, n_k_f)

              upper_bound = math.Log(c*upper_bound/(1.0-upper_bound))
              lower_bound = math.Log(c*lower_bound/(1.0-lower_bound))
              
              if lower_bound >= upper_bound {
                fmt.Println(ii, t, k,upper_bound, lower_bound,total_data)
                panic("lowerbound >= upperbound!")
              }
              
              //           if mode == "beta" {
              //             if n_k_f[kk].Get(tt,vv) == 0 {
              //               lower_bound = math.Inf(-1)
              //             } else if total_data-n_k_f[kk].Get(tt,vv) == 0 {
              //               upper_bound = math.Inf(1)
              //             }
              //           }
              
              new_phi = SampleTruncatednormal(generator, 1, mu, sigma, lower_bound, upper_bound)[0]
              
              if math.IsNaN(new_phi) || math.IsNaN(upper_bound) || math.IsNaN(lower_bound) || math.IsNaN(mu) || math.IsNaN(sigma) || math.IsNaN(threshold){
                fmt.Println(kk, tt, vv, n_k_f[kk].Get(tt,vv), total_data,  n_k_sum_f[kk].String())
                fmt.Printf("phi %.3f, lo %.3f, up %.3f, mu %.3f, sigma %.3f, c %.3f, c_full %.3f, thres %.3f\n\n", new_phi, lower_bound, upper_bound, mu, sigma, c, c_full, threshold)
                err = errors.New("NaN in lognormal resampling!")
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



func compute_constant(beta []float64, k int) (c float64) {
  for i:=0 ; i<len(beta) ; i++ {
    if i!=k {c+=math.Exp(beta[i])}
  }
  return
}

func compute_constant_full(beta []float64) (c float64) {
  for i:=0 ; i<len(beta) ; i++ {
    c+=math.Exp(beta[i])
  }
  return
}




func Sample_many(generator *rand.Rand, n, t, k int, threshold, total_data float64, data map[int]*matrix.SparseMatrix) (float64, float64) {
  z := 0.0
  lower_bound := 0.0
  upper_bound := 1.0
  /* draw data[k] RVs in [0,threshold] */
  for i:=0 ; i<int(data[n].Get(t,k)) ; i++ {
    z = generator.Float64() * (threshold-0) + 0
    if z > lower_bound {lower_bound = z}
  }
  /* draw D-data[k] RVs in [threshold,1] */
  for i:=0 ; i<int(total_data - data[n].Get(t,k)) ; i++ {
    z = generator.Float64() * (1-threshold) + threshold
    if z < upper_bound {upper_bound = z}
  }
  return lower_bound, upper_bound
}



func Sample_beta(n, t, k int, threshold, total_data float64, data map[int]*matrix.SparseMatrix) (float64, float64) {
  lower_bound := stat.NextBeta(data[n].Get(t,k), 1                   ) * (threshold - 0        ) + 0
  upper_bound := stat.NextBeta(1.0    , total_data - data[n].Get(t,k)) * (1.0       - threshold) + threshold
  return lower_bound, upper_bound
}



func Sample_uniform(generator *rand.Rand, n, t, k int, threshold, total_data float64, data map[int]*matrix.SparseMatrix) (float64, float64) {
  
  
  lower_bound :=        math.Pow(generator.Float64(), 1.0 /  data[n].Get(t,k)               ) * (threshold - 0        ) + 0
  upper_bound := (1.0 - math.Pow(generator.Float64(), 1.0 / (total_data - data[n].Get(t,k)))) * (1.0       - threshold) + threshold
  
  return lower_bound, upper_bound
}
