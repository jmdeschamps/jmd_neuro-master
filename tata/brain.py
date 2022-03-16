## -*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import askopenfilenames

import random

class Vue():
    def __init__(self,parent):
        self.parent=parent
        self.root=Tk()

class Modele():
    def __init__(self,parent):
        self.parent=parent
        
class SNP():
    def __init__(self):
        self.ganglions=[]
        
class SNC():
    def __init__(self):
        self.ganglions=[]
        
class Ganglion():
    def __init__(self):
        self.neurones=[]
        
        
class Neurone():
    def __init__(self):
        self.neurites=[]
        self.dendrites=[]
class Neurite():
    def __init__(self):
        self.neurites=[]
        self.dendrites=[]
class Dendrite():
    def __init__(self):
        self.neurites=[]
        self.dendrites=[]

class Controleur():
    def __init__(self):
        self.modele=Modele(self)
        self.vue=Vue(self)
        self.vue.root.mainloop()
        
if __name__ == '__main__':
    c=Controleur()
    print("OK")