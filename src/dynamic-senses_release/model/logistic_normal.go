package model

import (
      "math"
)

func Additive_logistic_transform(x []float64) (transf []float64) {
  max := math.Inf(-1)
  transf  = make([]float64, len(x))
  denom  := 0.0
  
  for _,v := range(x) {
    if v>max {max=v}
  }
  for k:=0 ; k<len(x) ; k++ {denom    += math.Exp(x[k]-max)}
  for k,v := range(x)       {transf[k] = math.Exp(v-max)/denom}
  
  return
}




func Inverse_alt(x []float64) (inv []float64) {
  inv = make([]float64, len(x))
  for k:=0 ; k<=len(x)-1 ; k++ {
    inv[k] = math.Log(x[k] / x[len(x)-1])
  }
  return
}
