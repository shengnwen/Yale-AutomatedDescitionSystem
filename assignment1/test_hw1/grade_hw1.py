## CS 458/558
## Fall 2015
## author: Ronghui Gu
## email: ronghui.gu@yale.edu

# This is a sample test script

import os
import re
import subprocess
import shlex
import time

# pre-process the word, remove all the non-alphanumeric characters
def pre_process_word (word):
    return re.sub ("[^a-zA-Z0-9_\.]", "", word.lower ())

# debug function
def debug (flag = True, output = ""):
    if flag :
        print output

CORRECT = 0
PYTHON_FOUND = 1
R_FOUND = 2
TIMEOUT_ERROR = 3
FORMAT_ERROR = 4
OTHER_ERROR = 5

# test whether all the required files are existing
def test_file_exists (path, isDebug):
    if os.path.exists (os.path.join (path, "hw1.py")):
        return PYTHON_FOUND
    elif os.path.exists(os.path.join (path, "hw1.R")):
        return R_FOUND
    debug (isDebug, "\tCan not find hw1.py or hw1.R, please indicates the right path of your program")
    return OTHER_ERROR

# get the result from the Python code
def get_result (command, timeout = 20, isDebug = True, code_type = PYTHON_FOUND):
    # run the Python code in the shell
    # I use "####" as the special mark to split the output of hw0.py and the function call I invoke
    if code_type == PYTHON_FOUND:
        p_command = "python -c 'import hw1; print \"####\"; print hw1." + command + "'"
    else:
        p_command = "Rscript -e 'source(\"hw1.R\"); print (\"####\"); print (" + command + ")'"
        
    process = subprocess.Popen(shlex.split (p_command), stdout=subprocess.PIPE)

    # get the timeout
    wait = timeout
    while wait > 0 and (process.poll() is None):
        time.sleep(1)
        wait -= 1

    if wait <= 0:
        process.kill()
        debug (isDebug, "\ttime out!")
        debug (isDebug, "\tthe program should finish in " + str(timeout) + " seconds")
        return (TIMEOUT_ERROR, "")
        
    p_output = process.communicate()[0].split("\n")
    p_list = [];

    for word in p_output:
        # remove the line number like "[1]"
        # split the word with "\"", such that it can deal with the case that you failed to print a word per line
        p_list += re.sub ("\[\d+\]", "", word.lower ()).split ("\"")

    # get the index of "####"
    if "####" in p_list :
        index = p_list.index ("####")
    else:
        debug (isDebug, "\tcan not find #### in the output")
        return (FORMAT_ERROR, "")
    for word in p_list[index + 1:] :
        pword = pre_process_word (word)
        if pword != "":
            return (CORRECT, pword)

    #debug (isDebug, "\tcan not find the required output")
    return (CORRECT, "")

def grade_program (isDebug = True, code_type = PYTHON_FOUND):
    
    passed_cases = 0
    
    (errno, result) = get_result ("hitme(12,1)", isDebug = isDebug, code_type = code_type)
    if errno == CORRECT:
        if result == "true" or result == "false":
            passed_cases += 1
            debug (isDebug, ">> hitme() function pass")
        else:
            debug (isDebug, "\tyour program print " + result)            
            debug (isDebug, "\thitme() function should print true or false!")            
            debug (isDebug, ">> hitme() function is not correct!")            
    else:
        debug (isDebug, ">> hitme() function is not correct!")

    (errno, result) = get_result ("play(3)", timeout = 60, isDebug = isDebug, code_type = code_type)
    if errno == CORRECT:
        try:
            float(result)
            passed_cases += 1
            debug (isDebug, ">> play() function pass")
        except ValueError:
            debug (isDebug, "\tyour program print " + result)
            debug (isDebug, "\tplay() function should print a floating number!")            
            debug (isDebug, ">> play() function is not correct!")            
    else:
        debug (isDebug, ">> play() function is not correct!")

    if os.path.exists ("transcript"):
        os.remove ("transcript")

    (errno, result) = get_result ("sim(3)", timeout = 100, isDebug = isDebug, code_type = code_type)
    if errno == CORRECT:
        if os.path.exists ("transcript"):
            passed_cases += 1
            debug (isDebug, ">> sim() function pass")
        else:
            debug (isDebug, "\tsim() function should generate the transcript file!")            
            debug (isDebug, ">> sim() function is not correct!")            
    else:
        debug (isDebug, ">> sim() function is not correct!")

    debug (isDebug, ">> " + str(passed_cases) + "/3 cases passed!")
    return

def grade_hw1 (path = ".", isDebug = True):
    # test whether all the required files are existing
    exists_file = test_file_exists (path, isDebug)
    if exists_file == OTHER_ERROR:
        debug (isDebug, ">> the test is uncomplete, since some files are missing")
    elif exists_file == PYTHON_FOUND:
        debug (isDebug, ">> test the Python code")
        grade_program(isDebug = isDebug, code_type = exists_file)
    elif exists_file == R_FOUND:
        debug (isDebug, ">> test the R code")
        grade_program(isDebug = isDebug, code_type = exists_file)

    return

grade_hw1()
#print grade_hw0 (total_cases = 5, path = "test", isDebug = False)
