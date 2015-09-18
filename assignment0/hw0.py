## CS 458/558
## Fall 2015
## hw0.py

# This is a warmup exercise that really has little to do with decision making.
# Rather, it is an opportunity to begin to learn R and Python.
# You will implement the same functions in both languages.

## Function 1: palindrome
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

## Use the following function signature.  Replace "pass" with your code.


# either 1. print all the value to make it the same with the example output
# or 2. return a list of all palindrome objects
def isPalindrome(word):
    start = 0
    end = len(word) - 1
    while (start < end):
        while start < end and not word[start].isalnum():
            start = start + 1
        while start < end and not word[end].isalnum():
            end = end - 1
        if word[start].lower() != word[end].lower():
            return False
        start = start + 1
        end = end - 1
    return True


def isStartWith(word, letter):
    for i in word:
        if i.isalnum():
            if i == letter:
                return True;
            else:
                return False;
        else:
            continue;
    return False;


def palindrome(filename="/usr/share/dict/words", letter="all"):
    # palindromes = []
    with open(filename) as f:
        words = f.read().splitlines()  # to get rid of all the '\n' print out
    if letter.lower() == "all":
        for word in words:
            if isPalindrome(word):
                print(word)
    else:
        for word in words:
            if isStartWith(word.lower(), letter.lower()) and isPalindrome(word):
                print(word)
            # return palindromes


# palindrome()

# palindrome(letter = "b")


# >>> palindrome(letter = "b")
# B
# b
# Bab
# bab
# B/B
# BB
# bb
# BBB
# Beeb
# Bib
# bib
# Bob
# bob
# boob
# Bub
# bub



## Function 2: anagram
#
# write a function anagram which reads an ascii file comprising one word
# per line and returns all the largest set of words which are anagrams.  
# The default file is the standard UNIX online dictionary: /usr/share/dict/words
# 
# There is another optional argument which is a single word.  
# In that case, the function returns all anagrams for that word 

# Example output
# >>> anagram()
# ['alerts', 'alters', 'artels', 'estral', 'laster', 'lastre', 'rastle', 'ratels', 'relast', 'resalt', 'salter', 'slater', 'staler', 'stelar', 'talers']
# 
# >>> anagram(target = 'male')
# ['alem', 'alme', 'amel', 'lame', 'leam', 'male', 'meal', 'mela']

## Use the following function signature.  Replace "pass" with your code.

from collections import defaultdict


# either Using python map type 'dict'
# or directly using python sorted trick
def isAnagram(str1, str2):
    if len(str1) != len(str2):
        return False
    if ''.join(sorted(str1)) == ''.join(sorted(str2)):
        return True
    else:
        return False


def anagram(filename="/usr/share/dict/words", target=False):
    with open(filename) as f:
        words = f.read().splitlines()
    diction = defaultdict(list)
    for word in words:
        if target:
            if not isAnagram(target, word):
                continue
        diction[tuple(sorted(word))].append(word)
    if target:
		for i in diction[tuple(sorted(target))]:
			print(i)
    else:
        max = []
        for v in diction.values():
            if len(v) > len(max):
                max = v
        for i in max:
			print(i);

# anagram(filename = "testwords", target="male")
## Bonus question (no credit)
## An auto-antonym is a word that has two meanings that are opposites.
## For example, "dust" can mean to remove dust (I am dusting under the bed)
## and also "dust" can mean to add dust (I am dusting the cake with powdered sugar)
##
## How would you use a computer to come up with a list of auto-antonyms?
## Hint: there is more than one answer.
# fist answer

# second answer
