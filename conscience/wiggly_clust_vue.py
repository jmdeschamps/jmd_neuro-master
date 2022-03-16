# -*- coding: utf-8 -*-
"""
Neuro_wiggly est une simulation neuronale
PREAMBULE
ce programme est une simulation cherchant à imiter les liens entre neurones et organes.
Dans ce sens les comportements (action des entites) ne sont pas programm� au sens
courant, mais d�coule de l'activation des composantes neuronales.
PRINCIPES
- les neurones sont compos�s de dendrites (entr�es) et de neurites (sorties)
- les dendrites peuvent recevoir leur stimulation d'un sens (generalement ratach� �
un organe), ou d'une dendrite.
- le neurone envoie un signal aux neurites
- les neurites (les terminaux au bout des axones) transmettent leur signaux � des dendrites
ou � d'autres types d'organes (muscles, glandes, etc)
- les composantes ont des seuils � atteindre avant de transmettre un signal
- les composantes ont un dur�e de repos avant de pouvoir �tre r�activer

VERSIONS
-V_01-
Bibitte initiale
- les bibittes sont compos�es de syst�me de vision binoculaire, champ de 90 degr�es, 
de 20 deg vers le centre, 70 vers l'ext�rieur (champ central commun),
les yeux sont compos� de 90 neurones (un par degr�),chacun poss�dant un seul dendrite
stimulable, mais de 10 � 15 neurites.
- les yeux sont connectes sur les pattes et les stimulent, ce qui occasione leur contraction,
qui s'interpr�tent par un mouvement



"""
import math
import random
from tkinter import *
from tkinter import ttk
#from jmdwidgets import *
import time
from helper import Helper as h
"""
ajouter l'odorat
ajouter la r�action adverse aux autres
"""
# 30 aout 2014, jmd    _v2_01 - refactorisation de l'approche, en largeur plutot qu'en profondeur
idcourant=0
seuilmin=2
seuilpatte=6
log=[]
def getId():
    global idcourant
    idcourant=idcourant+1
    return idcourant

