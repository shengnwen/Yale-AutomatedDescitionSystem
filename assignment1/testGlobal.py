__author__ = 'shengwen'
gl = 5

def f1():
    global gl
    gl = 42
def f2():
    print gl

f1()
f2()