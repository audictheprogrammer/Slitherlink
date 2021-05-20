def solveur(indices, etat, sommet):
    voisins = fonction_voisins(sommet)
    nb_voisins = 0
    res = 0
    for voisin in voisins:
        if est_trace(etat, (voisin, courant)) == True:
            nb_voisins += 1
    if nb_voisins == 2:
        for i in range(len(indices)):
            for j in range(len(indices[0])):
                case = i, j
                res += statut_case(indices, etat, case)
        if res == 0:                
            return True
        return False
    if nb_voisins > 2:
        return False
    if nb_voisins < 2:
        if:
            return True
        if:
            return False
    else:
        return False
    
    