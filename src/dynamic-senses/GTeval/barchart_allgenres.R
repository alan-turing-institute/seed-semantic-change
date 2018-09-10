### Use this if you have 10 genres
### Usage: Rscript barchart.R <path-to-your-output.dat-file> <path-where-to-save-plot> <missing-genre-code>
### Example: Rscript barchart.R output/59339/output.dat 59339/plotname.png "5"
### This plots the output.dat from folder 59339 in the png file plotname for all the genres except 5. If you
### want to plot all the genres do not specify any missing genre.

args <- commandArgs(trailingOnly = TRUE)
path <- as.character(args[1])
titleplot <- as.character(args[2])
#missing_genre <-  as.numeric(args[3])
missing_genre <- as.numeric(unlist(strsplit(args[3],",")))   ### input the genres as "1,2,3,4"


library(ggplot2)
library(magrittr)
library(stringr)
#library(scater)
library(cowplot)

### Import the output.txt data ###########################################
### take start_time, end_time, dT ########################################

#path <- "GTeval/output_dyn_cp.dat" 

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

time_per <-   unique(c(seq(time_val["start"], time_val["end"], by = time_val["dT"]),time_val["end"])) %>%  #time_val["end"]+1 if times are not OK
  cut(., ., include.lowest = TRUE, right = FALSE, ordered_result = TRUE) %>%
  levels(.)

### Import the output.txt data ###########################################
###the ":" separator makes it possible to have all the data needed for the stacked bar chart in the first column

output <-read.csv(path, header = FALSE, sep = ":", quote = "\"",
                  dec = ".", na.strings = "NA", stringsAsFactors = FALSE, encoding = "UTF-8")




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


bag_words<- grepl("sum_t P", output[,1]) %>%
  which(.) %>%
  output[.,2] %>%
  .[1:nlevK] %>%
  str_remove_all(., "  ") %>%
  str_remove_all(., "\\s*\\([^\\)]+\\) ") %>%   
  ordered(., .)


data <- data.frame("Prob" = as.numeric(datatext[,1]), "Time" = as.numeric(datamat[, 1]), 
                   "K" = as.numeric(datamat[, 2]), "Time_periods" = rep(time_per, each = nlevK*10),
                   "K_bag" = rep(bag_words, times = nlevTime*10), "Genre" = rep(0:9, each=nlevK, times = nlevTime))

data$Prob <- ifelse(data$Genre %in% missing_genre, NA, data$Prob)

# You can check that for each time the sum of Prob is equal to 1 by writing aggregate(data$Prob, by=list(data$Time), FUN=sum)

#print(data)
#pyt_col <- c("#D8BFD8", "#4682B4", "#FF7F50", "#008080", "yellow")

### Stacked bar chart #############################

plotlist <- rep(list(NA), 10)

for(gen in 0:9){
  
  stackedplot <- ggplot() +
    theme_linedraw() +
    #ggtitle(paste("Model sense distribution -", targetword, "- genre", gen)) +
    theme(plot.title = element_text(lineheight=.8, face="bold", hjust = 0.5), 
          legend.position="bottom", legend.direction="vertical",
          legend.text = element_text(size = 20)) + 
    #labs(x = "Time", fill="Senses", y = "Sense distribution") +
    labs(x = NULL, fill="Senses", y = NULL) +
    scale_y_continuous(breaks = seq(0, 1, by = 0.2)) + 
    scale_fill_brewer(palette="Set2")
  
  if(max(data$Time) > 15) {
    stackedplot <- stackedplot + 
      geom_bar(aes(y = Prob, x = ordered(Time_periods, levels = time_per), fill = K_bag), colour = "grey40", size = 0.05,
               data = subset(data, Genre==gen), stat="identity", show.legend = TRUE) + 
      #scale_y_continuous(breaks = seq(0, 1, by = 0.2)) + 
      coord_fixed(ratio = max(data$Time)) #+
    #scale_fill_manual(values=pyt_col)
  } else {
    stackedplot <- stackedplot + 
      geom_bar(aes(y = Prob, x = ordered(Time_periods, levels = time_per), fill = K_bag), colour = "grey40", size = 0.05,
               data = subset(data, Genre==gen), stat="identity", show.legend = TRUE)
    #  scale_y_continuous(breaks = seq(0, 1, by = 0.2)) 
    # scale_fill_manual(values=pyt_col)
  }
  
  if(gen == 0) legend_greek <- get_legend(stackedplot)
  
 plotlist[[gen + 1]] <- stackedplot +  theme(legend.position="none")
}

allplots <- plot_grid(plotlist = plotlist, ncol = 2, labels = 0:9, label_y = 1, label_x = 0.03, vjust = 0.95)
title <- ggdraw() + draw_label(paste("Model sense distribution -", targetword), fontface='bold')
#legend_greek <- get_legend(plotlist[[1]])




### Save the output ###############################

#titleplot <-"GTeval/multiplot_dynamis.png"
ggsave(titleplot, 
       plot_grid(title, allplots, legend_greek, ncol=1, rel_heights=c(0.04, 1, 0.15)),
       width = 15, height = 11.69, dpi = 150, units = "in")
