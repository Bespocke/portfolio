G = [[7, 8], [2, 4],[1, 7, 8], [4, 5, 9], [1, 3, 6], [3], [4], [2, 0], [2, 0], [3]]

from collections import deque

def parcours_largeur(G, s):
	n= len(G)
    visite = [s]
    marque = [False]*n
    F = deque()
    F.append(s)
    marque[s] = True
    while len(F) > 0:
        u = F.popleft()
        for v in G[u]:
                if not  marque[v]:
                    F.append(v)
                    visite.append(v)
                    marque[v] = True
    return visite



def parcours_profondeur_rec(G, s):
    def visiter(u):
		visite.append(u)
		marque[u] = True
		for v in G[u]:
			if not marque[v]:
				visiter(v)
    n = len(G)
    marque = [False]*n
    visite = []
    visiter(s)
    return visite





def parcours_profondeur_it(G, s):
    visite = []
    marque = [False]*len(G)
    P = []
    P.append(s)
    while len(P) > 0:
        u = P.pop()
        if not marque[u]:
            visite.append(u)
            marque[u] = True
            for v in G[u]:
                 if not marque[v]:
                    P.append(v)
    return visite




def est_connexe(G):
    return len(parcours_largeur(G,0)) == len(G)



def distances(G,s):
	n= len(G)
    marque = [False]*n
    F = deque()
    F.append(s)
    marque[s] = True
    D = [-1]*n
    D[s] = 0
    P = [None]*n
    while len(F) > 0:
        u = F.popleft()
        for v in G[u]:
                if not  marque[v]:
                    F.append(v)
                    marque[v] = True
                    D[v] = D[u] + 1
                    P[v] = u
    return D,P



def chemin(P, u):
	if P[u] == None:
		return [u]
	return chemin(P,P[u])+[u]

def a_un_cycle(G):
	def visiter(u):
		M[u] = 1
		for v in G[u]:
		    if M[v] == 1:
		        M[v] = 2
            elif not M[v]:
            	P[v] = u
                if visiter(v):
                	return True
        return M[u] == 2
    M = [0]*len(G)
    for s in range(len(G)):
		if visiter(s):
			return True
	return False

def cycle(G):
	def visiter(u):
		M[u] = True
		for v in G[u]:
		    if M[v]:
		        M2[v] = True
		        pred2[v] = u
            elif not M[v]:
            	pred[v] = u
            	r = visiter(v)
                if r != None:
                	return r
        if M2[u]:
        	pred[u] = None
        	return chemin(pred,pred2[u]) + [u]
	pred = [None]*len(G)
	pred2 = [None]*len(G)
    M = [False]*len(G)
    M2 = [False]*len(G)
    for s in range(len(G)):
    	if not M[s]:
			r = visiter(s)
			if r != None:
				return r


def a_un_cycle_no(G):
	def visiter(u):
		M[u] = 1
		for v in G[u]:
		    if M[v] == 1 and P[u] != v:
		        M[v] = 2
            elif not M[v]:
            	P[v] = u
                if visiter(v):
                	return True
        return M[u] == 2
    M = [0]*len(G)
    P = [None]*len(G)
    for s in range(len(G)):
		if visiter(s):
			return True
	return False

def cycle_no(G):
	def visiter(u):
		M[u] = True
		for v in G[u]:
		    if M[v] and pred[u] != v:
		        M2[v] = True
		        pred2[v] = u
            elif not M[v]:
            	pred[v] = u
            	r = visiter(v)
                if r != None:
                	return r
        if M2[u]:
        	pred[u] = None
        	return chemin(pred,pred2[u]) + [u]
	pred = [None]*len(G)
	pred2 = [None]*len(G)
    M = [False]*len(G)
    M2 = [False]*len(G)
    for s in range(len(G)):
    	if not M[s]:
			r = visiter(s)
			if r != None:
				return r

G = [[7, 8], [2, 4],[1, 7, 8], [4, 5, 9], [1, 3, 6], [3], [4], [2, 0], [2, 0], [3] ]

print(cycle_no(G))

