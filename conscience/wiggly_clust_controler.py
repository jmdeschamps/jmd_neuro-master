# -*- coding: utf-8 -*-
"""
Neuro_wiggly est une simulation neuronale
PREAMBULE
ce programme est une simulation cherchant à imiter les liens entre neurones et organes.
Dans ce sens les comportements (action des entites) ne sont pas programmé au sens
courant, mais découle de l'activation des composantes neuronales.
PRINCIPES
- les neurones sont composés de dendrites (entrées) et de neurites (sorties)
- les dendrites peuvent recevoir leur stimulation d'un sens (generalement rataché à
un organe), ou d'une dendrite.
- le neurone envoie un signal aux neurites
- les neurites (les terminaux au bout des axones) transmettent leur signaux à des dendrites
ou à d'autres types d'organes (muscles, glandes, etc)
- les composantes ont des seuils à atteindre avant de transmettre un signal
- les composantes ont un durée de repos avant de pouvoir être réactiver

VERSIONS
-V_01-
Bibitte initiale
- les bibittes sont composées de système de vision binoculaire, champ de 90 degrées, 
de 20 deg vers le centre, 70 vers l'extérieur (champ central commun),
les yeux sont composé de 90 neurones (un par degré),chacun possédant un seul dendrite
stimulable, mais de 10 à 15 neurites.
- les yeux sont connectes sur les pattes et les stimulent, ce qui occasione leur contraction,
qui s'interprètent par un mouvement

30 aout 2014, jmd    _v2_01 - refactorisation de l'approche, en largeur plutot qu'en profondeur



- V3_6 et plus
Faire ganglion
    couche concentrée de neurones
        redirecteur concentrateur

Odorat
    le nez sent les choses proches
        plus important que la vision
        stimule et inhibe la vue
        stéréo
        categories d'odeurs: floral, fruite, epice, resineux, brule, putride

v3_9 - 25 juillet 2017
ajusté graphique pour yeux et nez
séparé systeme nerveux du modele



"""
#import Pyro4
import math
import random
import time
import socket
from helper import Helper as h
from fgetid import *
from wiggly_clust_modele import *
from wiggly_clust_vue import *


class Controleur():
    # classe principale du Modele dans MVC
    def __init__(self):
        self.cadre=0
        self.modele=None
        self.vue=Vue(self,None)
        #self.vue.dessinemodele(None)
        #self.initserveurpyro()
        #self.demarresession()
        self.vue.root.mainloop()
        
    # def initserveurpyro(self):
    #     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     s.connect(("gmail.com",80))
    #     monip=s.getsockname()[0]
    #     print("MON IP SERVEUR",monip)
    #     s.close()
    #     daemon = Pyro4.core.Daemon(host=monip,port=9999)
    #
    #     daemon.register(self, "controleurServeur")
    #
    #     print("Serveur Pyro actif sous le nom \'controleurServeur\'")
    #     daemon.requestLoop()
    #
    def demarresession(self):
        self.cadre=0
        # lire data du taboption
        dons=self.vue.taboptionswidgets
        #random.seed(171727)
        if dons["Random seed"].get():
            random.seed(int(dons["Random seed"].get()))
        else:
            print(dons["Random seed"])
        self.modele=Modele(self,dons["Largeur"].get(),dons["Hauteur"].get(),
                           dons["Nbre Bouffe"].get(),dons["Nbre Poison"].get(),dons["Nbre Bibitte"].get(),)
        self.vue.setTailleCanevas(int(dons["Largeur"].get()),int(dons["Hauteur"].get()))
        self.boucleOn=0
        self.debugOn=0
        self.tour=0
        self.vue.dessinemodele(self.modele)
        self.metabolise()
        
    def getBibitte(self,n):
        for i in self.modele.bibittes:
            if i.id==n:
                return i
    def metabolise(self):
        self.cadre=self.cadre+1
        if self.debugOn:
            n=1+1 # excuse pour breakpoint
        for i in self.modele.bibittes:
            i.metaboliser()  
        for i in self.modele.bibittes2:
            i.metaboliser()  
        t1=time.time()
        self.vue.updateBibittes(self.cadre,self.modele.bibittes) # changer pour envoyer bibittes seulement
        self.vue.updateBibittes2(self.cadre,self.modele.bibittes2) # changer pour envoyer bibittes seulement
        t2=time.time()
        #print(t2-t1)
        #self.vue.dessineBibittes(self.modele.bibittes) # changer pour envoyer bibittes seyulement
        if self.boucleOn:
            self.prochaineAction=self.vue.root.after(10,self.metabolise)
    """
    def tournebibitte(self):
        for i in self.modele.bibittes:
            if i.panic==0:
                i.angle=i.angle+10
                if i.angle>360:
                    i.angle=i.angle-360
                    print("tour",self.tour)
                i.miseajourposition()
            i.metaboliser()  
        self.vue.dessineBibittes(self.modele.bibittes)
        if self.boucleOn:
            self.tour=self.tour+1
            self.prochaineAction=self.vue.root.after(1,self.tournebibitte)
    """
        
if __name__ == '__main__':
    controleur=Controleur()