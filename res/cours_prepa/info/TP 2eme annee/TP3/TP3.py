#Compression

def numerotation(L):
    D = {}
    T= []
    n = 0
    for x in L:
        if x not in D:
            D[x] = n
            n = n+1
            T.append(x)
    return T,D

def phrase(L):
    if L==[]:
        return ""
    p = L[0]
    for i in range(1,len(L)):
        p = p+' '
        p = p+L[i]
    return p



def compresser(nom_source, nom_comp):
    fichier_source = open(nom_source,'r')
    L = []
    for ligne in fichier_source.readlines():
        ligne = ligne.strip()
        L += ligne.split(' ')
    fichier_source.close()
    T,D = numerotation(L)
    fichier_comp = open(nom_comp, 'w')
    fichier_comp.write(phrase(T))
    fichier_comp.write("\n")
    fichier_source = open(nom_source,'r')
    for ligne in fichier_source.readlines():
        ligne = ligne.strip()
        fichier_comp.write(phrase([str(D[mot]) for mot in ligne.split(' ')]))
        fichier_comp.write('\n')
    fichier_comp.close()
    fichier_source.close()

def decompresser(nom_comp, nom_dec):
    fichier_comp = open(nom_comp, 'r')
    T =  fichier_comp.readline().strip().split(' ')
    fichier_dec = open(nom_dec, 'w')
    for ligne in fichier_comp.readlines():
        ligne = ligne.strip()
        L = ligne.split(' ')
        L_dec = [T[int(num)] for num in L]
        fichier_dec.write(phrase(L_dec))
        fichier_dec.write('\n')
    fichier_comp.close()
    fichier_dec.close()


#Table de hachage


def hash(ch,n):
    h = 0
    for c in ch:
        h += ord(c)
    return h%n

def hash(ch,n):
    h = 0
    p = 1
    for c in ch:
        h = (h + ord(c)*p)%n
        p = p * 101
    return h

def hash(ch,n):
    h = 0
    for c in ch:
        h += ord(c)
    return h%n

def creer_dico(n):
    D = [[] for _ in range(n)]
    return D

def cle_presente(D,cle):
    n = len(D)
    h = hash(cle,n)
    for (x,y) in D[h]:
        if x==cle:
            return True
    return False

def ajouter(D,cle,valeur):
    n = len(D)
    h = hash(cle,n)
    D[h].append([cle,valeur])

def valeur_associee(D,cle):
    n = len(D)
    h = hash(cle,n)
    for (x,y) in D[h]:
        if x==cle:
            return y

def modifier_valeur(D,cle,valeur):
    n = len(D)
    h = hash(cle,n)
    for i in range(len(T[h])):
        if cle==D[h][i][0]:
            D[h][i][1] = valeur
            return

def supprimer(D,cle):
    n = len(D)
    h = hash(cle,n)
    for i in range(len(T[h])):
        if cle==D[h][i][0]:
            D[h].pop(i)
            return



#Compression avec l'implémentation maison

def numerotation(L):
    D = creer_dico(len(L))
    T= []
    n = 0
    for x in L:
        if not cle_presente(D,x):
            ajouter(D,x,n)
            n = n+1
            T.append(x)
    return T,D


def compresser(nom_source, nom_comp):
    fichier_source = open(nom_source,'r')
    L = []
    for ligne in fichier_source.readlines():
        ligne = ligne.strip()
        L += ligne.split(' ')
    fichier_source.close()
    T,D = numerotation(L)
    fichier_comp = open(nom_comp, 'w')
    fichier_comp.write(phrase(T))
    fichier_comp.write("\n")
    fichier_source = open(nom_source,'r')
    for ligne in fichier_source.readlines():
        ligne = ligne.strip()
        fichier_comp.write(phrase([str(valeur_associee(D,mot)) for mot in ligne.split(' ')]))
        fichier_comp.write('\n')
    fichier_comp.close()
    fichier_source.close()

def decompresser(nom_comp, nom_dec):
    fichier_comp = open(nom_comp, 'r')
    T =  fichier_comp.readline().strip().split(' ')
    fichier_dec = open(nom_dec, 'w')
    for ligne in fichier_comp.readlines():
        ligne = ligne.strip()
        L = ligne.split(' ')
        L_dec = [T[int(num)] for num in L]
        fichier_dec.write(phrase(L_dec))
        fichier_dec.write('\n')
    fichier_comp.close()
    fichier_dec.close()


def f_collisions(D):
    n = 0
    d = 0
    for L in D:
        if len(L)>1:
            n+=len(L)
        d+=len(L)
    return n/d


def dico_texte(nom_source):
    fichier_source = open(nom_source,'r')
    L = []
    for ligne in fichier_source.readlines():
        ligne = ligne.strip()
        L += ligne.split(' ')
    fichier_source.close()
    T,D = numerotation(L)
    return D
