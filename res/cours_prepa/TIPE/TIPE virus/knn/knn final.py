#%%

import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import copy
import random as rd

def generer(n):
    return [[0] * n for _ in range(n)]

def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def liste_voisins(M, p, k):
    def f(L):
        return L[0]

    a, b = p
    D = []
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] != 0 and not (a,b)==(i,j):
                p2 = (i, j)
                D.append((distance(p, p2), (i, j)))

    return sorted(D, key=f)[:int(k)]

# def liste_voisins(M, coord, k):
#     voisins = []
#     n = len(M)
#     x, y = coord
    
#     # Coordonnées des voisins dans un carré de taille k x k
#     for i in range(max(0, x-k), min(n, x+k+1)):
#         for j in range(max(0, y-k), min(n, y+k+1)):
#             if (i, j) != (x, y):
#                 voisins.append((i, j))
    
#     return voisins

def etiquette_maj(M, V):
    D = {}
    for (_, e) in V:
        x, y = e
        if M[x][y] not in D:
            D[M[x][y]] = 1
        else:
            D[M[x][y]] += 1
    e_maj = None
    M_max = 0
    for e in D:
        if D[e] > M_max:
            e_maj = e
            M_max = D[e]
    return e_maj

def bernoulli(pb):
    if random.random() <= pb:
        return 1
    return 0

def init(n, v, l):
    M = generer(n)
    for _ in range(v):
        a, b = random.randint(0, n - 1), random.randint(0, n - 1)
        M[a][b] = 1
    for _ in range(l):
        r, s = random.randint(0, n - 1), random.randint(0, n - 1)
        M[r][s] = 2
    return M

# def propagation_epidemie(M, k, pr, pm):
#     M2 = [row[:] for row in M]  # Copy the matrix

#     for i in range(len(M)):
#         for j in range(len(M)):
#             if M[i][j] == 2:  # Infected cell
#                 if bernoulli(pm) == 1:  # Probability of dying
#                     M2[i][j] = 4  # Cell dies
#                 elif bernoulli(pr) == 1:  # Probability of recovery
#                     M2[i][j] = 3  # Cell recovers
#             elif M[i][j] == 1:  # Healthy cell
#                 voisins = liste_voisins(M, (i, j), k)
#                 if etiquette_maj(M, voisins) == 2:  # Majority label is infected
#                     M2[i][j] = 2  # Cell gets infected

#     return M2

# def propagation_epidemie(M, k, pr, pm):
#     M2 = copy.deepcopy(M)  # Copy the matrix

#     for i in range(len(M)):
#         for j in range(len(M)):
#             if M[i][j] == 2:  # Infected cell
#                 if bernoulli(pm) == 1:  # Probability of dying
#                     M2[i][j] = 4  # Cell dies
#                 elif bernoulli(pr) == 1:  # Probability of recovery
#                     M2[i][j] = 3  # Cell recovers
#             elif M[i][j] == 1:  # Healthy cell
#                 voisins = liste_voisins(M, (i, j), k)
#                 if etiquette_maj(M, voisins) == 2:  # Majority label is infected
#                     M2[i][j] = 2  # Cell gets infected

#     return M2

def propagation_epidemie(M, k, pr, pm):
    M2 = [row[:] for row in M]  # Copie temporaire de la matrice

    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] == 2:  # Cellule infectée
                if bernoulli(pm) == 1:  # Probabilité de décès
                    M2[i][j] = 4  # La cellule meurt
                elif bernoulli(pr) == 1:  # Probabilité de guérison
                    M2[i][j] = 3  # La cellule guérit

    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] == 1:  # Cellule saine
                voisins = liste_voisins(M, (i, j), k)
                e=etiquette_maj(M, voisins)
                if e==2:  # La majorité des voisins sont infectés
                    M2[i][j] = 2  # La cellule devient infectée

    return M2



# def afficher(M):
#     plt.imshow(M)
#     plt.show()
#
# def simulation(n, k, pr, pm, iterations):
#     M = init(n, k)
#     continuer=True
#
#     while continuer==True:
#         M = propagation_epidemie(M, k, pr, pm)
#         afficher(M)
#
#
# def afficher_matrice(M):
#     for row in M:
#         print(' '.join(str(cell) for cell in row))

def afficher(M):
    cmap = ListedColormap(['white', 'green', 'red', 'blue', 'black'])
    bounds = [0, 1, 2, 3, 4, 5]
    norm = BoundaryNorm(bounds, cmap.N)
    plt.imshow(M, cmap=cmap, norm=norm)
    plt.colorbar(ticks=[0, 1, 2, 3, 4], boundaries=bounds)
    plt.show()

def afficher2(M):
    plt.imshow(M)
    plt.show()
    
def compte(M):
    occurences = {
        1: 0,  # Cellule saine
        2: 0,  # Cellule infectée
        3: 0,  # Cellule guérie
        4: 0   # Cellule décédée
    }

    for row in M:
        for cell in row:
            if cell in occurences:
                occurences[cell] += 1

    return occurences

# def simulation(n, v, l, k, pr, pm):
#     M = init(n, v, l)
#     D = compte(M)
#     t = 0
#     p=D[1]+D[2]
#     S, I, R, Mo, T, popl = [D[1]], [D[2]], [D[3]], [D[4]], [t], [D[1]+D[2]]
#     continuer = True

#     while continuer:
#         t += 1
#         M = propagation_epidemie(M, k, pr, pm)
#         D = compte(M)
#         S.append(D[1])
#         I.append(D[2] + D[3] + D[4])
#         R.append(D[3])
#         Mo.append(D[4])
#         T.append(t)
#         popl.append( p- D[4])
#         plt.pause(0.1)
#         plt.clf()
#         afficher(M)

#         # Vérifier s'il reste des individus infectés
#         infectes = sum(row.count(2) for row in M)
#         if infectes == 0:
#             continuer = False
#     plt.close()
#     plt.plot(T,S)
#     plt.plot(T,I)
#     plt.plot(T,R)
#     plt.plot(T,Mo)
#     plt.plot(T,popl)
#     plt.legend(["saine","infecte_total ","retabli","mort",'population'])
#     plt.show()
#     return S, I, R, Mo, T, popl

def simulation(n, v, l, k, pr, pm):
    M = init(n, v, l)
    D = compte(M)
    t = 0
    S, I, R, Mo, T, popl = [D[1]], [D[2]], [D[3]], [D[4]], [t], [D[1]+D[2]]
    popi=D[1]+D[2]
    continuer = True
    occurrences_sans_modification = 0  # Compteur d'occurrences sans modification
    derniere_occurrence = None  # Dernière configuration de la matrice

    while continuer:
        t += 1
        M = propagation_epidemie(M, k, pr, pm)
        D = compte(M)
        S.append(D[1])
        I.append(D[2] )
        R.append(D[3])
        Mo.append(D[4])
        T.append(t)
        popl.append(popi - D[4])
        plt.pause(0.1)
        plt.clf()


        # Vérifier s'il reste des individus infectés
        infectes = sum(row.count(2) for row in M)

        if M == derniere_occurrence:
            occurrences_sans_modification += 1
        else:
            occurrences_sans_modification = 0

            derniere_occurrence = M

        if infectes == 0 or occurrences_sans_modification >= 5:
        # Vérifier si la configuration de la matrice a changé
        # Vérifier si le nombre d'occurrences sans modification atteint 5
            continuer = False

    plt.close()
    plt.plot(T, S)
    plt.plot(T, I)
    plt.plot(T, R)
    plt.plot(T, Mo)
    plt.legend(["Saine", "Infecté", "Rétabli", "Mort"])
    plt.title("voisin proche")
    plt.show()
    return S, I, R, Mo, T, popl

def simulation2(n, v, l, k, pr, pm):
    M = init(n, v, l)
    D = compte(M)
    t = 0
    S, I, R, Mo, T, popl = [D[1]], [D[2]], [D[3]], [D[4]], [t], [D[1]+D[2]]
    popi=D[1]+D[2]
    continuer = True
    occurrences_sans_modification = 0  # Compteur d'occurrences sans modification
    derniere_occurrence = None  # Dernière configuration de la matrice

    while continuer:
        t += 1
        M = propagation_epidemie(M, k, pr, pm)
        D = compte(M)
        S.append(D[1])
        I.append(D[2] + D[3] + D[4])
        R.append(D[3])
        Mo.append(D[4])
        T.append(t)
        popl.append(popi - D[4])

        # Vérifier s'il reste des individus infectés
        infectes = sum(row.count(2) for row in M)

        if M == derniere_occurrence:
            occurrences_sans_modification += 1
        else:
            occurrences_sans_modification = 0

            derniere_occurrence = M

        if infectes == 0 or occurrences_sans_modification >= 5:
        # Vérifier si la configuration de la matrice a changé
        # Vérifier si le nombre d'occurrences sans modification atteint 5
            continuer = False
    return S, I, R, Mo, T, popl


