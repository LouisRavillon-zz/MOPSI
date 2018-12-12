import numpy as np
import random as rd
import time
import copy
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
            return False
        if self.type=="deplacement":
            if not check_empty(plateau,nouvelle_pos):
                print("La case n'est pas vide !")
                return False
            if not norm1(self.vect)==1:
                print("Trop grand déplacement !")
                return False
            if self.de.a_balle:
                print("Le pion a la balle !")
                return False
            return True
        elif self.type=="passe":
            if check_empty(plateau,nouvelle_pos):
                return False
            if self.de.num_joueur!=plateau[nouvelle_pos[0]][nouvelle_pos[1]].num_joueur:
                return False
            if not coords_dans_liste(nouvelle_pos, passe_possible(self.de.position)):
                return False
            return True
    def faire(self,plateau):
        if self.type=="deplacement":
            #print([self.de.position[0],self.de.position[1]])
            plateau[self.de.position[0]][self.de.position[1]].bouge(self.vect)
        elif self.type=="passe":
            nouvelle_pos=self.de.position+self.vect
            plateau[nouvelle_pos[0]][nouvelle_pos[1]].a_balle=True
            plateau[self.de.position[0]][self.de.position[1]].a_balle=False
            
            
            
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
            print("Victoire par antijeu du joueur " + str(num_joueur))
            return True
        ligne_victoire=[self.taille-1,0]
        for p in self.pions:
            if p.position[0]==ligne_victoire[num_joueur-1] and p.num_joueur==num_joueur and p.a_balle:
                print("Victoire classique de " + str(num_joueur))
                return True
        return False
    
    def jouer(self,num_joueur,action):
        if action.est_legale(self.plateau):                
            action.faire(self.plateau)
            self.rafraichir()
    def jouer_trois(self,num_joueur,actions):
        for action in actions:
            self.jouer(num_joueur,action)
    def selection_pions(self,joueur):
        return [p for p in self.pions if p.num_joueur==joueur]
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

def deplacement_naif(pion,plateau):
    for a in [-1,0,1]:
        for b in [-1,0,1]:
            if norm1([a,b])==1:
                A=action("deplacement",pion,[a,b])
                if A.est_legale(plateau.plateau):
                    return A
    return False
def passe_naive(pion,plateau):
    for p in plateau.selection_pions(pion.num_joueur):
        #print(coords_dans_liste(p.position,passe_possible(pion.position)))
        if coords_dans_liste(p.position,passe_possible(pion.position)) and pion.a_balle:
            if ((p.position-pion.position)[1]!=0):
                A=action("passe",pion,p.position-pion.position)
                if A.est_legale(plateau.plateau):
                    return A
    return False
Plateau=plateau()
Plateau.draw()

# while not Plateau.check_victoire(1) and not Plateau.check_victoire(2):
#     for joueur in [1,2]:
#         Actions=[]
#         pions_i=Plateau.selection_pions(joueur)
#         k=rd.randint(0,len(pions_i)-1)
#         for i in range(rd.randint(1,3)):
#             Pass=passe_naive(pions_i[k],Plateau)
#             Move=deplacement_naif(pions_i[k],Plateau)
#             if rd.random()<0.9 and Pass!=False:
#                 Actions+=[Pass]
#             elif Move!=False:
#                 Actions+=[Move]
#         Plateau.jouer(joueur,Actions)
#         Plateau.draw()
#         print(10*"\n")

# def actions_possibles(pion,plateau=Plateau):
#     Actions=[]
#     for a in [-1,0,1]:
#         for b in [-1,0,1]:
#             if norm1([a,b])==1:
#                 A=action("deplacement",pion,np.array([a,b]))
#                 if A.est_legale(plateau.plateau):
#                     Actions+=[A]
#     if pion.a_balle:
#         for c in passe_possible(pion.position):
#             A=action("passe",pion,np.array(c)-pion.position)
#             if A.est_legale(plateau.plateau):
#                 Actions+=[A]
#     return Actions

# def trois_actions_possibles(num_joueur,plateau=Plateau):
#     Actions_1=[actions_possibles(pion,plateau) for pion in plateau.selection_pions(num_joueur)]
#     Actions_2=[]
#     for a in Actions_1:
#         plateau_copie=copy.deepcopy(plateau)
#         a[0].faire(plateau_copie.plateau)
#         A=[actions_possibles(pion,plateau_copie) for pion in plateau_copie.selection_pions(num_joueur)]
#         Actions_2+=[[a[0],b[0]] for b in A]
#     Actions_3=[]
#     for a in Actions_2:
#         plateau_copie=copy.deepcopy(plateau)
#         a[0].faire(plateau_copie.plateau)
#         a[1].faire(plateau_copie.plateau)
#         A=[actions_possibles(pion,plateau_copie) for pion in plateau_copie.selection_pions(num_joueur)]
#         Actions_3+=[a+b for b in A]
#     return Actions_1+Actions_2+Actions_3

# a_p=actions_possibles(Plateau.pions[0])
# for a in a_p:
#     temp=copy.deepcopy(Plateau)
#     temp.jouer(1,[a])
#     temp.draw()

A=action("deplacement",Plateau.plateau[0][2],np.array([1,0]))

Plateau.jouer_trois(1,[A])
B=action("deplacement",Plateau.plateau[1][2],np.array([1,0]))
print(Plateau.plateau[1][2])
Plateau.jouer_trois(1,[B])

Plateau.draw()