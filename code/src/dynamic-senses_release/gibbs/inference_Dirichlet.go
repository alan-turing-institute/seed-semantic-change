package gibbs

import (
  "dynamic-senses_release/util"
  "dynamic-senses_release/data"
  "fmt"
)

/* take a model containing data and inference options
 *  run inference as specified in options */
func (s *Sampler) Estimate_Dirichlet(verbose bool, test_corpus *data.Corpus) (err error) {
    
  num_categories := s.Model.GetParameter("num_categories")
  pK             := make([]float64, num_categories)
  pFgK           := make([]float64, num_categories)
  posterior      := make([]float64, num_categories)
  
  err = s.estimate_Dirichlet(pK, pFgK, posterior, test_corpus)
  return err
}



func (s *Sampler) estimate_Dirichlet(pK, pFgK, posterior []float64, test_corpus *data.Corpus) (err error){
  
  for iteration := 1 ; iteration <= s.iterations ; iteration++ {
    println(iteration)
    
    s.Resample_categories_Dirichlet(pK, pFgK, posterior)

    if iteration%10 ==0 {
      fmt.Println("\nLoglikelihood: ", s.Model.Predict(s.Corpus))
    }
    
    if iteration%1000==0 {
       s.Model.Print_categories(10, s.Corpus.TargetFeatures.IDtoString, s.Corpus.ContextFeatures.IDtoString)
     }
  }
  return err
}


func (s *Sampler) Resample_categories_Dirichlet(pK, pFgK, posterior []float64) {
  /* resample categories (and keep model counts up-to-date) */
  for docIdx, doc := range(s.Corpus.Documents) {
    new_k := s.resample_category_Dirichlet(doc, pK, pFgK, posterior)
    s.Corpus.Documents[docIdx].Label = new_k
  }
}



/* Takes one concept as input and resamples its category */
func (s *Sampler) resample_category_Dirichlet(doc *data.Document, pK, pFgK, posterior []float64) (new_k int) {

  old_k := doc.Label
  s.Model.Print()
  s.Model.Update(old_k, doc.Target, doc.Context, doc.Time, -1)
  s.Model.Print()
  s.Model.Log_Posterior_categories_Dirichlet(doc, posterior, pFgK, pK, doc.Time, 0.5, 0.1)

  new_k  = util.GetSampleLog_gen(s.generator, posterior)
  fmt.Println(new_k)
  s.Model.Update(new_k, doc.Target, doc.Context, doc.Time, 1)
  s.Model.Print()
  return new_k
}
