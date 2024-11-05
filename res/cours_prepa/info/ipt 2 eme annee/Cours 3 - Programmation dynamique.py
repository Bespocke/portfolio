#Fibo pourri
def fibo(n):
    if n <= 1:
        return n
    return fibo(n-1) + fibo(n-2)



#Fibo bas en haut naïf (complexité spatiale linéaire)
def fibo(n):
    T = [0, 1]+[0]*(n-1)
    for i in range(2,n+1):
        T[i] = T[i-2] + T[i-1]
    return T[n]


#Fibo bas en haut optimisé (complexité spatiale constante)
def fibo(n):
    if n == 0:
        return 0
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a+b
    return b

#Rendu bas en haut
def rendu(E, S):
    n = [0]*(S+1)
    for i in range(1, S+1):
        min = n[i - 1]
        for p in E:
            if p <= i and n[i-p] < min:
                min = n[i-p]
        n[i] = 1 + min
    return n[S]


def rendu(E, S):
    n = [0]*(S+1)
    for i in range(1, S+1):
        m = min([n[i-p] for p in E if p <= i])
        n[i] = 1 + m
    return n[S]

#Fibo mémoïsé
memo_fibo = {0:1, 1:1}

def fibo(n):
    if n in memo_fibo:
        return memo_fibo[n]
    else:
        r = fibo(n-1) + fibo(n-2)
        memo_fibo[n] = r
        return r




#Rendu mémoïsé
memo_rendu = {}

def rendu(E, S):
    if S==0:
        return 0
    if (E,S) in memo_rendu:
        return memo_rendu[E,S]
    min = rendu(E,S-1)
    for p in E:
        if p <= S and rendu(E,S-p) < min:
            min = rendu(E,S-p)
    memo_rendu[E,S] = 1 + min
    return 1 + min

#rendu qui marche pas
memo_rendu = {}

def rendu(E, S):
    if S==0:
        return 0
    if S in memo_rendu:
        return memo_rendu[S]
    min = rendu(E,S-1)
    for p in E:
        if p <= S and rendu(E,S-p) < min:
            min = rendu(E,S-p)
    memo_rendu[S] = 1 + min
    return 1 + min

#Reconstruction de rendu bas en haut
def rendu(E, S):
    T = [0]*(S+1)
    for s in range(1, S+1):
        min = T[s - 1]
        for p in E:
            if p <= s and T[s-p] < min:
                min = T[s-p]
        T[s] = 1 + min
    #Reconstruction
    R = []
    while S > 0:
        for p in E:
            if p <= S and T[S-p] + 1 == T[S]:
                R.append(p)
                S = S-p
                break
    return R

#Reconstruction de rendu mémoïsé
memo_rendu = {}

def rendu(E, S):
    if S==0:
        return 0
    if (E,S) in memo_rendu:
        return memo_rendu[E,S]
    min = rendu(E,S-1)
    for p in E:
        if p <= S and rendu(E,S-p) < min:
            min = rendu(E,S-p)
    memo_rendu[E,S] = 1 + min
    return 1 + min

def pieces_a_rendre(E, S):
    R = []
    while S > 0:
        for p in E:
            if p <= S and rendu(E,S-p) + 1 == rendu(E,S):
                R.append(p)
                S = S-p
                break
    return R

#Reconstruction optimisée de rendu bas en haut
def rendu(E, S):
    T = [(0,0)]*(S+1)
    #T[i][0] est la quantité optimale de pièces à rendre sur la somme i
    #T[i][1] est la première pièce qu'on doit rendre sur la somme i
    for s in range(1, S+1):
        min = T[s - 1][0]
        pmin = 1
        for p in E:
            if p <= s and T[s-p][0] < min:
                min = T[s-p][0]
                pmin = p
        T[s] = 1 + min, pmin
    R = []
    while S > 0:
        p = T[S][1]
        S = S - p
        R.append(p)
    return R


