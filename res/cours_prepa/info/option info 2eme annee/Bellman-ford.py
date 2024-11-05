G1 = [[(3,-2)], [(2,4)], [(0,1), (1,1), (3,4)], [(1,-2)]]

inf = float("inf")

def listes_vers_matrice(G):
    n = len(G)
    M = [[inf for _ in range(n)] for _ in range(n)]
    for u in range(n):
        for (v,w) in G[u]:
            M[u][v] = w
    return M

M1 = listes_vers_matrice(G1)

def bellman_ford(M,s):
    n = len(M)
    d = [[inf for _ in range(n)] for _ in range(n)]
    d[0][s] = 0.
    for k in range(1,n):
        for v in range(n):
            d[k][v] = d[k-1][v]
            for u in range(n):
                new_d = d[k-1][u] + M[u][v]
                if new_d < d[k][v]:
                    d[k][v] = new_d
    return d[n-1]

def bellman_ford_chemins(M,s):
    n = len(M)
    d = [[inf for _ in range(n)] for _ in range(n)]
    d[0][s] = 0.
    P = [-1]*n
    for k in range(1,n):
        for v in range(n):
            d[k][v] = d[k-1][v]
            for u in range(n):
                new_d = d[k-1][u] + M[u][v]
                if new_d < d[k][v]:
                    d[k][v] = new_d
                    P[v] = u
    return d[n-1],P

def bellman_ford_detection(M,s):
    n = len(M)
    d = [[inf for _ in range(n)] for _ in range(n)]
    d[0][s] = 0.
    P = [-1]*n
    for k in range(1,n):
        for v in range(n):
            d[k][v] = d[k-1][v]
            for u in range(n):
                new_d = d[k-1][u] + M[u][v]
                if new_d < d[k][v]:
                    d[k][v] = new_d
                    P[v] = u
    for v in range(n):
        for u in range(n):
            new_d = d[n-1][u] + M[u][v]
            if new_d < d[n-1][v]:
                return None
    return d[n-1],P

def chemin(P,u):
    if P[u] == -1:
        return [u]
    else:
        l = chemin(P,P[u])
        l.append(u)
        return l

def bellman_ford_opti(G,s):
    n = len(G)
    D = [inf for _ in range(n)]
    D[s] = 0.
    P = [-1]*n
    for k in range(1,n):
        for u in range(n):
            for (v,w) in G[u]:
                new_d = D[u] + w
                if new_d < D[v]:
                    D[v] = new_d
                    P[v] = u
    return D,P