

#%%
text1=["si","six","scies","scient","six","cypres","six","cents","scies","scient","six","cents","cypres"]
T=["si","six","scies","scient","cypres","cents","0","1","2","3","1","4","1","5","2","3","1","5","4"]
D={"si":0,"six":1,"scies":2,"scient":3,"cypres":4,"cents":5}

def numerotation2(texte):
    T=[]
    D={}
    j=0
    for i in texte:
        if not i in D:
            D[i]=j
            T.append(i)
            j+=1
    T.append('FINDETEXTE\n')
    for i in texte:
        T.append(str(D[i]))
    return T,D

def numerotation(texte):
    T=[]
    D=creer_dico(100)
    j=0
    for i in texte:
        if not cle_presente(D,i):
            ajouter(D,i,j)
            T.append(i)
            j+=1
    T.append('FINDETEXTE\n')
    for i in texte:
        print(valeur_associee(D,i))
        T.append(str(valeur_associee(D,i)))
    return T,D






            
def phrase(phrase):
    t=phrase[0]
    for i in phrase[1:]:
        t+=" "+ i
    return t

def compresser(nom_ouvrir,nom_creer):
    t=open(nom_ouvrir,'r')
    r=t.readlines()
    texte1=[ligne.strip() + ' indentation' for ligne in r]
    texte2=[]
    for i in texte1:
        texte2+=i.split(' ')
    T,_=numerotation(texte2)
    ph=''
    for i in T:
        ph+=i+' '
    c=open(nom_creer,'w')
    c.write(ph)
    t.close()
    c.close()

def decompresser(nom_ouvrir,nom_creer):
    t=open(nom_ouvrir,'r')
    r=t.readlines()
    texte1=[ligne.strip() for ligne in r]
    texte2=[]
    for i in texte1:
        texte2+=i.split(' ')
    i=0
    k=-1
    while texte2[i]!='FINDETEXTE':
        if texte2[i]=='indentation':
            k=i
        i+=1
    l=texte2[0:i]
    q=texte2[i+1:]
    ph=''
    for j in q:
        if j=='\n':
            ph+='\n'
        elif int(j)==k:
            ph+='\n'
        else:
            ph+= l[int(j)] + ' '
    c=open(nom_creer,'w')
    c.write(ph)
    t.close()
    c.close()

def hash(mot,n):
    res=0
    for i in mot:
        res+=ord(i)
    return res%n

def creer_dico(n):
    return [[] for i in range(n) ]

def cle_presente(D,cle):
    for (c,v) in D[hash(cle,len(D))]:
        if c==cle:
            return True
    return False

def ajouter(D,cle,valeur):
    D[hash(cle,len(D))].append((cle,valeur))

def valeur_associee(D,cle):
    for (c,v) in D[hash(cle,len(D))]:
        if c == cle:
            return v

def modifier_valeur(D,cle,valeur):
    for i in range(D[hash(cle,len(D))]):
        c,v = D[hash(cle,len(D))][i]
        if c == cle:
            D[hash(cle,len(D))][i]=(c,valeur)

def modifier_valeur(D,cle,valeur):
    for i in range(len(D[hash(cle,len(D))])):
        c,v = D[hash(cle,len(D))][i]
        if c == cle:
            D[hash(cle,len(D))][i]=(c,valeur)



def supprimer_valeur(D,cle):
    for i in range(len(D[hash(cle,len(D))])):
        c,v = D[hash(cle,len(D))][i]
        if c == cle:
             D[hash(cle,len(D))].pop(i)



        
#%%