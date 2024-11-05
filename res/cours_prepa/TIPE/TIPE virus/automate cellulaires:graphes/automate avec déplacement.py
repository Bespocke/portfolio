#%%

import random as rd
import matplotlib.pyplot as plt


def grille(n):
    return [[0 for _ in range(n)]for _ in range(n)]

def init(n,pop,inf):
    G = grille(n)
    for i in range(pop-inf):
        H = True
        while H:
            k,l = rd.randint(0,len(G)-1),rd.randint(0,len(G)-1)
            if G[k][l]== 0:
                G[k][l] = 1
                H = False
    for i in range(inf):
        H = True
        while H:
            k,l = rd.randint(0,len(G)-1),rd.randint(0,len(G)-1)
            if G[k][l]==0:
                G[k][l] = 2
                H = False
    return G


nombre_de_jour_infecte = 8

sommets_habites = set(range(1, nombre_de_jour_infecte +3))
sommets_infectes = set(range(2,nombre_de_jour_infecte+2))

def est_mort(G,i,j):
    return G[i][j] == nombre_de_jour_infecte +3

def est_sain(G,i,j):
    return G[i][j] == 1


def est_infecte(G,i,j):
    return G[i][j] in sommets_infectes

def compte(G):
    L = [0]*(nombre_de_jour_infecte+4)
    for s in G:
        for k in s:
            L[k] += 1
    return L

def est_exposee(G,i,j):
    n = len(G)
    if i==j==0:
        if est_infecte(G,0,1) or est_infecte(G,1,1) or est_infecte(G,1,0):
            return True
    elif i == 0 and j == n-1:
        if est_infecte(G,0,n-2) or est_infecte(G,1,n-2) or est_infecte(G,1,n-1):
            return True
    elif i == n-1 and j == 0:
        if est_infecte(G,n-1,1) or est_infecte(G,n-2,1) or est_infecte(G,n-2,0):
            return True
    elif i ==j==n-1:
        if est_infecte(G,n-1,n-2) or est_infecte(G,n-2,n-2) or est_infecte(G,n-2,n-1):
            return True
    elif i == 0 and 1<=j<=n-2:
        if est_infecte(G,0,j-1) or est_infecte(G,0,j+1) or est_infecte(G,1,j-1) or est_infecte(G,1,j) or est_infecte(G,1,j+1):
            return True
    elif i == n-1 and 1<=j<=n-2:
        if est_infecte(G,n-1,j-1) or est_infecte(G,n-1,j+1) or est_infecte(G,n-2,j-1) or est_infecte(G,n-2,j) or est_infecte(G,n-2,j+1):
            return True
    elif j == 0 and 1<=i<=n-2:
        if est_infecte(G,i-1,0) or est_infecte(G,i+1,0) or est_infecte(G,i-1,1) or est_infecte(G,i,1) or est_infecte(G,i+1,1):
            return True
    elif j == n-1 and 1<=i<=n-2:
        if est_infecte(G,i-1,n-1) or est_infecte(G,i+1,n-1) or est_infecte(G,i-1,n-2) or est_infecte(G,i,n-2) or est_infecte(G,i+1,n-2):
            return True
    else:
        if est_infecte(G,i-1,j-1) or est_infecte(G,i-1,j) or est_infecte(G,i-1,j+1) or est_infecte(G,i,j-1) or est_infecte(G,i,j+1) or est_infecte(G,i+1,j-1) or est_infecte(G,i+1,j) or est_infecte(G,i+1,j+1):
            return True
    return False

def bernoulli(p):
    if rd.random() <= p:
        return 1
    return 0

### les différents types de déplacement

def deplacement_aleatoire_2D(graphe):
    largeur_du_graphe = len(graphe[0])
    hauteur_du_graphe = len(graphe)


    for i in range(hauteur_du_graphe):
        for j in range(largeur_du_graphe):
            sommet = graphe[i][j]

            if sommet in sommets_habites:
                x, y = j, i  # Coordonnées du sommet

                # Déplacement aléatoire
                dx = rd.randint(-1, 1)
                dy = rd.randint(-1, 1)

                # Nouvelles coordonnées potentielles du sommet
                nouveau_x = x + dx
                nouveau_y = y + dy

                # Vérification des limites du graphe
                if nouveau_x >= 0 and nouveau_x < largeur_du_graphe and nouveau_y >= 0 and nouveau_y < hauteur_du_graphe:
                    destination = graphe[nouveau_y][nouveau_x]

                    # Vérification si la destination est une case vide (numérotée 0)
                    if destination == 0:
                        graphe[i][j] = 0  # Le sommet actuel quitte sa case
                        graphe[nouveau_y][nouveau_x] = sommet  # Le sommet se déplace vers la case vide