# Vue debut **********************
class Vue():
    # classe d'entree/sortie, le V de MVC
    def __init__(self, parent,modele):
        self.parent=parent
        self.modele=modele
        self.root=Tk()
        self.root.title("Simpleboucle")
        self.large=1200
        self.haut=800
        
        self.taboptionswidgets={}
        self.bibdetail=None
        
        self.root.protocol("WM_DELETE_WINDOW", self.fermeture)
        self.montreodorat=IntVar()
        self.montrevision=IntVar()
        self.montrevision.set(0)
        self.updatevisuel=IntVar()
        self.updatevisuel.set(1)
        self.initialiseRoot()
        self.initialiseTerrain(self.tabvisuel)
        self.initialiseDetail(self.tabvisuel)
        self.initialiseExecution(self.taboption)
        
    def fermeture(self):
        f=open("simple.txt","w")
        for i in log:
            s=str(i)+"\n"
            f.write(s)
        f.close()
        self.root.destroy()

    def dessinemodele(self,modele):
        self.canevas.delete(ALL)
        for i in modele.bouffes:
            self.canevas.create_oval(i.x-i.largedemi,i.y-i.largedemi,
                                     i.x+i.largedemi,i.y+i.largedemi,
                                     fill="green",tags=("bouffe",i.id))
            #self.canevas.create_text(i.x+5,i.y,anchor="w",text=i.id,tags=("bouffe",i.id))
        for i in modele.poisons:
            self.canevas.create_rectangle(i.x-3,i.y-3,i.x+3,i.y+3,fill="purple",tags=("poison",i.id))
        self.dessineBibittes(modele.bibittes) # changer pour fournir liste bibittes
        #self.dessineBibittes2(modele.bibittes2) # changer pour fournir liste bibittes
    
    def initialiseRoot(self):
        self.mainpane=PanedWindow(self.root)
        ###
        self.tabvisuel= ttk.Notebook(self.mainpane, name='visuel')
        self.mainpane.add(self.tabvisuel,minsize=100)
        ###
        self.taboption= ttk.Notebook(self.mainpane, name='option')
        self.mainpane.add(self.taboption,minsize=100)
        ###
        self.mainpane.pack(expand=1,fill=BOTH)
                
    def initialiseTerrain(self,tab):
        self.cadreterrain=Frame(tab,width=200,height=400,bg="green")
        scVert=Scrollbar(self.cadreterrain)
        scVert.pack(side=RIGHT, fill=Y)
        scHoriz=Scrollbar(self.cadreterrain,orient=HORIZONTAL)
        scHoriz.pack(side=BOTTOM, fill=X)
        self.canevas=Canvas(self.cadreterrain,width=self.large,height=self.haut,
                            scrollregion=(0,0,self.large,self.haut),
                            yscrollcommand=scVert.set,
                            xscrollcommand=scHoriz.set,bg="linen")
        self.canevas.tag_bind("bibitte", "<Button>", self.getbibitte)
        self.canevas.tag_bind("bouffe", "<Button>", self.getbouffe)
        scVert.config(command=self.canevas.yview)
        scHoriz.config(command=self.canevas.xview)
        self.canevas.pack(expand=1,fill=BOTH)
        tab.add(self.cadreterrain,text='Terrain')
        
    def initialiseDetail(self,tab):
        self.cadredetail=Frame(tab,width=200,height=400,bg="blue")
        scVert2=Scrollbar(self.cadredetail)
        scVert2.pack(side=RIGHT, fill=Y)
        scHoriz2=Scrollbar(self.cadredetail,orient=HORIZONTAL)
        scHoriz2.pack(side=BOTTOM, fill=X)
        self.canevasdetail=Canvas(self.cadredetail,width=300,height=400,
                                  scrollregion=(0,0,1000,1000),
                            yscrollcommand=scVert2.set,
                            xscrollcommand=scHoriz2.set,bg="black")
        self.canevasdetail.bind("<Button>",self.montreid)
        scVert2.config(command=self.canevasdetail.yview)
        scHoriz2.config(command=self.canevasdetail.xview)
        self.canevasdetail.pack(expand=1,fill=BOTH)
        tab.add(self.cadredetail,text='Detail')
            
    def initialiseExecution(self,tab):
        self.cadreEntries=Frame(tab)
        # create the notebook
        self.cadreEntries.pack(side=LEFT)
        rn=random.randrange(100)+17
        entrees=[["Nbre Bibitte",3,""],
                ["Nbre Bouffe",30,""],
                ["Nbre Poison",0,""],
                ["Largeur",1200,""],
                ["Hauteur",800,"toito"],
                ["Random seed",rn,"tourloup"]]
        cadreentree=Frame(self.cadreEntries)
        self.taboptionswidgets={}
        r=1
        for i in entrees:
            e=Entry(cadreentree)
            e.insert(0,str(i[1]))
            self.taboptionswidgets[i[0]]=e
            l1=Label(cadreentree,text=i[0])
            l2=Label(cadreentree,text=i[2])
            l1.grid(column=0,row=r)
            e.grid(column=1,row=r)
            l2.grid(column=2,row=r)
            r=r+1
            
        
        rang=0
        b=Label(self.cadreEntries,text="Valeurs de démarrage")
        b.grid(column=0,row=rang,columnspan=2)
        cadreentree.grid(column=0,row=rang+1,columnspan=2)
        #
        b=Button(self.cadreEntries,text="Demarre session",command=self.demarre)
        b.grid(column=0,row=rang+2,columnspan=2)
        ba=Button(self.cadreEntries,text="Active")
        ba.bind("<Button>",self.pause)
        ba.grid(column=0,row=rang+4,columnspan=2)
        db=Button(self.cadreEntries,text="Debug")
        db.bind("<Button>",self.mondebug)
        db.grid(column=0,row=rang+5,columnspan=2)
        c =Checkbutton( self.cadreEntries, text="Montre champ de vision", variable=self.montrevision)
        c.grid(column=0,row=rang+6,columnspan=2)
        d =Checkbutton( self.cadreEntries, text="Montre champ d'odorat", variable=self.montreodorat)
        d.grid(column=0,row=rang+7,columnspan=2)
        
        d =Checkbutton( self.cadreEntries, text="Update Visuel", variable=self.updatevisuel)
        d.grid(column=0,row=rang+8,columnspan=2)
        
        self.iteration=Label(self.cadreEntries,text="Itérations: 0")
        self.iteration.grid(column=0,row=rang+9,columnspan=2)
        
        tab.add(self.cadreEntries,text="Options")
        
    def demarre(self):
        self.parent.demarresession()
        
    def setTailleCanevas(self,large,haut):
        self.canevas.config(scrollregion=(0,0,large,haut))
        
    def getbibitte(self,evt):
        tag=self.canevas.gettags(CURRENT)
        bib=self.parent.getBibitte(int(tag[1]))
        self.bibdetail=bib
        self.dessineBibitteDetail()
        print("Clique bibitte",bib)
        
    def getbouffe(self,evt):
        print("Clique bouffe",evt)
        
    def montreid(self,evt):
        return
        #tag=self.canevasdetail.gettags(CURRENT)
        #self.note.delete(0.0,END)
        #self.note.insert(0.0,str(tag)+"ok")
        
    def mondebug(self,evt):
        widg=evt.widget
        if self.parent.debugOn:
            self.parent.debugOn=0
            widg.config(text="Demarrare debug")
        else:
            self.parent.debugOn=1
            widg.config(text="Arrete debug")
        
    def pause(self,evt):
        widg=evt.widget
        if self.parent.boucleOn==1:
            self.parent.boucleOn=0
            widg.config(text="Active")
        else:
            self.parent.boucleOn=1
            widg.config(text="Pause")
            self.parent.metabolise()
    
    def dessineBibittes2(self,bib):
        self.bibittes2={} # ajout pour conserver les items de bibittes
        if bib:
            self.canevas.delete("bibitte2")
            for i in bib:
                dicitem=self.dessineBibitte2(i)
                self.bibittes2[i.id]=dicitem
                if i==self.bibdetail:
                    self.updatedetail()
    
    def dessineBibitte2(self,b):
        bibitems={} #dico des items pour cet bibitte
        #dessine corps
        bibitems["corps"]=self.canevas.create_oval(b.x-5,b.y-5,b.x+5,b.y+5,fill="lightgreen",tags=("bibitte2",))
        
    
        return bibitems
                    
                    
    def dessineBibittes(self,bib):
        self.bibittes={} # ajout pour conserver les items de bibittes
        if bib:
            self.canevas.delete("bibitte")
            for i in bib:
                dicitem=self.dessineBibitte(i)
                self.bibittes[i.id]=dicitem
                if i==self.bibdetail:
                    self.updatedetail()
    
    def dessineBibitte(self,b):
        bibitems={} #dico des items pour cet bibitte
        #dessine systeme visuel
        bibitems["oeilgauche"]=self.canevas.create_oval(b.xoeilgcentre-b.largehuit,b.yoeilgcentre-b.largehuit,
                                 b.xoeilgcentre+b.largehuit,b.yoeilgcentre+b.largehuit,
                                 fill="green",tags=("bibitte",b.id))

        bibitems["oeildroit"]=self.canevas.create_oval(b.xoeildcentre-b.largehuit,b.yoeildcentre-b.largehuit,
                                 b.xoeildcentre+b.largehuit,b.yoeildcentre+b.largehuit,
                                 fill="red",tags=("bibitte",b.id))
        #dessine champ de vision gauche
        
        
        x1=b.xoeilgcentre-b.longquadruple
        y1=b.yoeilgcentre-b.longquadruple
        x2=b.xoeilgcentre+b.longquadruple
        y2=b.yoeilgcentre+b.longquadruple
        ang=(360-b.angle)-20
        bibitems["oeilgauchechamppie"]=self.canevas.create_arc((x1,y1,x2,y2),
                                                               start= ang, extent=90,
                                                               outline="blue",tags=("bibitte",b.id))
        

        x1=b.xoeildcentre-b.longquadruple
        y1=b.yoeildcentre-b.longquadruple
        x2=b.xoeildcentre+b.longquadruple
        y2=b.yoeildcentre+b.longquadruple
        ang=(360-b.angle)-70
        bibitems["oeildroitchamppie"]=self.canevas.create_arc((x1,y1,x2,y2),
                                                               start= ang, extent=90,
                                                               outline="red",tags=("bibitte",b.id))
        #dessine corps
        bibitems["corps"]=self.canevas.create_polygon(b.xpbgdemi,b.ypbgdemi,
                                    b.xphgdemi,b.yphgdemi,
                                    b.xphddemi,b.yphddemi,
                                    b.xpbddemi,b.ypbddemi,
                                    fill="gold",tags=("bibitte",b.id))
        #dessine systeme digestif 
        #dessine intestin
        bibitems["intestin"]=self.canevas.create_line(b.x,b.y,
                                    b.xanuscentre,b.yanuscentre,width=b.largequart,
                                    fill="pink",tags=("bibitte",b.id))
        #dessine oesophage
        #self.xbeccentre,self.ybeccentre
        bibitems["oesophage"]=self.canevas.create_line(b.x,b.y,
                                    b.xbeccentre,b.ybeccentre,width=b.largequart,
                                    fill="lightblue",tags=("bibitte",b.id))
        #dessine estomac
        bibitems["estomac"]=self.canevas.create_oval(b.x-b.largehuit,b.y-b.largehuit,
                                 b.x+b.largehuit,b.y+b.largehuit,
                                 fill="lightblue",tags=("bibitte",b.id))
        #dessine pattes
        bibitems["pdb"]=self.canevas.create_line(b.xpbddemi,b.ypbddemi,b.xpbdquart,b.ypbdquart,
                                 width=b.largehuit,
                                 fill="brown",tags=("bibitte",b.id))
        bibitems["phd"]=self.canevas.create_line(b.xphddemi,b.yphddemi,b.xphdquart,b.yphdquart,
                                 width=b.largehuit,
                                 fill="brown",tags=("bibitte",b.id))
        bibitems["pbg"]=self.canevas.create_line(b.xpbgdemi,b.ypbgdemi,b.xpbgquart,b.ypbgquart,
                                 width=b.largehuit,
                                 fill="brown",tags=("bibitte",b.id))
        bibitems["phg"]=self.canevas.create_line(b.xphgdemi,b.yphgdemi,b.xphgquart,b.yphgquart,
                                 width=b.largehuit,
                                 fill="brown",tags=("bibitte",b.id))
        
        #*********  Odorat
        etendu=240
        ang=(360-b.angle)-(etendu/2)
        
        x1=b.xbeccentre-b.longueur
        y1=b.ybeccentre-b.longueur
        x2=b.xbeccentre+b.longueur
        y2=b.ybeccentre+b.longueur
        bibitems["odor3"]=self.canevas.create_arc((x1,y1,x2,y2),style="arc",
                                                               start= ang, extent=etendu,
                                                               outline="red",tags=("bibitte",b.id))
        
        x1=b.xbeccentre-b.longdemi
        y1=b.ybeccentre-b.longdemi
        x2=b.xbeccentre+b.longdemi
        y2=b.ybeccentre+b.longdemi
        bibitems["odor2"]=self.canevas.create_arc((x1,y1,x2,y2),style="arc",
                                                               start= ang, extent=etendu,
                                                               outline="red",tags=("bibitte",b.id))
                                     
        x1=b.xbeccentre-b.longquart
        y1=b.ybeccentre-b.longquart
        x2=b.xbeccentre+b.longquart
        y2=b.ybeccentre+b.longquart
        bibitems["odor1"]=self.canevas.create_arc((x1,y1,x2,y2),style="arc",
                                                               start= ang, extent=etendu,
                                                               outline="red",tags=("bibitte",b.id))
        
    
        return bibitems

    def updateBibittes2(self,cadre,bib):
        if bib and self.updatevisuel.get():
            self.canevas.delete("bibitte2")
            for i in bib:
                self.updateBibitte2(i)

    def updateBibittes(self,cadre,bib):
        if bib and self.updatevisuel.get():
            #self.canevas.delete("bibitte")
            for i in bib:
                self.updateBibitte(i)
                if i==self.bibdetail:
                    self.updatedetail()
        self.iteration.config(text="Itérations : "+str(cadre))
        
    def updateBibitte2(self,b):
        self.canevas.create_oval(b.x-5,b.y-5,b.x+5,b.y+5,fill="lightgreen",tags=("bibitte2",))
        
    def updateBibitte(self,b):
        bibitems=self.bibittes[b.id]
        #dessine systeme visuel
        self.canevas.coords(bibitems["oeilgauche"], b.xoeilgcentre-b.largehuit,b.yoeilgcentre-b.largehuit,
                                 b.xoeilgcentre+b.largehuit,b.yoeilgcentre+b.largehuit)
        
        self.canevas.coords(bibitems["oeildroit"], b.xoeildcentre-b.largehuit,b.yoeildcentre-b.largehuit,
                                 b.xoeildcentre+b.largehuit,b.yoeildcentre+b.largehuit)    
    
        #dessine corps
        self.canevas.coords(bibitems["corps"], b.xpbgdemi,b.ypbgdemi,
                                    b.xphgdemi,b.yphgdemi,
                                    b.xphddemi,b.yphddemi,
                                    b.xpbddemi,b.ypbddemi)
        
        #dessine systeme digestif 
        #dessine intestin
        self.canevas.coords(bibitems["intestin"], b.x,b.y,
                                    b.xanuscentre,b.yanuscentre)
        #dessine oesophage
        #self.xbeccentre,self.ybeccentre
        self.canevas.coords(bibitems["oesophage"], b.x,b.y,
                                    b.xbeccentre,b.ybeccentre)
        #dessine estomac
        self.canevas.coords(bibitems["estomac"], b.x-b.largehuit,b.y-b.largehuit,
                                 b.x+b.largehuit,b.y+b.largehuit)
        #dessine pattes
        self.canevas.coords(bibitems["pdb"], b.xpbddemi,b.ypbddemi,b.xpbdquart,b.ypbdquart)
        
        self.canevas.coords(bibitems["phd"], b.xphddemi,b.yphddemi,b.xphdquart,b.yphdquart)
        
        self.canevas.coords(bibitems["pbg"], b.xpbgdemi,b.ypbgdemi,b.xpbgquart,b.ypbgquart)
        
        self.canevas.coords(bibitems["phg"], b.xphgdemi,b.yphgdemi,b.xphgquart,b.yphgquart)
        
        #dessine champs de vision
        if self.montrevision.get():
            self.canevas.itemconfigure(bibitems["oeilgauchechamppie"], state='normal')
            self.canevas.itemconfigure(bibitems["oeildroitchamppie"], state='normal')
            
            
            x1=b.xoeilgcentre-b.longquadruple
            y1=b.yoeilgcentre-b.longquadruple
            x2=b.xoeilgcentre+b.longquadruple
            y2=b.yoeilgcentre+b.longquadruple
            ang=(360-b.angle)-20
            self.canevas.coords(bibitems["oeilgauchechamppie"],(x1,y1,x2,y2))
            self.canevas.itemconfig(bibitems["oeilgauchechamppie"],start=ang)
            
            
            x1=b.xoeildcentre-b.longquadruple
            y1=b.yoeildcentre-b.longquadruple
            x2=b.xoeildcentre+b.longquadruple
            y2=b.yoeildcentre+b.longquadruple
            ang=(360-b.angle)-70
            self.canevas.coords(bibitems["oeildroitchamppie"],(x1,y1,x2,y2))
            self.canevas.itemconfig(bibitems["oeildroitchamppie"],start=ang)
        else: 
            self.canevas.itemconfigure(bibitems["oeilgauchechamppie"], state='hidden')
            self.canevas.itemconfigure(bibitems["oeildroitchamppie"], state='hidden')
        
        #dessine champs odorants    
        if self.montreodorat.get():
            
            self.canevas.itemconfigure(bibitems["odor3"], state='normal')
            self.canevas.itemconfigure(bibitems["odor2"], state='normal')
            self.canevas.itemconfigure(bibitems["odor1"], state='normal')
            
            ang=(360-b.angle)-(120)
            x1=b.xbeccentre-b.longdemi
            y1=b.ybeccentre-b.longdemi
            x2=b.xbeccentre+b.longdemi
            y2=b.ybeccentre+b.longdemi
            self.canevas.coords(bibitems["odor3"], (x1,y1,x2,y2))
            self.canevas.itemconfigure(bibitems["odor3"], start=ang)
            
            x1=b.xbeccentre-b.longquart
            y1=b.ybeccentre-b.longquart
            x2=b.xbeccentre+b.longquart
            y2=b.ybeccentre+b.longquart
            self.canevas.coords(bibitems["odor2"],(x1,y1,x2,y2))
            self.canevas.itemconfigure(bibitems["odor2"], start=ang)
            
            x1=b.xbeccentre-b.longhuit
            y1=b.ybeccentre-b.longhuit
            x2=b.xbeccentre+b.longhuit
            y2=b.ybeccentre+b.longhuit
            self.canevas.coords(bibitems["odor1"],(x1,y1,x2,y2))
            self.canevas.itemconfigure(bibitems["odor1"], start=ang)
        else: 
            self.canevas.itemconfigure(bibitems["odor3"], state='hidden')
            self.canevas.itemconfigure(bibitems["odor2"], state='hidden')
            self.canevas.itemconfigure(bibitems["odor1"], state='hidden')
            


    def dessineBibitteDetail(self): #dessine l'activite neuronale de cette bibitte
        self.connectans=[]
        self.dicodendrite={}
        b=self.bibdetail
        self.canevasdetail.delete("neuro")
        echelle=0.5
        xx=b.nbrneuriteyeux*echelle
        yy=(b.nbrdendritepattes/2)*echelle
        #pr"Neurites",(0,0,xx,yy))
        deby=10 *echelle
        debx=10*echelle
        unitey=16*echelle
        unitex=4*echelle
        unitexdemi=unitex/2*echelle
        #pr"detail",debx)
        for i in b.yeux:
            for j in i.neurones:
                xsoma=(j.nbrneurite/2)*echelle
                debx=debx+xsoma
                self.canevasdetail.create_rectangle(debx-unitexdemi,deby,debx+unitexdemi,deby+unitey,
                                                    outline="",fill="green",
                                                    tags=("neuro","a"+str(j.id),"dendrite",str(j.dendrites[0].id),
                                                          debx-unitexdemi,deby,debx+unitexdemi,deby+unitey))
                deby=deby+unitey
                self.canevasdetail.create_rectangle(debx-unitexdemi,deby,debx+unitexdemi,deby+unitey,
                                                    outline="",fill="yellow",
                                                    tags=("neuro","a"+str(j.id),"soma",str(j.id),
                                                          debx-unitexdemi,deby,debx+unitexdemi,deby+unitey))
                deby=deby+unitey
                
                debx=debx-xsoma
                unitex=1*echelle
                for k in j.neurites:
                    nd=self.canevasdetail.create_rectangle(debx,deby,debx+unitexdemi,deby+unitey,width=0,
                                                        outline="",fill="lightgreen",
                                                        tags=("neuro","a"+str(j.id),"neurite",str(k.id),
                                                              debx,deby,debx+unitexdemi,deby+unitey))
                    self.connectans.append([k,[debx+unitexdemi,deby+unitey],k.dendrite.id])
                    debx=debx+(1*echelle)
                unitex=4*echelle
                deby=10*echelle
                debx=debx+(2*echelle)
            debx=debx+(10*echelle)
            
        if debx>xx:
            xx=debx
        deby=50*echelle
        debx=10*echelle
        unitey=4*echelle
        unitex=16*echelle
        uniteydemi=unitey/2*echelle
        for h,i in self.bibdetail.pattes.items():
            if h=="phg":
                debx=10*echelle
                deby=50*echelle
                cote="g"
            elif h=="phd":
                debx=xx-(30*echelle)
                deby=50*echelle
                cote="d"
            elif h=="pbg":
                debx=10*echelle
                deby=yy/2*echelle
                cote="g"
            elif h=="pbd":
                debx=xx-(30*echelle)
                deby=yy/2*echelle
                cote="d"
            if cote=="g":
                for j in i.neurones:
                    xsoma=(j.nbrdendrite/2)*echelle
                    deby=deby+xsoma
                    unitey=4*echelle
                    for k in j.neurites:
                        self.canevasdetail.create_rectangle(debx,deby,debx+unitex,deby+unitey,
                                                            outline="",fill="green",
                                                            tags=("neuro","a"+str(j.id),"neurite",str(k.id),
                                                                  debx,deby,debx+unitex,deby+unitey))
                        deby=deby+unitey
                    debx=debx+unitex
                    deby=deby-(xsoma/2)
                    self.canevasdetail.create_rectangle(debx,deby,debx+unitex,deby+unitey,
                                                        outline="",fill="yellow",
                                                        tags=("neuro","a"+str(j.id),"soma",str(j.id),
                                                              debx-unitexdemi,deby,debx+unitexdemi,deby+unitey))
                    debx=debx+unitex
                    
                    deby=deby-xsoma
                    unitey=1*echelle
                    for k in j.dendrites:
                        nd=self.canevasdetail.create_rectangle(debx,deby,debx+unitex,deby+unitey,width=0,
                                                            outline="",fill="lightgreen",
                                                            tags=("neuro","a"+str(j.id),"dendrite",str(k.id),
                                                                  debx,deby,debx+unitexdemi,deby+unitey))
                        deby=deby+(1*echelle)
                        self.dicodendrite[k.id]=[debx+unitexdemi,deby+unitey]
                    unitex=16*echelle
                    deby=deby+(10*echelle)
                    debx=debx-(unitex*2)
                if deby>yy:
                    yy=deby
            else:
                for j in i.neurones:
                    xsoma=(j.nbrdendrite/2)*echelle
                    deby=deby+xsoma
                    unitey=4*echelle
                    for k in j.neurites:
                        self.canevasdetail.create_rectangle(debx,deby,debx+unitex,deby+unitey,
                                                            outline="",fill="green",
                                                            tags=("neuro","a"+str(j.id),"neurite",str(k.id),
                                                                  debx,deby,debx+unitex,deby+unitey))
                        deby=deby+unitey
                    debx=debx-unitex
                    deby=deby-(xsoma/2)
                    self.canevasdetail.create_rectangle(debx,deby,debx+unitex,deby+unitey,
                                                        outline="",fill="yellow",
                                                        tags=("neuro","a"+str(j.id),"soma",str(j.id),
                                                              debx,deby,debx+unitex,deby+unitey))
                    debx=debx-unitex
                    
                    deby=deby-xsoma
                    unitey=1*echelle
                    for k in j.dendrites:
                        nd=self.canevasdetail.create_rectangle(debx,deby,debx+unitex,deby+unitey,width=0,
                                                            outline="",fill="lightgreen",
                                                            tags=("neuro","a"+str(j.id),"dendrite",str(k.id),
                                                                  debx,deby,debx+unitex,deby+unitey))
                        deby=deby+(1*echelle)
                        
                        self.dicodendrite[k.id]=[debx+unitex,deby+unitey]
                    unitex=16*echelle
                    deby=deby+(10*echelle)
                    debx=debx+(unitex*2)
                    
            debx=debx+(10*echelle)
            if deby>yy:
                yy=deby
        
        self.canevasdetail.config(scrollregion=(0,0,xx+(50*echelle),yy+(20*echelle)))
        

        for i in self.connectans:
            x3,y3=self.dicodendrite[i[2]]
            x1=i[1][0]
            y1=i[1][1]
            x2=x1
            y2=y3
            self.dicodendrite[i[2]]=[[x1,y1,x2,y2],[x2,y2,x3,y3]]
            
        
    def updatedetail(self):
        self.canevasdetail.delete("neurofil")
        for i in self.bibdetail.yeux:
            for j in i.neurones:
                self.updateobjet(j)
        for i,j in self.bibdetail.pattes.items():
            for k in j.neurones:
                self.updateobjet(k)
                    
    def updateobjet(self,neu):
        dends=neu.dendrites
        neurs=neu.neurites
        objs=self.canevasdetail.find_withtag("a"+str(neu.id))
        for j in objs:
            tag=self.canevasdetail.gettags(j)
            if "dendrite" in tag:
                id1=tag[3]
                obj=self.getObject(dends,id1)
                if obj != -1:
                    coul="#%02x%02x%02x" % (0, (obj.niveau*30)+100, 0)
                    self.canevasdetail.itemconfig(j,fill=coul)
            if "soma" in tag:
                coul="#%02x%02x%02x" % (0, 0,120+(neu.niveau*30))
                self.canevasdetail.itemconfig(j,fill=coul)
            if "neurite" in tag:
                id1=tag[3]
                obj=self.getObject(neurs,id1)
                if obj != -1:
                    coul="#%02x%02x%02x" % ( (obj.niveau*30)+100,0, 0)
                    self.canevasdetail.itemconfig(j,fill=coul)
                    if obj.niveau==obj.seuil and obj.dendrite:
                        self.dessineContact(obj.dendrite.id)
                
    def dessineContact(self,id):
        i,j=self.dicodendrite[id]
        self.canevasdetail.create_line(i,fill="red",width=1,tags=("neurofil",))
        self.canevasdetail.create_line(j,fill="red",width=1,tags=("neurofil",))
        
    def getObject(self,liste,id):
        for i in liste:
            if str(i.id) == id:
                return i
        return -1
         
        
if __name__ == '__main__':
    v=Vue("","")
    v.root.mainloop()