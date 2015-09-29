## CS 458/558
## Fall 2015
## author: Ronghui Gu
## email: ronghui.gu@yale.edu

# This is a sample program

# read the transcript file, and print true or false
hitme <- function (playerhand = 12, dealerfacecard = 1) {
     return (TRUE)
}

# print a float number
play <- function (trials = 5){
     return (0.89)
}

# generate the transcript file
sim <- function (trials = 5){
    mat <- matrix(0.3, nrow = 21, ncol = 10)
    write.table(mat, file="transcript", row.names=FALSE, col.names=FALSE)
}