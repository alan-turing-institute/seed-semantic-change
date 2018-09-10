### Usage: Rscript barchart.R <path-to-your-output.dat-file> <path-where-to-save-plot>
### Example: Rscript barchart.R output/59339/output.dat 59339/plotname.png


args <- commandArgs(trailingOnly = TRUE)
path <- as.character(args[1])
titleplot <- as.character(args[2])

library(ggplot2)
library(magrittr)
library(stringr)

### Import the output.txt data ###########################################
### take start_time, end_time, dT ########################################

con <- file(path, "r")
first_lines <- readLines(con, n = 2)
close(con)

aaa <- unlist(strsplit(first_lines, ", ")) 


targetword <-  which(grepl("(", aaa, fixed = TRUE) == TRUE)[1] %>% 
  aaa[.] %>% 
  str_extract_all(., "\\([^()]+\\)") %>%
  unlist(.) %>%
  substring(., 2, nchar(.)-1)
  

time_labels <- c("start", "end", "dT")
time_val <- numeric(3)
names(time_val) <- time_labels

for (i in 1: length(time_labels)){
  time_val[i] <- which(grepl(time_labels[i], aaa, fixed = TRUE) == TRUE) %>% 
    aaa[.] %>% 
    strsplit(., " ") %>%
    unlist(.) %>%
    .[2] %>%
    as.numeric(.)
}

time_per <- unique(c(seq(time_val["start"], time_val["end"], by = time_val["dT"]),time_val["end"])) %>%  #+1 if needed
  #seq(time_val["start"], time_val["end"], by = time_val["dT"]) %>% 
  cut(., ., include.lowest = TRUE, right = FALSE, ordered_result = TRUE) %>%
  levels(.)

### Import the output.txt data ###########################################
###the ":" separator makes it possible to have all the data needed for the stacked bar chart in the first column

output <-read.csv(path, header = FALSE, sep = ":", quote = "\"",
                  dec = ".", na.strings = "NA", stringsAsFactors = FALSE, encoding = "UTF-8")

bag_words<- grepl("sum_t P", output[,1]) %>%
  which(.) %>%
  output[.,2] %>%
  str_remove_all(., "  ") %>%
  str_remove_all(., "\\s*\\([^\\)]+\\) ") %>%   
  ordered(., .)


### Select only the "per time" distribution, removing the "Time=" lines (already contained in T) ####################

a1 <- which(output == "===============  per time  ===============") + 1
a2 <-  which(output == "-----------------------") - 1

output1 <- output[a1:a2, 1]
output2 <- output1[!grepl('Time=', output1)]

### Split the strings selection Prob, Time and K ###############################

datatext<- matrix(0, nrow=length(output2), ncol=2)
datamat<-matrix(0, nrow=length(output2), ncol=2)

for (i in 1:length(output2)){
  datatext[i,]<-unlist(strsplit(output2[i], "  "))
  datamat[i,]<- unlist(strsplit(datatext[i,2], "[[:punct:]]"))[c(2,4)]
}

nlevK <- nlevels(as.factor(datamat[, 2]))
nlevTime <- nlevels(as.factor(datamat[, 1]))

data <- data.frame("Prob" = as.numeric(datatext[,1]), "Time" = as.numeric(datamat[, 1]), 
                   "K" = as.numeric(datamat[, 2]), "Time_periods" = rep(time_per, each = nlevK),
                   "K_bag" = rep(bag_words, times = nlevTime))
# You can check that for each time the sum of Prob is equal to 1 by writing aggregate(data$Prob, by=list(data$Time), FUN=sum)

#print(data)
#pyt_col <- c("#D8BFD8", "#4682B4", "#FF7F50", "#008080", "yellow")

### Stacked bar chart #############################
stackedplot <- ggplot() +
  theme_linedraw() +
  ggtitle(paste("Model sense distribution -", targetword)) +
  theme(plot.title = element_text(lineheight=.8, face="bold", hjust = 0.5), legend.position="bottom", legend.direction="vertical") +
  labs(x = "Time", fill="Senses", y = "Sense distribution") +
  scale_y_continuous(breaks = seq(0, 1, by = 0.2)) + 
  scale_fill_brewer(palette="Set2")

if(max(data$Time) > 10) {
  stackedplot <- stackedplot + 
    geom_bar(aes(y = Prob, x = ordered(data$Time_periods, levels = time_per), fill = K_bag), colour = "grey40", size = 0.05,
             data = data, stat="identity", show.legend = TRUE) +  
    coord_fixed(ratio = max(data$Time)) #+
    #scale_fill_manual(values=pyt_col)
} else {
  stackedplot <- stackedplot + 
    geom_bar(aes(y = Prob, x = ordered(data$Time_periods, levels = time_per), fill = K_bag), colour = "grey40", size = 0.05,
             data = data, stat="identity", show.legend = TRUE) #+ 
  # scale_fill_manual(values=pyt_col)
  }

### Save the output ###############################
ggsave(titleplot, stackedplot, width = 10, height = 10, dpi = 150, units = "in")
