package model

type Model_parameters struct {
  /* hyperparameters */
  A0        float64
  B0         float64
  Kappa_f      float64
  Kappa_c      float64
  /* other fixed parameters */
  Num_categories   int
  Num_genres       int
  /* misc known counts */
  Num_documents    int
  Num_concepts     int
  Num_features     int
  Num_timestamps   int
}


func New_model_parameters(a0, b0, kappa_f, kappa_c float64, numD, numT, numG, numTime, numTgt, numCxt int) (mp *Model_parameters) {
  mp = new(Model_parameters)
  mp.A0   = a0
  mp.B0    = b0
  mp.Kappa_f = kappa_f
  mp.Kappa_c = kappa_c
  mp.Num_documents    = numD
  mp.Num_categories   = numT
  mp.Num_genres       = numG
  mp.Num_concepts     = numTgt
  mp.Num_features     = numCxt
  mp.Num_timestamps   = numTime
  return
}

// func (m *Model) GetParameters() (*Model_parameters) {
//  return m.Parameters
// }


func (m *Model) GetParameter(mode string) (int) {
  if mode == "num_categories" {
    return m.Parameters.Num_categories
  } else if mode =="num_concepts" {
    return m.Parameters.Num_concepts
  } else if mode =="num_features" {
    return m.Parameters.Num_features
  }
  panic("unknown parameter!")
}
