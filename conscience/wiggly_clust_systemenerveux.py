## -*- coding: utf-8 -*-
"""
v3_9
addition de ce module retiré de l'ancien module wiggly_clust_modele
"""

import math
import random
import time
from helper import Helper as h

from fgetid import *
# 30 aout 2014, jmd    _v2_01 - refactorisation de l'approche, en largeur plutot qu'en profondeur

seuilmin=2
seuilpatte=6
           
class Neurone():
    def __init__(self,parent,dendrites=1,neurites=1,seuil=10):
        self.id=getId()
        self.parent=parent
        self.dendrites=[]
        self.neurites=[]
        self.niveau=0
        self.seuil=seuil #min
        self.creeDendrites(dendrites)
        self.creeNeurites(neurites)
        self.nbrdendrite=len(self.dendrites)
        self.nbrneurite=len(self.neurites)
        
    def creeDendrites(self,n):
        for i in range(n):
            self.dendrites.append(Dendrite(self))
            
    def creeNeurites(self,n):
        for i in range(n):
            self.neurites.append(Neurite(self))
            
    def stimuler(self):
        self.niveau=self.niveau+1
        self.testseuil()
        
    def testseuil(self):
        if self.niveau>self.seuil:
            self.niveau=0
            self.stimulerNeurites()
            
    def stimulerNeurites(self):
        for i in self.neurites:
            i.stimuler()
        
class Neurite():
    def __init__(self,parent):
        self.id=getId()
        self.parent=parent
        self.dendrite=None
        self.niveau=0
        self.seuil=seuilmin #1 #3 #random.randrange(8)+2
        
    def stimuler(self):
        self.niveau=self.niveau+1
        if self.niveau>self.seuil:
            if self.dendrite:
                self.dendrite.stimuler() # affecte le dendrite connecte
                self.niveau=0
                
class Dendrite():
    def __init__(self,parent):
        self.id=getId()
        self.parent=parent
        self.neurite=None
        self.niveau=0
        self.seuil=seuilmin #1 
        
    def stimuler(self):
        self.niveau=self.niveau+1
        
    def testseuil(self):
        if self.niveau>self.seuil:
            self.niveau=0
            #print("STIMULE NEURONE")
            self.parent.stimuler() # averti le neurone parent de se stimuler

class Ganglion():
    def __init__(self,nb=0):
        print("Je suis un GANGLION")

if __name__ == '__main__':
    mod=Modele("", 1000,800)
    print(mod)