def deplacement_unique1D(graphe):
    largeur_du_graphe = len(graphe[0])
    hauteur_du_graphe = len(graphe)

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Haut, bas, gauche, droite

    for i in range(hauteur_du_graphe):
        for j in range(largeur_du_graphe):
            sommet = graphe[i][j]

            if sommet in sommets_habites:
                x, y = j, i  # Coordonnées du sommet

                # Mélange aléatoire des directions
                rd.shuffle(directions)

                # Recherche de la première direction valide pour le déplacement
                for dx, dy in directions:
                    nouveau_x = x + dx
                    nouveau_y = y + dy

                    # Vérification des limites du graphe
                    if nouveau_x >= 0 and nouveau_x < largeur_du_graphe and nouveau_y >= 0 and nouveau_y < hauteur_du_graphe:
                        destination = graphe[nouveau_y][nouveau_x]

                        # Vérification si la destination est une case vide (numérotée 0)
                        if destination == 0:
                            graphe[i][j] = 0  # Le sommet actuel quitte sa case
                            graphe[nouveau_y][nouveau_x] = sommet  # Le sommet se déplace vers la case vide
                            break





def deplacement_translation_proche(graphe):
    largeur_du_graphe = len(graphe[0])
    hauteur_du_graphe = len(graphe)

    cases_vides = []

    for i in range(hauteur_du_graphe):
        for j in range(largeur_du_graphe):
            sommet = graphe[i][j]

            if sommet == 0:
                cases_vides.append((j, i))  # Coordonnées de la case vide

    rd.shuffle(cases_vides)  # Mélange aléatoire des cases vides

    for i in range(hauteur_du_graphe):
        for j in range(largeur_du_graphe):
            sommet = graphe[i][j]

            if sommet in sommets_habites:
                x, y = j, i  # Coordonnées du sommet

                # Recherche de la première case vide aléatoire
                for nouveau_x, nouveau_y in cases_vides:
                    # Calcul de la distance de déplacement
                    distance = abs(nouveau_x - x) + abs(nouveau_y - y)

                    # Déplacement si la distance est inférieure ou égale à 1
                    if distance <= 3:
                        graphe[i][j] = 0  # Le sommet actuel quitte sa case
                        graphe[nouveau_y][nouveau_x] = sommet  # Le sommet se déplace vers la case vide
                        break



def deplacement_teleportation(graphe):
    largeur_du_graphe = len(graphe[0])
    hauteur_du_graphe = len(graphe)

    sommets_a_deplacer = []

    for i in range(hauteur_du_graphe):
        for j in range(largeur_du_graphe):
            sommet = graphe[i][j]

            if sommet in sommets_habites:
                sommets_a_deplacer.append((j, i))  # Coordonnées des sommets à déplacer

    rd.shuffle(sommets_a_deplacer)

    for x, y in sommets_a_deplacer:
        destination_trouvee = False

        while not destination_trouvee:
            nouvelle_x = rd.randint(0, largeur_du_graphe-1)
            nouvelle_y = rd.randint(0, hauteur_du_graphe-1)

            if graphe[nouvelle_y][nouvelle_x] == 0:
                graphe[nouvelle_y][nouvelle_x] = graphe[y][x]
                graphe[y][x] = 0
                destination_trouvee = True

deplacements =[deplacement_unique1D,
               deplacement_aleatoire_2D,
               deplacement_translation_proche,
               deplacement_teleportation]

### fin des différents types de déplacement

from copy import deepcopy

#calcule la genération suivante
def suivant(G,p1,p2):
    n = len(G)
    G_suivant = deepcopy(G)
    for i in range(n):
        for j in range(n):
            if est_sain(G,i,j) and est_exposee(G,i,j) and bernoulli(p2)==1:
                G_suivant[i][j] = 2
            elif est_infecte(G,i,j):
                if bernoulli(p1) == 1:
                    G_suivant[i][j] = nombre_de_jour_infecte +3
                else:
                    G_suivant[i][j] = G[i][j] +1
            elif est_mort(G,i,j):
                G_suivant[i][j] = 0
    return G_suivant





import matplotlib.colors

custom_cmap = matplotlib.colors.ListedColormap(["white","forestgreen","khaki","gold","orange","darkorange","tomato","orangered","red","lightskyblue","black"])
bounds = [0,1,2,3,4,5,6,7,8,9,10,11]
norms = matplotlib.colors.BoundaryNorm(bounds,custom_cmap.N)


##differentes simulations

'''1ere simualtion, avec affichage pour verifier si le programme fonctionne correctement'''

def simulation_avec_affichage(n,mouvement_pop,pop,inf0,p1,p2):
    # initialisation du graphe
    G = init(n,pop,inf0)
    C = compte(G)
    infect = inf0
    i = 0


    #initialisiation des listes
    S,I,R,M,T,POPULATION = [C[1]], [infect],[C[9]],[C[10]], [i], [pop]


    while infect != 0:    # on continue la simulation tant qu'il reste des infectés
        i += 1


        # on propage le virus a partir du modèle SIRM
        G = suivant(G,p1,p2)


        # on fait se déplacer la population de la maniere que l'on veut
        mouvement_pop(G)

        # on met a jour les listes
        C = compte(G)
        infect = C[2]+C[3]+C[4]+C[5]+C[6]+C[7]+C[8]
        S.append(C[1])
        I.append(infect)
        R.append(C[9])
        M.append(M[-1] + C[10])
        POPULATION.append(pop - M[-1])
        T.append(i)

    # on met a jour une dernierre fois pour afficher la derniere generation
    G = suivant(G,p1,p2)
    mouvement_pop(G)

    return S,I,R,M,T,POPULATION

