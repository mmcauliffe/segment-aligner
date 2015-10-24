library(ggplot2)
data <- read.csv('~/Documents/Data/temp/segalign/output.txt')

ggplot(data,aes(x = distance)) + geom_histogram()
