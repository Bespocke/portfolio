#%%

import matplotlib.pyplot as plt

n = 6
m = 7


def f(x):
    if x==0: return " "
    elif x==1 : return "o"
    elif x==2 : return "x"

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
    #lignes
    for i in range(n):
        s = 0
        for j in range(m):
            if grille[i][j] == p:
                s += 1
                if s==4:return True
            else: s = 0
    #colonnes
    for j in range(m):
        s = 0
        for i in range(n):
            if grille[i][j] == p:
                s += 1
                if s==4:return True
            else: s = 0
    #diagonales croissantes
    for i in range(n):
        s = 0
        for k in range(min(n-i,m)):
            if grille[i+k][k] == p:
                s += 1
                if s==4:return True
            else: s = 0
    for j in range(1,m):
        s = 0
        for k in range(min(n,m-j)):
            if grille[k][j+k] == p:
                s += 1
                if s==4:return True
            else: s = 0
    #diagonales décroissantes
    for i in range(n):
        s = 0
        for k in range(i+1):
            if grille[i-k][k] == p:
                s += 1
                if s==4:return True
            else: s = 0
    for j in range(1,m):
        s = 0
        for k in range(min(n,m-j)):
            if grille[n-1-k][j+k] == p:
                s += 1
                if s==4:return True
            else: s = 0
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
            print("le joueur",f(joueur_courant), "a gagné la partie")
            return
        joueur_courant = 3 - joueur_courant



def IA1(grille, hauteur, p):
    k = 0
    while hauteur[k] == n: k += 1
    return k

def enlever_coup(grille, hauteur, k):
    hauteur[k]-=1
    grille[n - 1 - hauteur[k]][k] = 0

def eval(grille, hauteur, p):
    s = 0
    opp = 3-p
    def score(l):
        if opp not in l:
            x = l.count(p)
            if x == 4:
                print("gros bug")
                afficher_grille(grille)
            return x/(4 - x)
        elif p not in l:
            x = l.count(opp)
            if x == 4:
                print("gros bug")
                afficher_grille(grille)
            return -x/(4 - x)
        return 0
    for i in range(n):
        for j in range(m):
            l = grille[i][j:j+4]
            if len(l) == 4 :
                s += score(l)
            if i+4 <= n:
                l = [grille[i+k][j] for k in range(4)]
                s += score(l)
            if i+4 <= n and j+4 <= m:
                l = [grille[i+k][j+k] for k in range(4)]
                s += score(l)
            if i+4 <= n and j-3 >= 0:
                l = [grille[i+k][j-k] for k in range(4)]
                s += score(l)
    return s

def IA(grille, hauteur, p, prof):
    def noeud_max(prof2):
        if victoire(grille, 3-p):
            return -float("inf")
        if prof2 == 0:
            v = eval(grille, hauteur, p)
            return v
        vmax = -float("inf")
        for k in range(m):
            if coup_possible(hauteur, k):
                jouer(grille, hauteur, k, p)
                v = noeud_min(prof2 - 1)
                enlever_coup(grille, hauteur, k)
                if v > vmax:
                    vmax = v
        return vmax
    def noeud_min(prof2):
        if victoire(grille, p):
            return float("inf")
        if prof2 == 0:
            v = eval(grille, hauteur, p)
            return v
        vmin = float("inf")
        for k in range(m):
            if coup_possible(hauteur, k):
                jouer(grille, hauteur, k, 3-p)
                v = noeud_max(prof2 - 1)
                enlever_coup(grille, hauteur, k)
                if v < vmin:
                    vmin = v
        return vmin

    kmax = 0
    vmax = -float("inf")
    for k in range(m):
        if coup_possible(hauteur, k):
            jouer(grille, hauteur, k, p)
            v = noeud_min(prof - 1)
            enlever_coup(grille, hauteur, k)
            if v >= vmax:
                vmax = v
                kmax = k
    print("coup joué :", kmax, "score :", vmax)
    return kmax

def PvIA(prof):
    grille = [[0 for _ in range(m)] for _ in range(n)]
    hauteur = [0 for _ in range(m)]
    joueur_courant = 1
    afficher_grille(grille)
    while True:
        if joueur_courant == 2: k = IA(grille, hauteur, 6, prof)
        else:
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
            print("le joueur",f(joueur_courant), "a gagné la partie")
            return
        joueur_courant = 3 - joueur_courant

def IAvIA(IA1, IA2):
    grille = [[0 for _ in range(m)] for _ in range(n)]
    hauteur = [0 for _ in range(m)]
    joueur_courant = 1
    afficher_grille(grille)
    while True:
        if joueur_courant == 2: k = IA2(grille, hauteur, 2)
        else: k = IA1(grille, hauteur, 1)
        jouer(grille, hauteur, k, joueur_courant)
        afficher_grille(grille)
        if hauteur == [n]*m:
            print("match nul")
            return
        if victoire(grille, joueur_courant):
            print("le joueur",f(joueur_courant), "a gagné la partie")
            return
        joueur_courant = 3 - joueur_courant

def IA2(grille, hauteur, p):
    return IA(grille, hauteur, p, 2)

def IA3(grille, hauteur, p):
    return IA(grille, hauteur, p, 4)

def IA4(grille, hauteur, p):
    return IA(grille, hauteur, p, 6)

#%%