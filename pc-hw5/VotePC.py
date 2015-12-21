from Tkinter import Tk, Frame, BOTH

class Person:
    # the person has a set of preferences,
    # a collection of relatinships, and
    # possibly a history of prior decisions.
    def __init__(self, name):
        self.name = name
        self.relation_dict = {}#"father": person1
        self.history_purchase = [] # "A":score=3
        self.operating_system_prefer = [] # compatible with smartphone
        self.software_prefer = {} # pages in mac# "Page": [mac]
        self.service_year = 3 # 3 year
        self. discount = 0
    def __str__(self):
        pass

class PC:
    def __init__(self):
        pass
    def __str__(self):
        pass

def whichpc(person):
    # price, memory size, screen size, disk space, etc.
    #user classification system that accounts for
    # why a person actually needs a computer.
    pass

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")

        self.parent = parent

        self.initUI()


    def initUI(self):

        self.parent.title("Simple")
        self.pack(fill=BOTH, expand=1)

def main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()
