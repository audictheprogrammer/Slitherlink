# import fltk
import sys
# Slitherlink game by Audic XU the best and Damien BENAMARI the almost best.

# TACHE 1 - STRUCTURES DE DONNEES
def saisie_nom_fichier(argv):
    """Vérifie si le fichier a été saisi, sinon demande de le saisir.
    Paramètres:
        argv -> List
    Return:
        nom_fichier -> Str
    """
    if len(argv) >= 2:
        nom_fichier = argv[1]
    else:
        nom_fichier = input("nom du fichier\n")
    while not verif_grille(nom_fichier):
        nom_fichier = input("nom du fichier\n")
    return nom_fichier


def verif_grille(nom_fichier):
    """Vérifie si les caractères du fichier sont autorisés.
    Paramètres:
        nom_fichier -> Str
    Return:
        cond -> Bool
    """
    cond = True
    carac_autorise = ["_", "3", "2", "1", "0", "\n"]
    f = open(nom_fichier, "r")
    contenu = f.read()
    for carac in contenu:
        if carac not in carac_autorise:
            cond = False
    return cond


def fichier_vers_liste(nom_fichier):
    """Convertie le fichier indiqué en liste de liste.
    Paramètres:
        nom_fichier -> Str
    Return:
        indices -> List[List]
                : [[None, None, None, None, 0, None], ...]
    """
    f = open(nom_fichier, "r")
    contenu = f.read()
    indices = []
    liste_temporaire = []
    for carac in contenu:
        if carac == "\n":
            indices.append(liste_temporaire)
            liste_temporaire = []
        elif carac == "_":
            liste_temporaire.append(None)
        else:
            liste_temporaire.append(int(carac))
    return indices


def est_trace(etat, segment):
    if est_vierge(etat, segment) == False:
        if etat[segment] == 1:
            return True
    return False

def est_interdit(etat, segment):
    if est_vierge(etat, segment) == False:
        if etat[segment] == -1:
            return True
    return False

def est_vierge(etat, segment):
    if segment in etat:
        return False
    return True


def tracer_segment(etat, segment):
    etat[segment] = 1

def interdire_segment(etat, segment):
    etat[segment] = -1

def effacer_segment(etat, segment):
    """
    Modifiant etat afin de représenter le fait que segment est maintenant vierge.
    Attention, effacer un segment revient à retirer de l’information
    du dictionnaire etat.
    """
    etat.pop(segment)


def segments_tests(etat, sommet, version):
    """Renvoie la liste des segments interdits adjacents à sommet dans etat
    Paramètres:
        etat -> Dict
        sommet -> Tuple
    Return:
        lst -> List[Tuple(Tuple, Tuple)]
    """

    i_sommet, j_sommet = sommet
    voisins = [(i_sommet + 1, j_sommet), (i_sommet - 1, j_sommet),
               (i_sommet, j_sommet + 1), (i_sommet, j_sommet - 1)]
    lst_traces = []
    lst_interdits = []
    lst_vierges = []
    for cle in etat:
        i_cle, j_cle = cle
        for elem in voisins:
            if ((sommet == i_cle and elem == j_cle) or
            (elem == i_cle and sommet == j_cle)):
                if etat[cle] == 1:
                    lst_traces.append(cle)
                elif etat[cle] == -1:
                    lst_interdits.append(cle)
                else:
                    lst_vierges.append(cle)
    if version == "traces":
        return lst_traces
    if version == "interdits":
        return lst_interdits
    if version == "vierges":
        return lst_vierges


def segments_testsV2(etat, sommet, fonction):
    """Renvoie la liste des segments tracés/interdits/vierges adjacents
     à sommet dans etat.
    Paramètres:
        etat    -> Dict: {((0, 1), (1, 1)): -1, ...}
        sommet  -> Tuple: (2, 1)
    Return:
        lst -> List[Tuple(Tuple, Tuple
            : [((1, 1), (2, 1)), ((1, 1), (1, 2))]
    """
    i_sommet, j_sommet = sommet
    voisins = [(i_sommet + 1, j_sommet), (i_sommet - 1, j_sommet),
               (i_sommet, j_sommet + 1), (i_sommet, j_sommet - 1)]
    lst = []
    for segment in etat:
        for voisin in voisins:
            if segment == (voisin[1], voisin[0]):
                voisin = (voisin[1], voisin[0])
            if fonction(etat, (voisin, sommet)):
                lst.append((sommet, voisin))
        return lst


def statut_case(indices, etat, case):
    """
    Renvoie le statut de la case: None, 0, 1 ou -1.
    Paramètres:
        indices: List
        etat: Dict
        case: Tuple
    Return:
        Int or None
    """
    if indices[case[0]][case[1]] is None:
        return None
    else:
        i_case, j_case = case
        sommet_autour = [(i_case, j_case), (i_case, j_case + 1),
                         (i_case + 1, j_case), (i_case, j_case)]
        nb_segment = 0
        for i in range(len(sommet_autour)):
            seg = (sommet_autour[i - 1], sommet_autour[i])
            seg_inv = (sommet_autour[i], sommet_autour[i - 1])
            # l'une des deux lignes ne modifie pas la valeur de nb_segment
            nb_segment += est_trace(etat, seg) + est_interdit(etat, seg)
            nb_segment += est_trace(etat, seg_inv) + est_interdit(etat, seg_inv)
        return indices[case[0]][case[1]] - nb_segment


# Tache 2 - CONDITIONS DE VICTOIRE

def partie_finie():
    pass




# Zone de tests
"""
etat = {((0, 0), (0, 1)) : 1, ((1, 1), (1, 2)) : - 1}
print(est_vierge(etat, ((0, 0), (0, 1))))   #False
print(est_vierge(etat, ((1, 0), (0, 1))))   #True
print(est_trace(etat, ((0, 0), (0, 1))))    #True
print(est_trace(etat, ((1, 0), (0, 1))))    #False
print(est_interdit(etat, ((0, 0), (0, 1)))) #False
print(est_interdit(etat, ((1, 1), (1, 2)))) #True
tracer_segment(etat, ((1, 0), (0, 1)))
print(etat)
interdire_segment(etat, ((1, 0), (2, 0)))
print(etat)
effacer_segment(etat, ((0, 0), (0, 1)))
print(etat)
"""

etat = {((0, 1), (1, 1)): -1,
        ((1, 0), (1, 1)): -1,
        ((1, 2), (1, 1)): 1,
        ((2, 1), (1, 1)): 1,
        ((2, 1), (1, 2)): -1
        }
# print(segments_testsV2(etat, (1, 1), est_trace))
# print(segments_testsV2(etat, (1, 1), est_interdit))
# print(segments_testsV2(etat, (1, 1), est_vierge))
# print("FIN DE ZONE DE TEST")


# Zone appel de fonctions

nom_fichier = saisie_nom_fichier(sys.argv)
indices = fichier_vers_liste(nom_fichier)
print(statut_case(indices, etat, ((1, 1))))
