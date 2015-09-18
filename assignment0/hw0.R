## CS 458/558
## Fall 2015
## hw0.R

# This is a warmup exercise that really has little to do with decision making.
# Rather, it is an opportunity to begin to learn R and Python.
# You will implement the same functions in both languages.

## Function 1: palindrom
# a palindrome is a string or word or number or phrase that is the same backward
# as forward.  Examples:

# radar
# Bob
# 10101
# A man, a plan, a canal: Panama!
# Madam, I'm Adam

# write a function palindrome which reads an ascii file comprising one word
# per line and returns all the palindromes.  
# The default file is the standard UNIX online dictionary: /usr/share/dict/words
# There is another optional argument of a single letter, in which case the
# program returns only palindromes which start with that letter.


## Use the following function signature. 
# function to detect if begin with character
isStartWith <- function(line, l) {
  chars <- strsplit(tolower(line),"")[[1]]
  for (char in chars) {
    if (any(char == letters)) {
      if (char == l) {
        return (TRUE);
      } else {
        return (FALSE);
      }
    }
  }
  return(FALSE)
}

isPalindrome <- function(line) {
  # compare first character with last character, get rid of non-alpha ones
  # split str in  to each character
  line <- gsub("[^A-Za-z0-9]", "", line)
  chars <- strsplit(tolower(line),"")[[1]]
  start <- 1
  end <- length(chars)
  #numbers = c("0","1","2","3","4","5","6","7","8","9")
  #validChar = c(numbers, letters)
  while(start < end) {
    #while(start < end && !any(chars[start] == validChar) ) {
    #  start <- start + 1
    #}
    #while(start < end && ! any(chars[end] == validChar)) {
    #  end <- end - 1
    #}
    if (chars[start] != chars[end]) {
      return(FALSE)
    }
    start <- start + 1
    end <- end - 1
  }
  return(TRUE)
}

palindrome <- function(filename = "/usr/share/dict/words", letter = "all"){
  # put your code here
  lines <- readLines(filename)
  #pattern = paste("^", tolower(letter), sep="")
  for (line in lines) {
    if(letter == "all") {
      if (isPalindrome(line)) {
        write(line,"")
      }
    } else {
      #if (grepl(pattern, tolower(line)) && isPalindrome(line)) {
      if (isStartWith(tolower(line), tolower(letter)) && isPalindrome(line)) {
        write(line,"")
      }
    }
  }
}
#palindrome()
## Function 2: anagram
##
# write a function anagram which reads an ascii file comprising one word
# per line and returns all the largest set of words which are anagrams.  
# The default file is the standard UNIX online dictionary: /usr/share/dict/words
# (During development, you might want to use a smaller dictionary.)
# 
# There is another optional argument which is a single word.  
# In that case, the function returns all anagrams for that word 

# Example output
# > anagram()
# [1] "alerts" "alters" "artels" "estral" "laster" "lastre" "rastle" "ratels" "relast" "resalt"
# [11] "salter" "slater" "staler" "stelar" "talers"
# 
# > anagram(target = 'male')
# [1] "alem" "alme" "amel" "lame" "leam" "meal" "mela"

## Use the following function signature.
isAnagram <- function (str1, str2) {
  if (nchar(str1) != nchar(str2)) {
    return(FALSE)
  }
  chars1 <- strsplit(str1,"")[[1]]
  chars2 <- strsplit(str2,"")[[1]]
  chars1 <- sort(tolower(chars1))
  chars2 <- sort(tolower(chars2))
  return(all(chars1 == chars2))
}

anagram <- function(filename = "/usr/share/dict/words", target = FALSE){
  # put your code here
  lines <- readLines(filename)
  res <- c()
  dict <- list()
  if (target != FALSE) {
    for (line in lines) {
      if (isAnagram(line, target)) {
        res <- c(res, line)
      }
    }
  } else {
    i = 0
    for (line in lines) {
      chars <- strsplit(tolower(line),"")[[1]]
      key <- paste(sort(chars), collapse="")
      dict[[key]] <- c(dict[[key]], line)
      if (length(dict[[key]]) > length(res)) {
        res <- dict[[key]]
      }
    }
  }
  return(res)
}


## Questions 1:"al l" is or not begin with "all"

## Bonus question (no credit)
## An auto-antonym is a word that has two meanings that are opposites.
## For example, "dust" can mean to remove dust (I am dusting under the bed)
## and also "dust" can mean to add dust (I am dusting the cake with powdered sugar)
##
## How would you use a computer to come up with a list of auto-antonyms?
## Hint: there is more than one answer.


# Answer:
