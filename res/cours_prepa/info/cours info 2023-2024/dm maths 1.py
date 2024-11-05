#%%

import numpy as np

def u(x, n):
    L = [x, 0]
    U_n = 0
    U_n_1 = x
    for i in range(n):
        annexe = U_n
        U_n = 1/2 * (annexe**2 + U_n_1**2)
        U_n_1 = annexe
        L.append(U_n)
    return L

def zero(L):
    for i in range(len(L)-1):
        if L[i] <= 1 and L[i+1] <= 1:
            return True
    return False

def infini(L):
    for i in range(len(L)-1):
        if L[i] >= 1 and L[i+1] >= 1:
                return True
    return False

def un(L):
    for i in range(len(L)-1):
        if L[i] == 1 and L[i+1] == 1:
                return True
    return False

def test():
    a = 1.41
    b = 2
    s = ""
    while True:
        m = (a+b)/2
        if zero(u(m, 10)):
            a = m
        elif infini(u(m, 8)):
            b = m
        s = str(a)
        if len(s) > 10:
            break
    return a 

#%%