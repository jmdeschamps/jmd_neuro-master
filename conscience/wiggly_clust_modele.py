# -*- coding: utf-8 -*-
"""
Neuro_wiggly est une simulation neuronale
(voir détail dans wiggly_clust_controler)
"""

import math
import random
import time

from helper import Helper as h
from fgetid import *

from wiggly_clust_systemenerveux import *

class Bibitte2():
    def __init__(self,parent,longueur,largeur,x,y,a):
        self.parent=parent
        self.id=getId()
        self.longueur=longueur
        self.largeur=largeur
        #ajouter taille relative et positionnement oeil, pattes estomac etc
        self.angle=a
        self.angleinchange=0
        self.vieilleangle=a
        self.x=x
        self.y=y
        self.ganglions=Ganglion()
        self.miseajourposition()
        
    def metaboliser(self):
        print("B" ,self.id,"metabolise")
        
    def miseajourposition(self):
        self.calcMensurations()
        self.calcPosition()
        
    def calcMensurations(self):
        b=self
        long=b.longueur
        large=b.largeur
        self.longdemi=long/2
        self.longquart=long/4
        self.longhuit=long/8
        self.largedemi=large/2
        self.largequart=large/4
        self.largehuit=large/8
        self.largeseize=large/16
        self.longdouble=long*2
        self.longquadruple=long*4
        
    def calcPosition(self):
        b=self
        x=b.x
        y=b.y
        angle=b.angle
        
        
        self.xbeccentre,self.ybeccentre=h.getAngledPoint(math.radians(angle),self.longdemi,x,y)
        
