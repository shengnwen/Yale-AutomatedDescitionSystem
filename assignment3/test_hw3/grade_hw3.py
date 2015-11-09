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
import random
import sys

# pre-process the word, remove all the non-alphanumeric characters
def pre_process_word (word):
    return re.sub ("[^-a-zA-Z0-9_\.]", "", word.lower ())

# debug function
def debug (flag = True, output = ""):
    if flag :
        print output

CORRECT = 0
PYTHON_FOUND = 1
PYTHON_FOUND2 = 2
R_FOUND = 3
TIMEOUT_ERROR = 4
FORMAT_ERROR = 5
OTHER_ERROR = 6

# test whether all the required files are existing
def test_file_exists (path, isDebug):
    if os.path.exists (os.path.join (path, "hw3.py")):
        return PYTHON_FOUND
    elif os.path.exists(os.path.join (path, "hw3.R")):
        return R_FOUND
    debug (isDebug, "\tCan not find hw3.py or hw3.R, please indicates the right path of your program")
    return OTHER_ERROR

# get the result from the Python code
def get_result (command, timeout = 20, isDebug = True, code_type = PYTHON_FOUND, path = ".", netid = ""):
    # run the Python code in the shell
    # I use "####" as the special mark to split the output of hw0.py and the function call I invoke
    
    if code_type == PYTHON_FOUND:
        p_command = "python -c 'import hw3; print \"####\"; print hw3." + command + "'"
    else:
        p_command = "Rscript -e 'source(\"hw3.R\"); print (\"####\"); print (" + command + ")'"
    
    process = subprocess.Popen(shlex.split (p_command), stdout=subprocess.PIPE)
    
        # get the timeout
    wait = timeout
    while wait > 0 and (process.poll() is None):
        time.sleep(1)
        wait -= 1

        #os.chdir(os.path.abspath(oldpath))

    if wait <= 0:
        process.kill()
        debug (isDebug, "\ttime out!")
        debug (isDebug, "\tthe program should finish in " + str(timeout) + " seconds")
        return (TIMEOUT_ERROR, "")
        
    p_output = process.communicate()[0].split("\n")

    #if os.path.getsize ("error/" + netid) < 1:
    #    os.remove ("error/" + netid)

    #print p_output
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

def grade_program (isDebug = True, code_type = PYTHON_FOUND, path = ".", netid = ""):
    
    is1 = is2 = is3 = 0
    comments = ""

    command = 'backtest(ticker = "AAPL", start = "2015-05-01", end = "2015-10-23", duration = 20)'
    (errno, result) = get_result (command, isDebug = isDebug, code_type = code_type, path = path, netid = netid)
    if errno == CORRECT:
        try:
            if float (result) < -0.035 and float(result) > -0.05:
                is1 = 1
                debug (isDebug, ">> backtest() function pass")
            else:
                debug (isDebug, "\tyour program print " + result)            
                debug (isDebug, "\tbacktest() function should print the floating point near -0.04!")
                debug (isDebug, ">> backtest() function is not correct!")            
        except:
            debug (isDebug, "\tyour program print " + result)            
            debug (isDebug, "\tbacktest() function should print the floating point near -0.04!")            
            debug (isDebug, ">> backtest() function is not correct!")            
    else:
        debug (isDebug, ">> backtest() function is not correct!")

    if is1 == 0:
        comments += "backtest() function is not correct;"
    
    if code_type == PYTHON_FOUND:
        command = ('sectortest (startdates = ["2015-01-01", "2015-06-01"],'
                   + 'enddates = ["2015-05-01", "2015-10-01"], durations = [20, 50], file = "test2")')
    else:
        command = ('sectortest (startdates = list("2015-01-01", "2015-06-01"),'
                   + 'enddates = list("2015-05-01", "2015-10-01"), durations = list(20, 50), file = "test2")')
        
    (errno, result) = get_result (command, timeout = 60, isDebug = isDebug, code_type = code_type, path = path, netid = netid)
    if errno == CORRECT:
        if os.path.exists ("test2"):
            with open ("test2") as f:
                result = f.readlines()
                # for best
                res = result[0].strip().split(" ")
                if (res[1] == "XLB" and res[2] == "2015-01-01"
                    and res[3] == "2015-05-01" and res[4] == "20" and float(res[5]) > 0.05 and float(res[5]) < 0.07):
                    debug (isDebug, ">> sectortest(): best pass")
                    is2 += 1
                else:
                    debug (isDebug, ">> sectortest(): best is not correct")
                    debug (isDebug, ">> sectortest(): should write 'best XLB 2015-01-01 2015-05-01 20 0.063'")

                res = result[1].strip().split(" ")
                if (res[4] == "20" and float(res[5]) > -0.11 and float(res[5]) < -0.08):
                    debug (isDebug, ">> sectortest(): worst pass")
                    is2 += 1
                else:
                    debug (isDebug, ">> sectortest(): worst is not correct")
                    debug (isDebug, ">> sectortest(): should write 'worst XLU 2015-01-01 2015-05-01 20 -0.09'")
                    debug (isDebug, ">> sectortest(): or 'worst XLI 2015-06-01 2015-10-01 20 -0.09'")

                res = result[2].strip().split(" ")
                if (res[1] == "2015-01-01"
                    and res[2] == "2015-05-01" and float(res[3]) > -0.019 and float(res[3]) < -0.014):
                    debug (isDebug, ">> sectortest(): avg-period pass")
                    is2 += 1
                else:
                    print result[2]
                    debug (isDebug, ">> sectortest(): avg-period is not correct")
                    debug (isDebug, ">> sectortest(): should write 'avg-period 2015-01-01 2015-05-01 -0.017'")
                    
                res = result[3].strip().split(" ")
                if (res[1] == "50" and float(res[2]) > -0.03 and float(res[2]) < -0.02):
                    debug (isDebug, ">> sectortest(): avg-duration pass")
                    is2 += 1
                else:
                    debug (isDebug, ">> sectortest(): avg-duration is not correct")
                    debug (isDebug, ">> sectortest(): should write 'avg-duration 50 -0.020'")
        else:
            debug (isDebug, "\tsectortest() function should generate the given file!")            
            debug (isDebug, ">> sectortest() function is not correct!")
    else:
        debug (isDebug, ">> sectortest() function is not correct!")

    if is2 == 0:
        comments += "sectortest() function is not correct;"


    command = ('realbacktest(ticker = "AAPL", start = "2014-08-01", end = "2015-10-23"'
               + ', duration = 20, commission = 2, file = "test3")')
    
    (errno, result) = get_result (command, timeout = 20, isDebug = isDebug, code_type = code_type, path = path, netid = netid)
    if errno == CORRECT:
        if os.path.exists ("test3"):
            with open ("test3") as f:
                result = f.readlines()
                # for best
                res = result[0].strip().split(" ")
                if (float(res[0]) > -0.14 and float(res[0]) < -0.12):
                    debug (isDebug, ">> realbacktest(): moving average pass")
                    is3 += 1
                else:
                    debug (isDebug, ">> realbacktest(): moving average not correct")
                    debug (isDebug, ">> realbacktest(): should write '-0.13 net return, moving average.'")

                res = result[1].strip().split(" ")
                if (float(res[0]) > 0.18 and float(res[0]) < 0.3):
                    debug (isDebug, ">> realbacktest(): buy and hold pass")
                    is3 += 1
                else:
                    debug (isDebug, ">> realbacktest(): buy and hold is not correct")
                    debug (isDebug, ">> realbacktest(): should write '0.20 buy and hold return.'")
        else:
            debug (isDebug, "\trealbacktest() function should generate the given file!")            
            debug (isDebug, ">> realbacktest() function is not correct!")
    else:
        debug (isDebug, ">> realbacktest() function is not correct!")

    if is3 == 0:
        comments += "realbacktest() function is not correct;"
        
    debug (isDebug, ">> " + str(is1 + is2 + is3) + "/7 cases passed!")
    
    return (str(is1), str(is2), str(is3), comments)


def grade_hw3 (path = ".", isDebug = True, info = []):
    # test whether all the required files are existing
    exists_file = test_file_exists (path, isDebug)
    grade = ("0", "0", "0", "some files are missing")
    if exists_file == OTHER_ERROR:
        debug (isDebug, ">> the test is uncomplete, since some files are missing")
    elif exists_file == PYTHON_FOUND or exists_file == PYTHON_FOUND2:
        debug (isDebug, ">> test the Python code")
        grade = grade_program(isDebug = isDebug, code_type = exists_file, path = path)
    elif exists_file == R_FOUND:
        debug (isDebug, ">> test the R code")
        grade = grade_program(isDebug = isDebug, code_type = exists_file, path = path)
    
    return grade

grade_hw3()
