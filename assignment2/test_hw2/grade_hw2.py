## CS 458/558
## Fall 2015
## author: Kun Ren
## email: kun.ren@yale.edu

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
    if os.path.exists(os.path.join (path, "hw2.R")):
        return R_FOUND
    elif os.path.exists (os.path.join (path, "hw2.py")):
        return PYTHON_FOUND
    debug (isDebug, "\tCan not find hw2.py or hw2.R, please indicates the right path of your program")
    return OTHER_ERROR

# get the result from the Python code
def get_result (command, timeout = 20, isDebug = True, code_type = PYTHON_FOUND):
    # run the Python code in the shell
    # I use "####" as the special mark to split the output of hw0.py and the function call I invoke
    if code_type == PYTHON_FOUND:
        sentences1 = "opt1 = hw2.option(\"OH\", 40000000, 2, 12, .05, True, 6500,10000, 1000);"
        sentences2 = "opt2 = hw2.option(\"SC\", 20000000, 2, 10, .05, True, 4000,10000, 500);"
        sentences3 = "opts = [opt1, opt2];"
        sentences4 = "s1 = [\"stockholders\", \"unions\", \"OH\", \"SC\"];"
        p_command = "python -c 'import hw2; print \"####\"; "+ sentences1+ sentences2 + sentences3+sentences4+" print hw2." + command + "'"
    else:
        sentences1 = "opt1 <- option$new(\"OH\",40000000, 2, 12, .05, TRUE, 6500, 10000, 1000);"
        sentences2 = "opt2 <- option$new(\"SC\",20000000, 2, 10, .05, FALSE, 4000, 10000, 500);"
        sentences3 = "opts <- list(opt1, opt2);"
        sentences4 = "s1 <- list(\"stockholders\", \"unions\", \"OH\", \"SC\");"
        p_command = "Rscript --default-packages=methods -e 'source(\"hw2.R\"); print (\"####\"); " + sentences1 + sentences2 + sentences3 + sentences4+" print (" + command + ")'"
        
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
    p_result = ""
    for word in p_list[index + 1:] :
        pword = pre_process_word (word)
        p_result += pword

    return (CORRECT, p_result)