class Bibitte():
    def __init__(self,parent,longueur,largeur,x,y,a):
        self.parent=parent
        self.id=getId()
        self.longueur=longueur
        self.largeur=largeur
        #ajouter taille relative et positionnement oeil, pattes estomac etc
        self.angle=a
        self.angleinchange=0
        self.vieilleangle=a
        self.x=x
        self.y=y
        self.ganglions=Ganglion()
        self.miseajourposition()
        self.yeux=[Oeil(self,"gauche",-70,20),Oeil(self,"droit",-20,70)]
        self.pattes={"phg":Patte(self,"phg"),
                     "phd":Patte(self,"phd"),
                     "pbg":Patte(self,"pbg"),
                     "pbd":Patte(self,"pbd")}
        
        self.bouche=Bouche(self)
        self.nez=Narine(self)
        self.estomac=Estomac(self)
        self.intestin=Intestin(self)
        self.anus=Anus(self)
        self.arteres=[]
        self.paniccooldown=random.randrange(5)+15
        self.panic=self.paniccooldown
        self.connecteNeuroYeux()
        self.nbrneuroneyeux=self.yeux[0].nbrneurone+self.yeux[1].nbrneurone
        self.nbrneuronepattes=self.pattes["phg"].nbrneurone+self.pattes["pbg"].nbrneurone+self.pattes["phd"].nbrneurone+self.pattes["pbd"].nbrneurone
        self.nbrneurone=self.nbrneuroneyeux+self.nbrneuronepattes
        
        self.nbrneuriteyeux=self.yeux[0].nbrneurite+self.yeux[1].nbrneurite
        self.nbrneuritepattes=self.pattes["phg"].nbrneurite+self.pattes["pbg"].nbrneurite+self.pattes["phd"].nbrneurite+self.pattes["pbd"].nbrneurite
        self.nbrneurite=self.nbrneuriteyeux+self.nbrneuritepattes

        self.nbrdendriteyeux=self.yeux[0].nbrdendrite+self.yeux[1].nbrdendrite
        self.nbrdendritepattes=self.pattes["phg"].nbrdendrite+self.pattes["pbg"].nbrdendrite+self.pattes["phd"].nbrdendrite+self.pattes["pbd"].nbrdendrite
        self.nbrdendrite=self.nbrdendriteyeux+self.nbrdendritepattes
        
    def miseajourposition(self):
        self.calcMensurations()
        self.calcPosition()
        
    def calcMensurations(self):
        b=self
        long=b.longueur
        large=b.largeur
        self.longdemi=long/2
        self.longquart=long/4
        self.longhuit=long/8
        self.largedemi=large/2
        self.largequart=large/4
        self.largehuit=large/8
        self.largeseize=large/16
        self.longdouble=long*2
        self.longquadruple=long*4
        
    def calcPosition(self):
        b=self
        x=b.x
        y=b.y
        angle=b.angle
        #print("Mise a jour ",b.angle)
        #calc bec
        self.xbeccentre,self.ybeccentre=h.getAngledPoint(math.radians(angle),self.longdemi,x,y)
        #calc anus
        self.xanuscentre,self.yanuscentre=h.getAngledPoint(math.radians(angle+180),self.longdemi,x,y)
        #calc champ de vision gauche
        xo1,yo1=h.getAngledPoint(math.radians(angle+270),self.largequart,x,y)
        self.xoeilgcentre,self.yoeilgcentre=h.getAngledPoint(math.radians(angle),self.longdemi,xo1,yo1)
        self.xoeilgchampgauche,self.yoeilgchampgauche=h.getAngledPoint(math.radians(angle-70),self.longquadruple,self.xoeilgcentre,self.yoeilgcentre)
        self.xoeilgchampdroit,self.yoeilgchampdroit=h.getAngledPoint(math.radians(angle+20),self.longquadruple,self.xoeilgcentre,self.yoeilgcentre)
        #calc champ de vision droit
        xo1,yo1=h.getAngledPoint(math.radians(angle+90),self.largequart,x,y)
        self.xoeildcentre,self.yoeildcentre=h.getAngledPoint(math.radians(angle),self.longdemi,xo1,yo1)
        self.xoeildchampgauche,self.yoeildchampgauche=h.getAngledPoint(math.radians(angle-20),self.longquadruple,self.xoeildcentre,self.yoeildcentre)
        self.xoeildchampdroit,self.yoeildchampdroit=h.getAngledPoint(math.radians(angle+70),self.longquadruple,self.xoeildcentre,self.yoeildcentre)
        # calc narine
        self.xnarineg,self.ynarineg=h.getAngledPoint(math.radians(angle+270),self.largehuit,x,y)
        
        self.xnarined,self.ynarined=h.getAngledPoint(math.radians(angle+90),self.largehuit,x,y)
        
        #dessine pattes
        xcentregauche,ycentregauche=h.getAngledPoint(math.radians(angle+270),self.largedemi,x,y)
        xcentredroit,ycentredroit=h.getAngledPoint(math.radians(angle+90),self.largedemi,x,y)
        #
        self.xphgquart,self.yphgquart=h.getAngledPoint(math.radians(angle),self.longquart,xcentregauche,ycentregauche)#1
        self.xpbgquart,self.ypbgquart=h.getAngledPoint(math.radians(angle+180),self.longquart,xcentregauche,ycentregauche)#2
        
        self.xphdquart,self.yphdquart=h.getAngledPoint(math.radians(angle),self.longquart,xcentredroit,ycentredroit)#3
        self.xpbdquart,self.ypbdquart=h.getAngledPoint(math.radians(angle+180),self.longquart,xcentredroit,ycentredroit)#4
        
        self.xphgdemi,self.yphgdemi=h.getAngledPoint(math.radians(angle),self.longdemi,xcentregauche,ycentregauche)
        self.xpbgdemi,self.ypbgdemi=h.getAngledPoint(math.radians(angle+180),self.longdemi,xcentregauche,ycentregauche)
        
        self.xphddemi,self.yphddemi=h.getAngledPoint(math.radians(angle),self.longdemi,xcentredroit,ycentredroit)
        self.xpbddemi,self.ypbddemi=h.getAngledPoint(math.radians(angle+180),self.longdemi,xcentredroit,ycentredroit)
        
    def metaboliser(self):
        self.sentir()
        self.verifieMembres()
        
    def verifieMembres(self):
        self.verifiePattes()
        
    def verifiePattes(self):
        #print("ON VERIFIE")
        for kk,i in self.pattes.items():
            n=0
            a=0
            b=0
            nivo=0
            for j in i.neurones:
                for k in j.dendrites:
                    k.testseuil()
            #for j in i.neurones:         
                for d in j.neurites:
                    #print("nivo",nivo)
                    nivo=nivo+d.niveau
                    d.niveau=0
            if nivo:
                i.stimuler(nivo)
    
    def sentir(self):
        self.perceptVisuel()
        self.perceptOlfactif()
        self.verifieDendrites()
        
    def verifieDendrites(self):
        #print("OEIL G")
        for i in self.yeux[0].neurones:
            i.dendrites[0].testseuil()
            
        #print("OEIL D")
        for i in self.yeux[1].neurones:
            i.dendrites[0].testseuil()
        #input("TEST OEIL")
        
    
    def perceptOlfactif(self):
        pass #print("IN perceptOlfactif")
        
    def perceptVisuel(self):
        self.objVuD=[]
        self.objVuG=[]
        self.objVuD=self.regarder(self,"d","red")
        self.objVuG=self.regarder(self,"g","blue")
        vud=self.yeux[1].voir(self.objVuD)
        vug=self.yeux[0].voir(self.objVuG)
        
        if vud==0 and vug==0:
            #print("JE VOIS RIEN")
            if self.panic==0:
                ang=random.randrange(30)+15
                cote=random.randrange(2)
                if cote:
                    ang=ang*-1
                self.angle=(self.angle+ang)%360
                rnd=random.randrange(5)
                if rnd==6:#3:
                    print(rnd)
                    self.x,self.y=h.getAngledPoint(math.radians(self.angle),self.longhuit,self.x,self.y)
                #self.miseajourposition()
                self.calcPosition()
                self.panic=self.paniccooldown
            else:
                self.panic-=1
        else:
            pass # print("VU ",vud,vug,self.objVuD,self.objVuG)        

    def etatNeurone(self,n):
        l0=[]
        for i in n.neurones:
            l0.append(i.dendrites[0].niveau)
        return l0
    
    def regarder(self,b,cote,coul):
        obj=[]
        x=b.x
        y=b.y
        long=b.longueur
        maxlong=long * 4
        large=b.largeur
        angle=b.angle
        angled=0
        angleg=0
        ar=angle
        adr=70
        agr=20
        
        if cote=="d":
            angled=(ar+adr)%360
            angleg=(ar-agr)%360
            xo2,yo2=self.xoeildcentre,self.yoeildcentre
            perp=90
        elif cote=="g":
            angled=(ar+agr)%360
            angleg=(ar-adr)%360
            xo2,yo2=self.xoeilgcentre,self.yoeilgcentre
            perp=270
            
        #dessine champ de vision gauche 
        
        for i in self.parent.bouffes:
            # trouve point de largeur perpendiculaire
            xbg,ybg=h.getAngledPoint((angle+90)%360,i.largedemi,i.x,i.y)
            xbd,ybd=h.getAngledPoint((angle+270)%360,i.largedemi,i.x,i.y)
            ## ICI je dois trouver les bordures exterieures pour affecter tous les neurones concerne
            angleb=math.degrees(h.calcAngle(xo2,yo2,i.x,i.y))%360
            
            anglebg=math.degrees(h.calcAngle(xo2,yo2,xbg,ybg))%360
            anglebd=math.degrees(h.calcAngle(xo2,yo2,xbd,ybd))%360
            etendu=int((abs(anglebg-anglebd))/2)
            if etendu<1:
                etendu=0
            ob=0
            anglei=None
            if angled< 90:
                if angleb<angled:
                    ob=1
                    anglei=90-angleb
                elif angleb>angleg and angleb<=360:
                    ob=1
                    anglei=angleb-angleg
            elif angleg< angleb and angleb<angled:
                ob=1
                anglei=angleb-angleg
            if ob:
                d=h.calcDistance(xo2,yo2,i.x,i.y)
                if anglei<0 or anglei>90:
                    print("TROP")
                if d<maxlong:
                    a=round(anglei)
                    if a<90:
                        obj.append([i,round(d),a,etendu])
            
        return obj

    
    def connecteNeuroYeux(self):
        """
        connecte les neurones des yeux aux neurones des pattes
        
        """
        for i in self.yeux:
            m=0
            # connection  aux pattes -> phd=patteHautDroit ; pbg=patteBasGauche
            if i.cote=="gauche":
                p1=self.pattes["phd"].neurones
                p2=self.pattes["pbd"].neurones
                p3=self.pattes["phg"].neurones
                p4=self.pattes["pbg"].neurones
            else:
                p1=self.pattes["phg"].neurones
                p2=self.pattes["pbg"].neurones
                p3=self.pattes["phd"].neurones
                p4=self.pattes["pbd"].neurones
            # variables pour savoir combien furent connecte sur quelle patte
            a1=0
            a2=0
            a3=0
            a4=0
            # pour chaque neurone de l'oeil
            for j in i.neurones:
                # pour chacun de ses neurites
                for k in j.neurites:
                    # connecte sur 
                    m=m+1
                    n=random.randrange(20)
                    if n <12:
                        a1=a1+1
                        self.connecteSynapse(k,p1)
                    elif n<16:
                        a2=a2+1
                        self.connecteSynapse(k,p2)
                    elif n<19:
                        a3=a3+1
                        self.connecteSynapse(k,p3)
                    else:
                        a4=a4+1
                        self.connecteSynapse(k,p4)
            print("All connected",i.cote,a1,a2,a3,a4)
                        
    def connecteSynapse(self,neurite,neurones):
        # connecte le neurite a une dendrite aleatoire d'un neurone aleatoire de la patte choisie
        val=1
        # on se donne 1000 chances de trouver une dendrite sans affectation prealable de neurite
        while val and val<1000:
            n=random.choice(neurones)
            d=random.choice(n.dendrites)
            if d.neurite==None:
                d.neurite=neurite
                neurite.dendrite=d
                return
            else:
                val=val+1 # arret si trop d'iteration
        else:
            print("NON")
        print("PLANTE")
            
