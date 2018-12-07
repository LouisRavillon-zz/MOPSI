import numpy as np
import random as rd

taille=7

def check_coords(coords):
    return 0<=coords[0]<taille and 0<=coords[1]<taille

def check_empty(plateau,coords):
    return plateau[coords[0]][coords[1]]==0

def norm1(vect):
    return abs(vect[0])+abs(vect[1])

def passe_possible(coords,t=taille):
    liste_cases=[]
    liste_cases_v=[[(coords[0]+i)%t,coords[1]] for i in range(1,t)]
    liste_cases_h=[[coords[0],(coords[1]+i)%t] for i in range(1,t)]
    liste_cases_diag1=[[liste_cases_v[i][0],liste_cases_h[i][1]] for i in range(t-1)]
    liste_cases_diag2=[[liste_cases_v[i][0],liste_cases_h[-i-1][1]] for i in range(t-1)]
    liste_cases=liste_cases_v+liste_cases_h+liste_cases_diag1+liste_cases_diag2
    return liste_cases

def coords_dans_liste(c,l):
    for c_p in l:
        if c[0]==c_p[0] and c[1]==c_p[1]:
            return True
    return False

class pion:
    def __init__(self,pos=np.array([rd.randint(0,taille),rd.randint(0,taille)]),num=rd.choice([1,2]),a_b=rd.choice([True,False])):
        self.position=pos
        self.num_joueur=num
        self.a_balle=a_b
    def bouge(self,vect):
        self.position+=vect
    def nb_voisins(self,plateau):
        nb_vois=0
        for a in [-1,0,1]:
            for b in [-1,0,1]:
                if norm1([a,b])!=0:
                    pos_actuelle=np.array([a,b])+self.position
                    if check_coords(pos_actuelle) and plateau[pos_actuelle[0]][pos_actuelle[1]]!=0 and plateau[pos_actuelle[0]][pos_actuelle[1]].num_joueur==self.num_joueur:
                        nb_vois+=1
        return nb_vois
    def en_contact(self,plateau):
        for a in [-1,1]:
            pos_actuelle=np.array([a,0])+self.position
            if check_coords(pos_actuelle) and plateau[pos_actuelle[0]][pos_actuelle[1]]!=0 and plateau[pos_actuelle[0]][pos_actuelle[1]].num_joueur==3-self.num_joueur:
                return True
        return False
                    
        
class action:
    def __init__(self,type_=rd.choice(["deplacement","passe"]),p=pion(),v=np.array([0,0])):
        self.type=type_
        self.de=p
        self.vect=v
    def est_legale(self,plateau):
        nouvelle_pos=self.de.position+self.vect
        if not check_coords(nouvelle_pos):
            print(nouvelle_pos)
            return False
        if self.type=="deplacement":
            if not check_empty(plateau,nouvelle_pos):
                print("pas vide")
                return False
            if not norm1(self.vect)==1:
                return False
            return True
        elif self.type=="passe":
            if check_empty(plateau,nouvelle_pos):
                print("vide")
                return False
            if self.de.num_joueur!=plateau[nouvelle_pos[0]][nouvelle_pos[1]].num_joueur:
                print("pb joueur")
                return False
            if not coords_dans_liste(nouvelle_pos, passe_possible(self.de.position)):
                print("passe impo")
                return False
            return True
    def faire(self,plateau):
        if self.type=="deplacement":
            self.de.bouge(self.vect)
        elif self.type=="passe":
            nouvelle_pos=self.de.position+self.vect
            plateau[nouvelle_pos[0]][nouvelle_pos[1]].a_balle=True
            self.de.a_balle=False
            
            
            
class plateau:
    def __init__(self):
        self.taille=taille
        self.pions=[]
        self.plateau=[[0 for i in range(self.taille)]for j in range(self.taille)]
        for i in range(self.taille):
            self.pions+=[pion(np.array([0,i]),1,i==self.taille//2)]
            self.pions+=[pion(np.array([self.taille-1,i]),2,i==self.taille//2)]
        for p in self.pions:
            self.plateau[p.position[0]][p.position[1]]=p
    def rafraichir(self):
        self.plateau=[[0 for i in range(self.taille)]for j in range(self.taille)]
        for p in self.pions:
            self.plateau[p.position[0]][p.position[1]]=p
    
    def check_antijeu(self,num_joueur):
        pions_joueurs=[p for p in self.pions if p.num_joueur==num_joueur]
        hist=[0 for i in range(self.taille)]
        for p in pions_joueurs:
            hist[p.position[0]]+=1
        for i in hist:
            if i!=1:
                return False
        nb_contacts=0
        for p in pions_joueurs:
            if 0<p.position[0]<self.taille-1 and p.nb_voisins(self.plateau)!=2:
                return False
            if p.en_contact(self.plateau):
                nb_contacts+=1
        return nb_contacts>=3
    
    def check_victoire(self,num_joueur):
        if self.check_antijeu(3-num_joueur):
            return True
        ligne_victoire=[self.taille-1,0]
        for p in self.pions:
            if p.position[0]==ligne_victoire[num_joueur-1] and p.num_joueur==num_joueur and p.a_balle:
                return True
        return False
    
    def jouer(self,num_joueur,actions):
        assert(0<len(actions)<=3)
        for action in actions:
            if action.est_legale(self.plateau):                
                action.faire(self.plateau)
                self.rafraichir()
    def draw(self):
        chaine=""
        for i in range(self.taille):
            for j in range(self.taille):
                case_actuelle=self.plateau[i][j]
                if self.plateau[i][j]!=0:
                    chaine+="  "+str(case_actuelle.num_joueur)+"b"*case_actuelle.a_balle+"  "
                else:
                    chaine+="     "
            chaine+="\n\n"
        print(chaine)


Plateau=plateau()
pionA=Plateau.plateau[0][3]
A=action("deplacement",pionA,np.array([1,0]))
B=action("deplacement",pionA,np.array([1,0]))
Plateau.jouer(1,[A,B])
Plateau.draw()
                