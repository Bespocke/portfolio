'''
m[0][pr] = 0 : si on doit choisir parmi 0 objets, on ne peut prendre aucun objet donc la valeur cumulée maximale vaut 0
Si p[i] > pr, on ne peut pas prendre l'objet d'indice i (le i+1e), donc m[i+1][pr] = m[i][pr]
Sinon, on peut prendre le i+1e. Si on ne le prend pas, la valeur cumulée maximale est m[i][pr]. Si on le prend, la valeur cumulée maximale est m[i][pr - p[i]] + v[i]. On prend le maximum des 2 cas pour avoir la valeur cumulée maximale totale.
'''

def sac_ascendant(v, p, Pmax):
    n = len(v)
    m = [[0 for _ in range(Pmax + 1)] for _ in range(n+1)]
    for i in range(n):
        for p_restant in range(0, Pmax + 1):
            if p[i] > p_restant:
                m[i+1][p_restant] = m[i][p_restant]
            else:
                m[i+1][p_restant] = max(m[i][p_restant], m[i][p_restant - p[i]] + v[i])
    return m[n][Pmax]

p = (23, 26, 20, 18, 32, 27, 29, 26, 30, 27)
v = (505, 352, 458, 220, 354, 414, 498, 545, 473, 543)
Pmax = 67

def sac_ascendant_opti(v,p,Pmax):
    n = len(v)
    m = [0 for _ in range(Pmax + 1)]
    for i in range(n):
        for p_restant in range(Pmax, -1, -1):
            if p[i] <= p_restant:
                m[p_restant] = max(m[p_restant], m[p_restant - p[i]] + v[i])
    return m[Pmax]

memo_sac = {}

def sac_descendant_aux(v, p, Pmax, i):
    if i == 0:
        return 0
    if (v, p, Pmax, i) in memo_sac:
        return memo_sac[v, p, Pmax, i]
    if p[i-1] > Pmax:
        r = sac_descendant_aux(v, p, Pmax, i-1)
    else:
        r = max(sac_descendant_aux(v, p, Pmax, i-1), sac_descendant_aux(v, p, Pmax - p[i-1])+ v[i-1], i-1)
    memo_sac[v, p, Pmax, i] = r
    return r

def sac_descendant(v, p, Pmax):
    return sac_descendant_aux(v, p, Pmax, len(v))

#Reconstruction


def sac_ascendant_detail(v,p,Pmax):
    n = len(v)
    m = [[0 for _ in range(Pmax + 1)] for _ in range(n+1)]
    for i in range(n):
        for p_restant in range(0, Pmax + 1):
            if p[i] > p_restant:
                m[i+1][p_restant] = m[i][p_restant]
            else:
                m[i+1][p_restant] = max(m[i][p_restant], m[i][p_restant - p[i]] + v[i])
    R = []
    P = Pmax
    k = n-1
    while k>=0 and P>=0:
        if m[k+1][P] == m[k][P]:
            k = k-1
        else:
            R.append(k)
            k = k-1
            P = P - p[k+1]
    return R

memo_sac_detail = {}

def sac_descendant_detail_aux(v, p, n, Pmax):
    if n == 0:
        return 0,[]
    if (v, p, n, Pmax) in memo_sac_detail:
        return memo_sac_detail[v, p, n, Pmax]
    if p[n-1] > Pmax or sac_descendant_detail_aux(v, p, n-1, Pmax)[0] >= sac_descendant_detail_aux(v, p, n-1, Pmax - p[n-1])[0] + v[n-1] :
        r, R = sac_descendant_detail_aux(v, p, n-1, Pmax)
    else:
        r, R = sac_descendant_detail_aux(v, p, n-1, Pmax - p[n-1])
        r += v[n-1]
        R.append(n-1)
    memo_sac[v, p, n, Pmax] = r, R
    return r, R

def sac_descendant_detail(v, p, Pmax):
    return sac_descendant_detail_aux(v, p, len(v), Pmax)

'''
Par définition, M[n] contient les distances recherchées, où n est le nombre de sommets
On a les relations :
M[0][u][v] = M[u][v] (on ne peut avoir aucun sommet intermédiaire donc on se ramène à l'existence d'un arc direct de u à v)
M[k][u][v] = min(M[k-1][u][v], M[k-1][u][k-1] + M[k-1][k-1][v]) (on fait la disjonction entre le cas où le chemin réalisant M[k][u][v] n'a pas k-1 comme sommet intermédiaire, et le cas contraire)
'''


def floyd_warshall(G):
    n = len(G)
    M = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(n+1)]
    for u in range(n):
        for v in range(n):
            M[0][u][v] = G[u][v]
    for k in range(1,n+1):
        for u in range(n):
            for v in range(n):
                M[k][u][v] = min(M[k-1][u][v], M[k-1][u][k-1] + M[k-1][k-1][v])
    return M[n]

inf = float("inf")
G = [[inf, inf, 0, inf], [-1, inf, inf, 2], [inf, 1, inf, 2], [inf, inf, inf, inf]]

def floyd_warshall_opti(G):
    n = len(G)
    M = [[0 for _ in range(n)] for _ in range(n)]
    for u in range(n):
        for v in range(n):
            M[u][v] = G[u][v]
    for k in range(1,n+1):
        for u in range(n):
            for v in range(n):
                M[u][v] = min(M[u][v], M[u][k-1] + M[k-1][v])
    return M

def floyd_warshall_chemins(G):
    n = len(G)
    M = [[0 for _ in range(n)] for _ in range(n)]
    P = [[-1 for _ in range(n)] for _ in range(n)]
    for u in range(n):
        for v in range(n):
            M[u][v] = G[u][v]
            if G[u][v] < inf:
                P[u][v] = u
    for k in range(1,n+1):
        for u in range(n):
            for v in range(n):
                d = M[u][k-1] + M[k-1][v]
                if d < M[u][v]:
                    M[u][v] = d
                    P[u][v] = P[k-1][v]
    return M,P

def chemin(P,u,v):
    if u==v:
        return [u]
    elif P[u][v] == -1:
        return []
    else:
        l = chemin(P,u,P[u][v])
        l.append(v)
        return l