class Oeil():
    def __init__(self,parent,cote="gauche",champgauche=-45,champdroite=45):
        self.id=getId()
        self.parent=parent
        self.cote=cote
        self.champgauche=champgauche
        self.champdroite=champdroite
        self.orientation=0 #angle par rapport a l'axe de bibitte
        self.cones=[]
        self.batonnets=[]
        self.neurones=[]
        nbrneurones=abs(self.champgauche)+abs(self.champdroite)
        self.creeNeurones(nbrneurones)
        self.nbrneurone=len(self.neurones)
        self.nbrneurite=0
        self.nbrdendrite=0
        for i in self.neurones:
            self.nbrneurite=self.nbrneurite+i.nbrneurite
            self.nbrdendrite=self.nbrdendrite+i.nbrdendrite
        
    def creeNeurones(self,n):
        for i in range(n):
            n=random.randrange(10)+5
            self.neurones.append(Neurone(self,1,n,2))

    def voir(self,vu):
        n=0
        for i in vu:
            if int(i[3]):
                nn=int(i[2])-int(i[3])
                if nn<0:
                    deb=0
                else:
                    deb=nn
                zz=int(i[2])+int(i[3])+1
                if zz>=len(self.neurones):
                    fin=len(self.neurones)-1
                else:
                    fin=zz
            else:
                deb=int(i[2])
                fin=deb+1
            for k in range(deb,fin):
                neu=None
                try:
                    neu=self.neurones[k]
                except:
                    print("PLANTE LISTE",i) 
                    for j in self.neurones: 
                        print("toto",j)   
                        self.parent.parent.parent.boucleOn=0    
                        break   
                neu.dendrites[0].stimuler()
            #print("dendrite stimuler ",int(i[2]))
        if len(vu)==0:
            return 0
        return 1
        
