#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 20:52:19 2023

@author: a.
"""

#%%

import copy
import math
import random as rd
import matplotlib.pyplot as plt

def distance(p,z):
    x,y=z
    a,b=p
    return math.sqrt((x-a)**2+(y-b)**2)

def generer(n):
    return [[0 for _ in range(n)] for _ in range(n)]

# def generer(n):
#     return [[(0,0) for i in range(n)]for i in range(n)]

def init(n,k):
    M=generer(n)
    for i in range(1,k+1):
        a,b=rd.randint(0,len(M)-1),rd.randint(0,len(M)-1)
        M[a][b]=1
    r,s=rd.randint(0,len(M)-1),rd.randint(0,len(M)-1)
    M[r][s]=2       
    return M
    
def init2(n,k,l):
    M=generer(n)
    for i in range(1,k+1):
        a,b=rd.randint(0,len(M)-1),rd.randint(0,len(M)-1)
        M[a][b]=1
    for i in range(l):
        r,s=rd.randint(0,len(M)-1),rd.randint(0,len(M)-1)
        M[r][s]=2       
    return M
    
M=init2(20,20,1)

# def init(M,k):
#     for i in range(1,k+1):
#         a,b=rd.randint(0,len(M)-1),rd.randint(0,len(M)-1)
#         M[a][b]=(i,1)
#     r,s=rd.randint(0,len(M)-1),rd.randint(0,len(M)-1)
#     M[r][s]=(k+2,2)       
#     return M
        
def mouvement(M):
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] != 0:
                dx, dy = rd.choice([-1, 0, 1]), rd.choice([-1, 0, 1])
                if i + dy <= len(M) - 1 and i + dy >= 0 and M[i + dy][j] == 0:
                    M[i + dy][j] = M[i][j]
                    M[i][j] = 0
                    if j + dx <= len(M) - 1 and j + dx >= 0 and M[i + dy][j + dx] == 0:
                        M[i + dy][j + dx] = M[i + dy][j]
                        M[i + dy][j] = 0
                elif j + dx <= len(M) - 1 and j + dx >= 0 and M[i][j + dx] == 0:
                    M[i][j + dx] = M[i][j]
                    M[i][j] = 0
                    if i + dy <= len(M) - 1 and i + dy >= 0 and M[i + dy][j + dx] == 0:
                        M[i + dy][j + dx] = M[i][j + dx]
                        M[i][j + dx] = 0
    return M

# def mouvement(M):
#     for i in range(len(M)):
#         for j in range(len(M)):
#             if M[i][j]!=(0,0):
#                 dx,dy=rd.randint(-1,1),rd.randint(-1,1)
#                 if i+dy<=len(M)-1 and i+dy>=0 and M[i+dy][j]==(0,0):
#                     M[i+dy][j]=M[i][j]
#                     M[i][j]=(0,0)
#                     if j+dx<=len(M)-1 and j+dx>=0 and M[i+dy][j+dx]==(0,0):
#                         M[i+dy][j+dx]=M[i+dy][j]
#                         M[i+dy][j]=(0,0)
#                 elif j+dx<=len(M)-1 and j+dx>=0 and M[i][j+dx]==(0,0):
#                     M[i][j+dx]=M[i][j]
#                     M[i][j]=(0,0)
#                     if i+dy<=len(M)-1 and i+dy>=0 and M[i+dy][j+dx]==(0,0):
#                         M[i+dy][j+dx]=M[i][j+dx]
#                         M[i][j+dx]=(0,0)
#     return(M)

def afficher(M):
    plt.imshow(M)
    plt.show()
    return()

# def afficher(M):
#     n=len(M)
#     M2=[[0 for i in range(n)]for i in range(n)]  
#     for i in range(n):
#         for j in range(n):
#             x,y=M[i][j]
#             M2[i][j]=y
#     plt.imshow(M2)
#     return()
                
def simuler(n,k,l):
    M=init2(n,k,l)
    continuer = True
    while continuer == True:
        plt.pause(0.01)
        plt.clf()
        afficher(mouvement(M))
    return()

def simuler2(n,k):
    M=init(n,k)
    continuer = True
    while continuer == True:
        plt.pause(0.1)
        plt.clf()
        afficher(propagation_knn(mouvement(M),1,0.3,0.3))
    return()
        
def simuler3(n,k,l):
    M=init2(n,k,l)
    C=compte(M)
    continuer=True
    while continuer==True:
        M2=propagation_knn(M,1,0.3,0.3)
        C=compte(M2)
        plt.pause(0.1)
        plt.clf()
        afficher(M2)
        print(C)
    return()

def liste_voisins(M,p,k):
    def f(L):
        return(L[0])
    a,b=p
    D=[]
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j]!=0 and M[i][j]!=M[a][b]:
                p2=(i,j)
                D+=[(distance(p,p2),(i,j))]
    return sorted(D,key=f)[:k]

# def liste_voisins(M,p,k):
#     def f(L):
#         return(L[0])
#     D=[]
#     for i in range(len(M)):
#         for j in range(len(M)):
#             if M[i][j]!=(0,0) and M[i][j]!=p:
#                 p2=(i,j)
#                 D+=[distance(p,p2),M[i][j]]
#     return sorted(D,key=f)[:k]

def etiquette_maj(M,V):
    D={}
    for (_,e) in V:
        x,y=e
        if M[x][y] not in D:
            D[M[x][y]]=1
        else:
            D[M[x][y]]+=1
    M=0
    for e in D:
        if D[e]>M:
            e_maj=e
            M=D[e]
    return e_maj

# def etiquette_maj(V):
#     D={}
#     for (_,p) in V:
#         i,e=p
#         if e not in D:
#             D[e]=1
#         else:
#             D[e]+=1
#     M=0
#     for e in D:
#         if D[e]>M:
#             e_maj=e
#             M=D[e]
#     return e_maj
 
def knn(M,p,k):
    return etiquette_maj(M,liste_voisins(M,p,k))

def bernoulli(pb):
    if rd.random() <= pb:
        return 1
    return 0

def propagation_knn(M,k,pr,pm):
    M2=copy.deepcopy(M)
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j]==2 and bernoulli(pm)==1 and bernoulli(pr)==0:
                M2[i][j]=4
            elif M[i][j]==2 and bernoulli(pr)==1 and bernoulli(pm)==0:
                M2[i][j]=3
            elif M[i][j]==2 and bernoulli(pm)==1 and bernoulli(pr)==1:
                M2[i][j]=4
            elif M[i][j]==2 and bernoulli(pm)==0 and bernoulli(pr)==0:
                M2[i][j]=2
            elif M[i][j]==1 and knn(M,(i,j),k)==2:
                    M2[i][j]=2
    return M2

# def propagation_knn(M,k,pr,pm):
#     M2=copy.deepcopy(M)
#     for i in range(len(M)):
#         for j in range(len(M)):
#             i,e=M[i][j]
#             if e==2 and bernoulli(pm)==1:
#                 M2[i][j]=(i,4)
#             if e==2 and bernoulli(pr)==1:
#                 M2[i][j]=(i,3)
#             else:
#                 if knn(M,M[i][j],k)==2:
#                     M2[i][j]=(i,2)
#     return M2
                
def compte(M):
    C = [0,0,0,0,0]
    for L in M:
        for e in L :
            C[e]=C[e]+1
    return C

# def compte(M):
#     C = [0,0,0,0,0]
#     for L in M:
#         for p in L :
#             i,e=p
#             C[e]=C[e]+1
#     return C

def eliminer_mort(M):
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j]==4:
                M[i][j]=0
    return(M)

def simulation(n,v,pr,pm):
    M=init(n,v)
    C=compte(M)
    t=0
    S,I,R,M,T,popl = [C[1]],[C[2]],[C[3]],[C[4]],[0],[n]
    continuer=True
    while continuer==True:
        t+=1
        M=propagation_knn(mouvement(M),1,pr,pm)
        C=compte(M)
        S.append(C[0])
        I.append(C[1] + C[2]+C[3])
        R.append(C[2])
        M.append(C[3])
        T.append(t)
        popl.append(popl[0] - C[3])
        plt.pause(0.01)
        plt.clf()
        afficher(M)
        if C[1] == 0:
            continuer=False
    return S,I,R,M,T,popl
    
    
#%%     
    

