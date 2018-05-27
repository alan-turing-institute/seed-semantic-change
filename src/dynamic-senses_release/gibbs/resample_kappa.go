package gibbs

import (
  "math"
  "code.google.com/gostat/stat"
  "github.com/skelterjohn/go.matrix"
  "dynamic-senses_release/slicesampler"
  "fmt"
  numstat "github.com/gonum/stat"
)



func Resample_kappa(old_kappa, a0, b0 float64, k, t int, g int, phi []map[int]*matrix.DenseMatrix) (new_kappa float64) {
  a,b      := Posterior_parameters(a0, b0, k, t, g, phi)
  new_kappa = stat.NextGamma(a , b)
  return
}




func Posterior_parameters(a0,b0 float64, k,t int, g int, phi []map[int]*matrix.DenseMatrix) (a,b float64) {
  a  = a0 + (float64(k*t)/2.0)
  b  = 0.0

  for gg:=0 ; gg<g ; gg++ {
    for kk:=0 ; kk<k ; kk++ {
      /* compute category-specific mean */
      mu_k := numstat.Mean(phi[g][0].ColCopy(kk), nil)

      for tt:=0 ; tt<t ; tt++ {
      b += math.Pow(phi[g][0].Get(tt,kk) - mu_k , 2)
      }
    }
  }
  fmt.Println(b0, b)
  b = b0+ (b / 2.0)
  return
}


func slice_update(val0 float64, log_prob func(float64)float64, size, max, lower, upper float64, num_samples, thin int) (samples []float64) {
  samples = make([]float64, num_samples)
  val := val0
  samples[0] = val0
  last_val := 0.0

  for i:=0 ; i<num_samples ; i++ {
    println(i)
    for j:=0 ; j<thin ; j++ {
      val = slicesampler.Sample(val, log_prob, size, max, lower, upper, last_val)
    }
    samples[i] = val
  }
  return samples
}
