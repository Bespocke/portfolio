def nils(i,moi,autre1,autre2,memoire):
    memoire.append([0,0,1,0,1,1,0,0,0,1])
    if i<9:
        j=memoire[0][i]
        return j
    if i=9 :
        if autre1[:9]==autre2[:9] and autre1[:9]==[0,0,1,0,1,1,0,0,0,1] :
            memoire.append(0)
            memoire.append(1)
            return 1
        if not autre1[:9]==[0,0,1,0,1,1,0,0,0,1] and not autre2[:9]==[0,0,1,0,1,1,0,0,0,1] :
            memoire.append(3)

        if autre1[:9]==[0,0,1,0,1,1,0,0,0,1] and not autre2[:9]==[0,0,1,0,1,1,0,0,0,1] :
            memoire.append(2)
            return autre2[i-1]
        else:
            memoire.append(1)
            return autre1[i-1]


    if i>9:
        if memoire[1]=0:
            if autre1[i-1]*autre2[i-1]==0:
                memoire[2]=0
            return memoire[2]
        if memoire[1]=1:
            return autre1[i-1]
        if memoire[1]=2:
            return autre2[i-1]
        if memoire[1]=3:

