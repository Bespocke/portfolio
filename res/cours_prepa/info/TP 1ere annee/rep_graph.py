#G = [[0, 0, 1, 1], [0, 0, 1, 0], [1, 1, 0, 1], [1, 0, 1, 0]]

#G = [[0, [2,3]], [1,[3]], [2, [0, 3]],  [3, [0, 1, 2]]]

#G = {"Anne" : ["Dom", "Caro"], "Bob" : ["Dom"], "Caro" : ["Anne", "Dom"], "Dom" : ["Anne", "Caro", "Bob"]}

# exo 1

G1 = [[3, 1], [0, 2, 3], [1, 3], [0, 1, 2]]

def ajoute_sommet1(G):
    G.append([])

def ajoute_arete1(G, a):
    G[a[0]].append(a[1])
    G[a[1]].append(a[0])

def ordre1(G):
    return len(G)

def degre1(G,s):
    return len(G[s])

def regulier1(G):
    d = degre1(G,0)
    for i in range(1,len(G)):
        if degre1(G,i) != d:
            return False
    return True



# exo 2

M = [[0, 1, 0, 1], [1, 0, 1, 1], [0, 1, 0, 1], [1, 1, 1, 0]]

def nb_aretes2(M):
    nb = 0
    n = len(M)
    for i in range(n):
        for j in range(i+1,n):
            if M[i][j] == 1:
                nb = nb + 1
    return nb

def ajoute_sommet2(M):
    for ligne in M:
        ligne.append(0)
    ligne = [0 for i in range(len(M)+1)]
    M.append(ligne)

def ajoute_arete2(M,a):
    M[a[0]][a[1]] = 1
    M[a[1]][a[0]] = 1

def ordre2(M):
    return len(M)

def degre2(M,s):
    return sum(M[s])

def regulier2(M):
    d = degre2(0)
    for i in range(1, len(M)):
        if degre2(M,i) != d:
            return False
    return True

def aretes2(M):
    n = len(M)
    liste = []
    for i in range(n):
        for j in range(i+1, n):
            if M[i][j] == 1:
                liste.append([i, j])
    return liste

# exo 3

g = [[1, 3],[0, 2, 3],[1],[0, 1]]

m = [[0, 1, 0, 1], [1, 0, 1, 1], [0, 1, 0, 0],[1, 1, 0, 0]]

def conversion1(G):
    n = len(G)
    mat = [n * [0] for i in range(n)]
    for s in range(n):
        for voisin in G[s]:
            mat[s][voisin] = 1
    return mat

def conversion2(M):
    n = len(M)
    G = [[]]*n
    for i in range(n):
        G[i] = []
        for j in range(len(M[i])):
            if M[i][j] == 1:
                G[i].append(j)
    return G


# exo 4

G3 = { "Andre" : ["Bea", "Charles", "Estelle", "Fabrice"], "Bea" : ["Andre", "Charles", "Denise", "Heloise"], "Charles" : ["Andre", "Bea", "Denise", "Estelle", "Fabrice", "Gilbert"], "Denise" : ["Bea", "Charles", "Estelle"], "Estelle" : ["Andre", "Charles","Denise"], "Fabrice" : ["Andre", "Charles", "Gilbert"], "Gilbert" : ["Charles", "Fabrice"], "Heloise" : ["Bea"] }

def conversion3(g):
    sommets = {}
    n = 0
    for s in g:
        sommets[s] = n
        n = n+1
    mat = [n*[0] for i in range(n)]
    for s in sommets :
        for voisin in g[s]:
            mat[sommets[s]][sommets[voisin]] = 1
    return mat, sommets

def produit(M1, M2):
    n = len(M1)
    P = [n*[0] for i in range(n)]
    for i in range(n):
        for j in range(n):
            p = 0
            for k in range(n):
                p += M1[i][k]*M2[k][j]
            P[i][j] = p
    return P

def distance(M, i, j):
    Mp= M
    p=1
    while Mp[i][j] ==0:
        Mp = produit(Mp,M)
        p += 1
    return p

def diametre(M):
    n = len(M)
    max = 0
    for i in range(n):
        for j in range(n):
            d = distance(M, i, j)
            if d > max:
                max  = d
    return max

def distance_collab(g, nom1, nom2):
    m, s = conversion3(g)
    return distance(m, s[nom1], s[nom2])

def diametre_collab(g):
    m, s = conversion3(g)
    return diametre(m)

