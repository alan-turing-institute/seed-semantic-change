#!/usr/bin/env Rscript

#Function to aggregate log-likelihood results across 50 train/test words.
#Input: likelihood results for each subcorpora
#Output: aggregated_loglike.txt file with mean +- sderr train and test loglike

all_files = list.files("./GTeval/subcorpora_GT/training_narr/", pattern="final_likelihoods.txt", recursive=TRUE, full.names=FALSE)
train_likelihoods = numeric(50)
test_likelihoods = numeric(50)
j = 1

for (filename in all_files){
  
  root = "./GTeval/subcorpora_GT/training_narr/"
  
  full_path = paste(root,filename,sep="")
  
  results = read.table(full_path)
  train_like = results$V2[1]
  test_like = results$V2[2]
  train_likelihoods[j] = train_like
  test_likelihoods[j] = test_like
  j = j + 1
}

print(cbind(train_likelihoods, test_likelihoods))

av_train_likelihood = mean(na.omit(train_likelihoods[train_likelihoods!=0])) #removing zeros for now (should check why two words are not working)
av_test_likelihood = mean(na.omit(test_likelihoods[test_likelihoods!=0])) #removing zeros for now 
sderr_train_likelihood = sd(na.omit(train_likelihoods[train_likelihoods!=0])) / length(na.omit(test_likelihoods[train_likelihoods!=0]))
sderr_test_likelihood = sd(na.omit(test_likelihoods[test_likelihoods!=0])) / length(na.omit(test_likelihoods[test_likelihoods!=0]))

sink('GTeval/aggregated_loglike_subGT.txt')
cat(sprintf("train loglikelihood: %f +- %f \n", av_train_likelihood, sderr_train_likelihood))
cat(sprintf("test loglikelihood: %f +- %f", av_test_likelihood, sderr_test_likelihood))
sink()
print("aggregated_loglike_subGT.txt created!")