def grade_program (isDebug = True, code_type = PYTHON_FOUND):
    
    passed_cases = 0
    if (code_type == PYTHON_FOUND):
        (errno, result) = get_result ("npv(opt1)", isDebug = isDebug, code_type = code_type)
        if errno == CORRECT:
            try:
                if float(result) >= 256973122 - 5 and float(result) <= 256973122 + 5:
                    passed_cases += 1
                    debug (isDebug, ">> npv(opt1) function pass")
                else:
                    debug (isDebug, "\tyour program print " + result)            
                    debug (isDebug, "\npv(optOH) function print the wrong result !")            
                    debug (isDebug, ">> npv(optOH) function is not correct!")   
            except ValueError:
                debug (isDebug, "\tyour program print " + result)
                debug (isDebug, "\npv(optSC) function should print a floating number!")            
                debug (isDebug, ">> npv() function is not correct!")    
                
        (errno, result) = get_result ("npv(opt2)", isDebug = isDebug, code_type = code_type)
        if errno == CORRECT:
            try:
                if float(result) >= 192449578 - 5 and float(result) <= 192449578 + 5:
                    passed_cases += 1
                    debug (isDebug, ">> npv(optSC) function pass")
                else:
                    debug (isDebug, "\tyour program print " + result)            
                    debug (isDebug, "\npv(optSC) function print the wrong result !")            
                    debug (isDebug, ">> decide() function is not correct!")   
            except ValueError:
                debug (isDebug, "\tyour program print " + result)
                debug (isDebug, "\npv() function should print a floating number!")            
                debug (isDebug, ">> npv() function is not correct!")       
        else:
            debug (isDebug, ">> decide function is not correct!")
            
        (errno, result) = get_result ("decide(opts)", isDebug = isDebug, code_type = code_type)
        if errno == CORRECT:
            if result == "optionlocationohcost40000000":
                passed_cases += 1
                debug (isDebug, ">> decide function pass")
            else:
                debug (isDebug, "\tyour program print " + result)                     
                debug (isDebug, ">> decide() function is not correct!")            
        else:
            debug (isDebug, ">> decide function is not correct!")
        
        (errno, result) = get_result ("sensitivity(opts)", isDebug = isDebug, code_type = code_type)
        if errno == CORRECT:
            if result.startswith("option"):
                passed_cases += 1
                debug (isDebug, ">> sensitivity function pass")
            else:
                debug (isDebug, "\tyour program print " + result)                     
                debug (isDebug, ">> sensitivity() function is not correct!")            
        else:
            debug (isDebug, ">> sensitivity function is not correct!")
        
        (errno, result) = get_result ("explain(opts, s1)", isDebug = isDebug, code_type = code_type)
        if errno == CORRECT:
            if result.startswith("decision"):
                passed_cases += 1
                debug (isDebug, ">> explain function pass")
            else:
                debug (isDebug, "\tyour program print " + result)                     
                debug (isDebug, ">> explain() function is not correct!")            
        else:
            debug (isDebug, ">> explain function is not correct!")
     
    elif (code_type == R_FOUND):
        (errno, result) = get_result ("npv(opt1)", isDebug = isDebug, code_type = code_type)
        if errno == CORRECT:
            try:
                if float(result) >= 256973122 - 5 and float(result) <= 256973122 + 5:
                    passed_cases += 1
                    debug (isDebug, ">> npv(optOH) function pass")
                else:
                    debug (isDebug, "\tyour program print " + result)            
                    debug (isDebug, "\npv(optOH) function print the wrong result !")            
                    debug (isDebug, ">> npv(optOH) function is not correct!")   
            except ValueError:
                debug (isDebug, "\tyour program print " + result)
                debug (isDebug, "\npv(optSC) function should print a floating number!")            
                debug (isDebug, ">> npv() function is not correct!")    
                
        (errno, result) = get_result ("npv(opt2)", isDebug = isDebug, code_type = code_type)
        if errno == CORRECT:
            try:
                if float(result) >= 192449578 - 5 and float(result) <= 192449578 + 5:
                    passed_cases += 1
                    debug (isDebug, ">> npv(optSC) function pass")
                else:
                    debug (isDebug, "\tyour program print " + result)            
                    debug (isDebug, "\npv(optSC) function print the wrong result !")            
                    debug (isDebug, ">> decide() function is not correct!")   
            except ValueError:
                debug (isDebug, "\tyour program print " + result)
                debug (isDebug, "\npv() function should print a floating number!")            
                debug (isDebug, ">> npv() function is not correct!")       
        else:
            debug (isDebug, ">> decide function is not correct!")
            
        (errno, result) = get_result ("decide(opts)", isDebug = isDebug, code_type = code_type)
        if errno == CORRECT:
            if result.startswith("thisisanoptionlocationohcost4e07"):
                passed_cases += 1
                debug (isDebug, ">> decide function pass")
            else:
                debug (isDebug, "\tyour program print " + result)                     
                debug (isDebug, ">> decide() function is not correct!")            
        else:
            debug (isDebug, ">> decide function is not correct!")
        
        (errno, result) = get_result ("sensitivity(opts)", isDebug = isDebug, code_type = code_type)
        if errno == CORRECT:
            if result.startswith("thisisanoption"):
                passed_cases += 1
                debug (isDebug, ">> sensitivity function pass")
            else:
                debug (isDebug, "\tyour program print " + result)                     
                debug (isDebug, ">> sensitivity() function is not correct!")            
        else:
            debug (isDebug, ">> sensitivity function is not correct!")
        
        (errno, result) = get_result ("explain(opts, s1)", isDebug = isDebug, code_type = code_type)
        if errno == CORRECT:
            if result.startswith("thisisadecision"):
                passed_cases += 1
                debug (isDebug, ">> explain function pass")
            else:
                debug (isDebug, "\tyour program print " + result)                     
                debug (isDebug, ">> explain() function is not correct!")            
        else:
            debug (isDebug, ">> explain function is not correct!")       
  
    debug (isDebug, ">> " + str(passed_cases) + "/5 cases passed!")
    return

def grade_hw2 (path = ".", isDebug = True):
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

grade_hw2()

