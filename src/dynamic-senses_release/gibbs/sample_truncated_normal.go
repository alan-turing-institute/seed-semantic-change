package gibbs

import (
      "math"
      "math/rand"
      "os/exec"
      "strconv"
      "strings"
      "github.com/gonum/stat/dist"
)

const MIN_VAL float64 = 0.000000001
const MAX_VAL float64 = 1.0 - MIN_VAL

/* Avoid the argument to Quantile() being zero or one
 * since this would result in +/-Infinity values
 * returned from the Inverse Transform sampler 
 * -> use MIN_VAL / MAX_VAL if necessary
 *
 * Input: - mu and sigma (i.e. std.dev NOT variance)
 *        - lower and upper bound
 *        - num samples
 *        - random number generator
 */ 
func SampleTruncatednormal(generator *rand.Rand, n int, mean, sigma, lower, upper float64) (rvs []float64) {
  var rv_uni float64
  rvs       = make([]float64, n)
  nrm      := dist.Normal{}
  nrm.Mu    = mean
  nrm.Sigma = sigma
  f_low := nrm.CDF(lower)
  f_up  := nrm.CDF(upper)
  for ii:=0 ; ii<n ; ii++ {
    rv_uni  = f_low + (f_up-f_low)*generator.Float64()
    if rv_uni == 0.0 {
      rv_uni = MIN_VAL
    } else if rv_uni == 1.0 {
      rv_uni = MAX_VAL
    }
    rvs[ii] = nrm.Quantile(rv_uni)
  }
  return
}



func SampleTruncatednormal_R(n int, lo, up, mu, sigma float64) (rvs []float64) {
  rvs    = make([]float64, n)
  tngen := new(exec.Cmd)
  args  := []string{"Rscript", 
                   "/home/lea/code/r/truncated_normal/truncnorm.r", 
		   strconv.Itoa(n),
                   strconv.FormatFloat(lo,   'f', -1, 64),
                   strconv.FormatFloat(up,   'f', -1, 64),
                   strconv.FormatFloat(mu,   'f', -1, 64),
                   strconv.FormatFloat(sigma,'f', -1, 64)}
  tngen.Args = args
  tngen.Path = "/usr/bin/Rscript"
  out, err := tngen.Output()
  if err!= nil {panic(err)}
  
//   fmt.Println(">>", lo, up, mu, sigma, string(out))
  
  if n==1 {
    rvs[0], err = strconv.ParseFloat(strings.TrimSpace(string(out)), 64)
    if err!= nil {panic(err)}
    return
  }
  outputs := strings.Split(string(out), " ")
  
  for i,str := range(outputs) {
    y, err := strconv.ParseFloat(strings.TrimSpace(str), 64)
    if err!= nil {panic(err)}
    rvs[i]  = y
  }
  return 
}

func SampleTruncatednormal_bruteforce(mean, stddev, lower, upper float64) (x float64) {
  count := 0
  for x = math.Inf(-1) ; x<lower || x>upper ; count++ {
    x = rand.NormFloat64() * stddev + mean
//     if count > 10000 {
//       return math.Inf(-1)
//     }
  }
  return
}
