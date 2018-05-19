#!/usr/bin/env Rscript
#Function to aggregate log-likelihood results across 50 train/test words.
#Input: likelihood results for each subcorpora
#Output: aggregated_loglike.txt file with mean +- sderr train and test negative loglike

all_files = list.files("./greek_input/subcorpora/training/", pattern="final_likelihoods.txt", recursive=TRUE, full.names=FALSE)

train_likelihoods = numeric(50)
test_likelihoods = numeric(50)
j = 1

for (filename in all_files){
  root = "./greek_input/subcorpora/training/"
  
  full_path = paste(root,filename,sep="")
  
  results = read.table(full_path)
  train_like = results$V2[1]
  test_like = results$V2[2]
  
  train_likelihoods[j] = train_like
  test_likelihoods[j] = test_like
  j = j + 1
}

av_train_likelihood = mean(train_likelihoods[train_likelihoods!=0]) #removing zeros for now (should check why two words are not working)
av_test_likelihood = mean(test_likelihoods[test_likelihoods!=0]) #removing zeros for now 
sderr_train_likelihood = sd(train_likelihoods[train_likelihoods!=0]) / length(test_likelihoods[train_likelihoods!=0])
sderr_test_likelihood = sd(test_likelihoods[test_likelihoods!=0]) / length(test_likelihoods[test_likelihoods!=0])

sink('aggregated_loglike.txt')
cat(sprintf("train loglikelihood: %f +- %f \n", av_train_likelihood, sderr_train_likelihood))
cat(sprintf("test loglikelihood: %f +- %f", av_test_likelihood, sderr_test_likelihood))
sink()

print("aggregated_loglike.txt file created!")