def a(n, v, l, k):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simulation2(n, v, l, k, p/100, q/100)
            if R[-1]+M[-1] >= 90 * popl[0] / 100:
                M_updated[p][q] = 1
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)

def ac(n, v, l, k):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simulation2(n, v, l, k, p/100, q/100)
            M_updated[p][q] = max(I)*100/(v+l)
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)

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

def eliminer_mort(M):
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j]==4:
                M[i][j]=0
    return(M)

def simulation_mouvement(n, v, l, k, pr, pm):
    M = init(n, v, l)
    D = compte(M)
    t = 0
    mort=D[4]
    S, I, R, Mo, T, popl = [D[1]], [D[2]], [D[3]], [D[4]], [t], [D[1]+D[2]]
    popi=D[1]+D[2]
    continuer = True
    occurrences_sans_modification = 0  # Compteur d'occurrences sans modification
    derniere_occurrence = None  # Dernière configuration de la matrice

    while continuer:
        print(t)
        t += 1
        M=mouvement(M)
        M = propagation_epidemie(M, k, pr, pm)
        D = compte(M)
        mort+=D[4]
        M=eliminer_mort(M)
        S.append(D[1])
        I.append(D[2])
        R.append(D[3])
        Mo.append(mort)
        T.append(t)
        popl.append(popi - mort)
        plt.pause(0.01)
        plt.clf()

        if derniere_occurrence is not None:
            if D == derniere_occurrence:
                occurrences_sans_modification += 1
            else:
                occurrences_sans_modification = 0
        derniere_occurrence = D.copy()
        if occurrences_sans_modification >= 5:
        # Vérifier si toutes les occurrences sont identiques
            if (occurrences_sans_modification == 5 and
                    S[-1] == S[-2] == S[-3] == S[-4] == S[-5] and
                    I[-1] == I[-2] == I[-3] == I[-4] == I[-5] and
                    R[-1] == R[-2] == R[-3] == R[-4] == R[-5] and
                    Mo[-1] == Mo[-2] == Mo[-3] == Mo[-4] == Mo[-5]):
                continuer = False
    plt.close()
    plt.plot(T, S)
    plt.plot(T, I)
    plt.plot(T, R)
    plt.plot(T, Mo)
    plt.legend(["Saine", "Infecté total", "Rétabli", "Mort"])
    plt.title("voisin proche avec mouvement")
    plt.show()
    return S, I, R, Mo, T, popl

def simulation_mouvement2(n, v, l, k, pr, pm):
    M = init(n, v, l)
    D = compte(M)
    t = 0
    mort=D[4]
    S, I, R, Mo, T, popl = [D[1]], [D[2]], [D[3]], [D[4]], [t], [D[1]+D[2]]
    popi=D[1]+D[2]
    continuer = True
    occurrences_sans_modification = 0  # Compteur d'occurrences sans modification
    derniere_occurrence = None  # Dernière configuration de la matrice

    while continuer:
        t += 1
        M=mouvement(M)
        M = propagation_epidemie(M, k, pr, pm)
        D = compte(M)
        mort+=D[4]
        M=eliminer_mort(M)
        S.append(D[1])
        I.append(D[2] + D[3] + D[4])
        R.append(D[3])
        Mo.append(mort)
        T.append(t)
        popl.append(popi - mort)
        
        if derniere_occurrence is not None:
            if D == derniere_occurrence:
                occurrences_sans_modification += 1
            else:
                occurrences_sans_modification = 0
        derniere_occurrence = D.copy()
        if occurrences_sans_modification >= 5:
        # Vérifier si toutes les occurrences sont identiques
            if (occurrences_sans_modification == 5 and
                    S[-1] == S[-2] == S[-3] == S[-4] == S[-5] and
                    I[-1] == I[-2] == I[-3] == I[-4] == I[-5] and
                    R[-1] == R[-2] == R[-3] == R[-4] == R[-5] and
                    Mo[-1] == Mo[-2] == Mo[-3] == Mo[-4] == Mo[-5]):
                continuer = False
        

    return S, I, R, Mo, T, popl

def a2(n, v, l, k):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simulation_mouvement2(n, v, l, k, p/400, q/400)
            if (R[-1]+M[-1]) >= 70 * popl[0] / 100:
                M_updated[p][q] = 1
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)

def ac2(n, v, l, k):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simulation_mouvement2(n, v, l, k, p/400, q/400)
            M_updated[p][q] = max(I)*100/(v+l)
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)

simulation(60, 2500, 300, 1, 0.6, 0.3)

#%%