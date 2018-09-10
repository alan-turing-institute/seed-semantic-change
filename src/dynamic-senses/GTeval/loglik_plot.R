#To use this from terminal, go into the folder where loglik_plot.R is stored and then type
#Rscript loglik_plot.R
#You might need to change this script by specifying your paths in all_files and root

#Function to plot heldout loglikelihood.
#Input: likelihood results for each parameter setting
#Output: loglik_plot.png file with mean +- sderr train and test loglike

library(stringi)
library(ggplot2)

all_files = list.files("./GTeval/aggregated_loglike_folder_GOOD/", pattern = "aggregated_loglike_it100_",
                       recursive=TRUE, full.names=FALSE)
#loglik_train <- matrix(NA, nrow = 2*length(all_files), ncol = 4)

loglik_train <- matrix(NA, nrow = length(all_files), ncol = 3)
loglik_test <- matrix(NA, nrow = length(all_files), ncol = 3)
colnames(loglik_train) <- c("loglik", "sderr", "param_set")
colnames(loglik_test) <- c("loglik", "sderr", "param_set")
loglik_test <- as.data.frame(loglik_test)

j <- 1
for (filename in all_files){
  loglik_test[j, 3] <- unlist(strsplit(filename, "it100_Top"))[2]
  root <- "./GTeval/aggregated_loglike_folder_GOOD/"
  full_path <- paste(root,filename,sep="")
  results <- read.table(full_path)
  loglik_test[j, 1:2] <- as.numeric(results[2, c(3, 5)])
  j <- j + 1
}

for (i in 1:length(all_files)){
  loglik_test$K[i] <- unlist(strsplit(as.character(loglik_test$param_set[i]),"\\_"))[1]
  loglik_test$other[i] <- unlist(stri_split_fixed(str = as.character(loglik_test$param_set[i]), pattern = "_", n = 2))[2]
}

loglik_test$model <- ifelse(stri_detect_fixed(as.character(loglik_test$param_set),"M"), "SCAN", "GTall" )
loglik_test$model <- ifelse(stri_detect_fixed(as.character(loglik_test$param_set),"narr"),  "GTnarr",loglik_test$model)
loglik_test$model <- as.factor(loglik_test$model)


loglik_test$param_code<- ifelse(stri_detect_fixed(as.character(loglik_test$other),"k10_"), 1, 2)
loglik_test$param_code <- ifelse(stri_detect_fixed(as.character(loglik_test$other),"a1b1_"),  3,loglik_test$param_code)
loglik_test$param_code <- as.factor(loglik_test$param_code)

loglik_test$comb <- as.factor(paste0(loglik_test$model,"_", loglik_test$param_code))

loglik_test$K <- as.numeric(loglik_test$K)

print(loglik_test)
#print(str(loglik_test$K))

heldoutplot<- ggplot(data = loglik_test, aes(x = K)) +
  theme_bw() +
  theme(text=element_text(size=15), legend.position = "bottom") +
  guides(col = guide_legend(ncol=3)) + 
  scale_x_continuous(minor_breaks = NULL, breaks = seq(5, 20, 5)) + 
  scale_y_continuous(minor_breaks = seq(-34000, -20000, 1000), breaks = seq(-34000, -20000, 2000)) + 
  geom_line(aes(y = loglik , col=comb), lwd = 1.1)+ #, col=comb
  #geom_text(aes(y = loglik, label=param_code, col=comb),hjust=0, vjust=0) +  
  geom_ribbon(aes(ymin=loglik - sderr, ymax=loglik + sderr, col = comb), alpha=0.05, linetype="dotted") + #"dashed" 
  labs(y = "Held-out log-likelihood",colour = "Models") + 
  scale_color_brewer(palette="Set1", direction = -1) 

print(heldoutplot)

ggsave('GTeval/heldoutplot.png', heldoutplot)

print("heldoutplot created!")
