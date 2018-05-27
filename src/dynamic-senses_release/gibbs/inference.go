package gibbs

import (
  "dynamic-senses_release/util"
  "dynamic-senses_release/data"
  "fmt"
)

/* take a model containing data and inference options
 *  run inference as specified in options */
func (s *Sampler) Estimate(verbose bool, test_corpus *data.Corpus, mode string) (err error) {

  num_categories := s.Model.GetParameter("num_categories")
  pK             := make([]float64, num_categories)
  pFgK           := make([]float64, num_categories)
  posterior      := make([]float64, num_categories)


  if mode == "independent" {
    err = s.estimate_independent(pK, pFgK, posterior, test_corpus)
  } else {
    err = s.estimate(pK, pFgK, posterior, test_corpus)
  }

  return err
}



func (s *Sampler) estimate(pK, pFgK, posterior []float64, test_corpus *data.Corpus) (err error){

  for iteration := 1 ; iteration <= s.iterations ; iteration++ {

    //if iteration == s.iterations {
    //    fmt.Println("\nTest loglikelihood: ", s.Model.Predict(test_corpus))
    //    fmt.Println("\nTrain loglikelihood: ", s.Model.Predict(s.Corpus))
    //}
    println(iteration)


    s.Resample_categories(pK, pFgK, posterior)
    err := Sample_logisticnormal_parameters_f("uniform",
                                     s.generator,
				     s.Model.Parameters.Num_timestamps,
             s.Model.Parameters.Num_genres,
				     s.Model.Parameters.Num_categories,
				     s.Model.Parameters.Num_features,
				     s.Model.Parameters.Kappa_f,
				     1,
				     s.Model.LogNormals_f,
				     s.Model.Psi,
				     s.Model.N_k_f,
				     s.Model.N_k_sum_f)
    if err!= nil {
      fmt.Println(s.Corpus.TargetFeatures.IDtoString, err)
      return err
    }
    err  = Sample_logisticnormal_parameters("uniform",
                                     s.generator,
				     s.Model.Parameters.Num_timestamps,
             s.Model.Parameters.Num_genres,
				     1,
				     s.Model.Parameters.Num_categories,
				     s.Model.Parameters.Kappa_c,
				     1,
				     s.Model.LogNormals_k,
				     s.Model.Phi,
				     s.Model.N_k,
				     s.Model.N_sum_k)

     if err!= nil {
       fmt.Println(s.Corpus.TargetFeatures.IDtoString, err)
       return err
     }
     if iteration%50==0 && iteration>100 {
       fmt.Println(iteration, " kappa_c", s.Model.Parameters.Kappa_c, "kappa_f", s.Model.Parameters.Kappa_f)
       fmt.Println(s.Model.N_k, "\n")
       fmt.Println(s.Model.Phi, "\n")
       fmt.Println(s.Model.LogNormals_k)

        s.post_reg += 0.3
        fmt.Println(s.post_reg)

       s.Model.Parameters.Kappa_c = Resample_kappa(s.Model.Parameters.Kappa_c,
                                                   s.Model.Parameters.A0,
                                                   s.Model.Parameters.B0,
						   s.Model.Parameters.Num_categories,
						   s.Model.Parameters.Num_timestamps,
               s.Model.Parameters.Num_genres,
						   s.Model.LogNormals_k)
     }
  }
  return err
}













func (s *Sampler) estimate_independent(pK, pFgK, posterior []float64, test_corpus *data.Corpus) (err error){

  for iteration := 1 ; iteration <= s.iterations ; iteration++ {

    println(iteration)

    s.Resample_categories(pK, pFgK, posterior)
    err := Sample_logisticnormal_parameters_independent_f("uniform",
                                     s.generator,
				     s.Model.Parameters.Num_timestamps,
             s.Model.Parameters.Num_genres,
				     s.Model.Parameters.Num_categories,
				     s.Model.Parameters.Num_features,
				     s.Model.Parameters.Kappa_f,
				     1,
				     s.Model.LogNormals_f,
				     s.Model.Psi,
				     s.Model.N_k_f,
				     s.Model.N_k_sum_f)
    if err!= nil {
      fmt.Println(s.Corpus.TargetFeatures.IDtoString, err)
      return err
    }
    err  = Sample_logisticnormal_parameters_independent("uniform",
                                     s.generator,
				     s.Model.Parameters.Num_timestamps,
             s.Model.Parameters.Num_genres,
				     1,
				     s.Model.Parameters.Num_categories,
				     s.Model.Parameters.Kappa_c,
				     1,
				     s.Model.LogNormals_k,
				     s.Model.Phi,
				     s.Model.N_k,
				     s.Model.N_sum_k)

     if err!= nil {
       fmt.Println(s.Corpus.TargetFeatures.IDtoString, err)
       return err
     }
     if iteration%50==0 && iteration>100 {
       fmt.Println(iteration, " kappa_c", s.Model.Parameters.Kappa_c, "kappa_f", s.Model.Parameters.Kappa_f)
       fmt.Println(s.Model.N_k, "\n")
       fmt.Println(s.Model.Phi, "\n")
       fmt.Println(s.Model.LogNormals_k)
     }
  }
  return err
}












func (s *Sampler) Resample_categories(pK, pFgK, posterior []float64) {
  /* resample categories (and keep model counts up-to-date) */
  for docIdx, doc := range(s.Corpus.Documents) {
    new_k := s.resample_category(doc, pK, pFgK, posterior)
    s.Corpus.Documents[docIdx].Label = new_k
  }
}



/* Takes one concept as input and resamples its category */
func (s *Sampler) resample_category(doc *data.Document, pK, pFgK, posterior []float64) (new_k int) {
  old_k := doc.Label
  s.Model.Update(old_k, doc.Target, doc.Context, doc.Time, -1)
//   s.Model.Posterior_categories(doc, posterior, pFgK, pK, doc.Time)
//   new_k  = util.GetSample(posterior)
  s.Model.Log_Posterior_categories(doc, posterior, pFgK, pK, doc.Time, /*s.post_reg*/1.0)
  new_k  = util.GetSampleLog_gen(s.generator, posterior)
  s.Model.Update(new_k, doc.Target, doc.Context, doc.Time, 1)
  return new_k
}