class Bouche():
    def __init__(self,parent):
        self.id=getId()
        self.parent=parent
        self.etat="repos"
        self.neurones=[]
        self.creeNeurones(50)
        self.nbrneurone=len(self.neurones)
        self.nbrneurite=0
        self.nbrdendrite=0
        for i in self.neurones:
            self.nbrneurite=self.nbrneurite+i.nbrneurite
            self.nbrdendrite=self.nbrdendrite+i.nbrdendrite
    
    def creeNeurones(self,n):
        p=0
        for i in range(n):
            m=random.randrange(10)+10
            self.neurones.append(Neurone(self,m,1,1))
            p=p+m
        
        
class Narine():
    def __init__(self,parent):
        self.id=getId()
        self.parent=parent
        self.etat="repos"
        self.neurones=[]
        nbrneurones=16
        self.creeNeurones(nbrneurones)
        self.nbrneurone=len(self.neurones)
        self.nbrneurite=0
        self.nbrdendrite=0
        for i in self.neurones:
            self.nbrneurite=self.nbrneurite+i.nbrneurite
            self.nbrdendrite=self.nbrdendrite+i.nbrdendrite
        
    def creeNeurones(self,n):
        for i in range(n):
            d=random.randrange(5)+3
            n=random.randrange(3)+1
            s=random.randrange(10)+5
            self.neurones.append(Neurone(self,d,n,s))
        
class Estomac():
    def __init__(self,parent):
        self.id=getId()
        self.parent=parent
        self.etat="repos"
        
class Intestin():
    def __init__(self,parent):
        self.id=getId()
        self.parent=parent
        self.etat="repos"
        self.longueur=10
        
class Anus():
    def __init__(self,parent):
        self.parent=parent
        self.id=getId()
        self.etat="repos"
        