'''2e simulation, sans affichage pour effectuer les mesures'''

def simulation_sans_affichage(n,mouvement_pop,pop,inf0,p1,p2):
    # initialisation du graphe
    G = init(n,pop,inf0)
    C = compte(G)
    infect = inf0


    #initialisiation des listes
    M = [C[-1] ]

    while infect != 0:    # on continue la simulation tant qu'il reste des infectés


        # on propage le virus a partir du modèle SIRM
        G = suivant(G,p1,p2)


        # on fait se déplacer la population de la maniere que l'on veut
        mouvement_pop(G)


        # on met a jour les listes
        C = compte(G)
        infect = C[2]+C[3]+C[4]+C[5]+C[6]
        M.append(M[-1] + C[10])

    # on met a jour une dernierre fois pour afficher la derniere generation
    G = suivant(G,p1,p2)
    mouvement_pop(G)
    L= compte(G)
    for i in range(len(L)):
        L[i] = L[i] / (pop)
    L[-1] = M[-1]/pop
    return L

### fin des simulations
n = 20
pop =120
inf0 = 10
p1 = 0.4 # nombre de morts sur nombre total de contaminés du covid dans le monde
p2 = 0.9
mouvement_pop = deplacement_translation_proche

def valeur_courbe(n,mouvement_pop,p1):
    L,M = [],[]
    for i in range(101):
        u = i/100
        K = simulation_avec_affichage(n,mouvement_pop,pop,inf0,p1,u)
        compteur = K[-2] +K[-1]
        M.append(compteur)
        L.append(u)
    return L,M

# L,M = valeur_courbe(n,mouvement_pop,p1)

def seuil(Lp2,Lxa):
    for i in range(len(Lp2)):
        if Lxa[i] >= 0.5:
            return [Lp2[i-1],Lp2[i]]

# print(seuil(L,M))
#
# plt.close()
# plt.plot(L,M)
# plt.show()

def continu(n):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simulation_avec_affichage(n,deplacement_aleatoire_2D,pop,inf0,p/100,p/100)
            M_updated[p][q] = max(I)*100/n
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)

def a(n):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simulation_avec_affichage(n,deplacement_aleatoire_2D,pop,inf0,p/100,p/100)
            if (R[-1]+M[-1]) >= 70 * popl[0] / 100:
                M_updated[p][q] = 1
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)

def t(n):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simulation_avec_affichage(n,deplacement_aleatoire_2D,pop,inf0,p/100,p/100)
            M_updated[p][q] = T[-1]
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)

t(n)

S,I,R,M,T,POPULATION = simulation_avec_affichage(n,deplacement_aleatoire_2D,pop,inf0,p1,p2)

plt.plot(T,S)
plt.plot(T,I)
plt.plot(T,R)
plt.plot(T,M)
plt.title("Automate avec déplacement")
plt.xlabel('Temps / jours')
plt.ylabel('Population')
plt.legend(["saine","infecte_total ","retabli","mort"])
plt.show()


for f in deplacements:
    L,M = valeur_courbe(n,f,p1)
    print(seuil(L,M))





import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import random as rd
import numpy as np

def afficher(M):
    M = np.array(M)
    
    cmap = ListedColormap(["white", "forestgreen", "lemonchiffon", "yellow", "orange", "darkorange",
                           "orangered", "red", "firebrick", "darkred", "blue", "black"])
    bounds = np.arange(13) - 0.5
    norm = BoundaryNorm(bounds, cmap.N)

    plt.imshow(M, cmap=cmap, norm=norm)
    plt.colorbar(ticks=np.arange(12), boundaries=bounds)
    plt.show()

def mouvement(M):
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j]!=0:
                dx,dy=rd.randint(-1,1),rd.randint(-1,1)
                if i+dy<=len(M)-1 and i+dy>=0 and M[i+dy][j]==0:
                    M[i+dy][j]=M[i][j]
                    M[i][j]=0
                    if j+dx<=len(M)-1 and j+dx>=0 and M[i+dy][j+dx]==0:
                        M[i+dy][j+dx]=M[i+dy][j]
                        M[i+dy][j]=0
                elif j+dx<=len(M)-1 and j+dx>=0 and M[i][j+dx]==0:
                    M[i][j+dx]=M[i][j]
                    M[i][j]=0
                    if i+dy<=len(M)-1 and i+dy>=0 and M[i+dy][j+dx]==0:
                        M[i+dy][j+dx]=M[i][j+dx]
                        M[i][j+dx]=0
    return(M)

def generer(n):
    M = [[0] * n for _ in range(n)]
    for i in range(1, 12):
        continuer = True
        while continuer:
            x,y = rd.randint(0,len(M)-1),rd.randint(0,len(M)-1)
            if M[x][y] == 0:
                M[x][y] = i
                continuer = False
    return(M)



#%%