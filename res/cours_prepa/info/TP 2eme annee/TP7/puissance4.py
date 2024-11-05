#%%

import matplotlib.pyplot as plt

n = 6
m = 7

def f(n):
    if n==0: return " "
    elif n==1 : return "o"
    elif n==2 : return "x"

def afficher_grille(grille):
    num = [" "]+[str(j) for j in range(m)]+[" "]
    print(" ".join(num))
    for i in range(n):
        l = [str(i)]
        l += [f(x) for x in grille[i]]
        l.append(str(i))
        print("|".join(l))
    print(" ".join(num))

def coup_possible(hauteur, k):
    return k>=0 and k<m and hauteur[k]<n

def jouer(grille, hauteur, k, p):
    grille[n - 1 - hauteur[k]][k] = p
    hauteur[k]+=1

def victoire(grille, p):
    #A compléter
    return False

def PvP():
    grille = [[0 for _ in range(m)] for _ in range(n)]
    hauteur = [0 for _ in range(m)]
    joueur_courant = 1
    afficher_grille(grille)
    while True:
        k = int(input("Joueur "+f(joueur_courant)+", entrez votre coup :"))
        while not coup_possible(hauteur, k):
            print("coup non valide")
            k = int(input("Joueur "+f(joueur_courant)+", entrez votre coup :"))
        jouer(grille, hauteur, k, joueur_courant)
        afficher_grille(grille)
        if hauteur == [n]*m:
            print("match nul")
            return
        if victoire(grille, joueur_courant):
            print("le joueur ",f(joueur_courant), " a gagné la partie")
            return
        joueur_courant = 3 - joueur_courant