class Patte():
    def __init__(self,parent,position=""):
        self.id=getId()
        self.parent=parent
        self.position=position
        self.niveau=0 #si niveau=seuil alors mouvement
        self.seuil=seuilpatte #4 #apres stimulation le seuil augmente un peu afin de resister a un appel trop rapide
        self.seuilnormal=4
        self.etat="repos" #retour
        self.neurones=[]
        self.creeNeurones(50)
        self.nbrneurone=len(self.neurones)
        self.nbrneurite=0
        self.nbrdendrite=0
        for i in self.neurones:
            self.nbrneurite=self.nbrneurite+i.nbrneurite
            self.nbrdendrite=self.nbrdendrite+i.nbrdendrite
    
    def stimuler(self,n):
        #print("PATEE", n)
        big=n
        small=n/20
        if self.position=="phg":
            ang=big
        elif self.position=="phd":
            ang=-1*big
        elif self.position=="pbg":
            self.parent.x,self.parent.y=h.getAngledPoint(math.radians(self.parent.angle),self.parent.longhuit,self.parent.x,self.parent.y)
            ang=small
        else: #self.position=="pbd":
            self.parent.x,self.parent.y=h.getAngledPoint(math.radians(self.parent.angle),self.parent.longhuit,self.parent.x,self.parent.y)
            ang=-1*small
        self.parent.angle=(self.parent.angle+ang)%360
        #self.parent.miseajourposition()
        log.append([self.position,ang,time.time()])
        self.parent.calcPosition()
        
    def stimuler2(self):
        big=random.randrange(10)+5
        small=random.randrange(3)+1
        if self.position=="phg":
            ang=big
        elif self.position=="phd":
            ang=-1*big
        elif self.position=="pbg":
            self.parent.x,self.parent.y=h.getAngledPoint(math.radians(self.parent.angle),self.parent.longhuit,self.parent.x,self.parent.y)
            ang=small
        else: #self.position=="pbd":
            self.parent.x,self.parent.y=h.getAngledPoint(math.radians(self.parent.angle),self.parent.longhuit,self.parent.x,self.parent.y)
            ang=-1*small
        self.parent.angle=(self.parent.angle+ang)%360
        #self.parent.miseajourposition()
        self.parent.calcPosition()
        
    def creeNeurones(self,n):
        for i in range(n):
            d=random.randrange(10)+10
            s=random.randrange(3)+2
            self.neurones.append(Neurone(self,d,1,s))
        
class Bouffe():
    def __init__(self,v,x,y):
        self.id=getId()
        self.valeur=v
        self.odeur=v
        self.largedemi=v/2
        self.x=x
        self.y=y
        
class Poison():
    def __init__(self,v,x,y):
        self.id=getId()
        self.valeur=v
        self.odeur=v
        self.x=x
        self.y=y
        
class Modele():
    def __init__(self,parent,largeur,hauteur,bouffe=10,pois=10,bibitte=3):
        self.parent=parent
        self.largeur=int(largeur)
        self.hauteur=int(hauteur)
        self.bibittes=[]    
        self.bibittes2=[]
        self.bouffes=[]
        self.poisons=[]
        self.peupleModele(bouffe,pois,bibitte)
        
    def calculeEtatMonde(self):
        pass

    def peupleModele(self,bouf=100,pois=100,bib=10,bib2=10):
        for i in range(int(bouf)):
            v=random.randrange(5,10)#*2
            x=random.randrange(self.largeur)
            y=random.randrange(self.hauteur)
            self.bouffes.append(Bouffe(v,x,y))
            
        for i in range(int(pois)):
            v=random.randrange(10)+2
            x=random.randrange(self.largeur)
            y=random.randrange(self.hauteur)
            self.poisons.append(Poison(v,x,y))
        i=None
        
        a=random.randrange(360)
        x=random.randrange(self.largeur)
        y=random.randrange(self.hauteur)
            
        for i in range(int(bib)):
            a=random.randrange(360)
            x=random.randrange(self.largeur)
            y=random.randrange(self.hauteur)
            long=random.randrange(40)+20
            large=random.randrange(10)+10
            self.bibittes.append(Bibitte(self,long,large,x,y,a))
        if i==None:
            self.bibittes.append(Bibitte(self,200,100,400,300,10))
            
        
        for i in range(int(bib2)):
            a=random.randrange(360)
            x=random.randrange(self.largeur)
            y=random.randrange(self.hauteur)
            long=random.randrange(40)+20
            large=random.randrange(10)+10
            self.bibittes2.append(Bibitte2(self,long,large,x,y,a))
            

if __name__ == '__main__':
    mod=Modele("", 1000,800)
    print(mod)