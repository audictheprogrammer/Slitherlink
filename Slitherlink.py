import fltk
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
        nom_fichier = input("nom du fichier ('grille-personnalisee.txt')\n")
    while not verif_grille(nom_fichier):
        nom_fichier = input("nom du fichier ('grille-personnalisee.txt')\n")
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


def est_trace(etat, seg):
    i_seg, j_seg = seg
    seg_inv = j_seg, i_seg
    if seg in etat and etat[seg] == 1:
        return True
    if seg_inv in etat and etat[seg_inv] == 1:
        return True
    return False

def est_interdit(etat, seg):
    i_seg, j_seg = seg
    seg_inv = j_seg, i_seg
    if seg in etat and etat[seg] == -1:
        return True
    if seg_inv in etat and etat[seg_inv] == -1:
        return True
    return False

def est_vierge(etat, seg):
    i_seg, j_seg = seg
    seg_inv = j_seg, i_seg
    if seg in etat or seg_inv in etat:
        return False
    return True

def tracer_segment(etat, seg):
    etat[seg] = 1

def interdire_segment(etat, seg):
    etat[seg] = -1

def effacer_segment(etat, seg):
    """
    Modifiant etat afin de représenter le fait que segment est maintenant vierge.
    Attention, effacer un segment revient à retirer de l’information
    du dictionnaire etat.
    """
    etat.pop(seg)

def segments_tests(etat, sommet, version):
    """Renvoie la liste des segments interdits adjacents à sommet dans etat
    Paramètres:
        etat -> Dict
        sommet -> Tuple
    Return:
        lst -> List[Tuple(Tuple, Tuple)]
    """

    voisins = fonction_voisins(sommet)
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

def fonction_voisins(sommet):
    i_sommet, j_sommet = sommet
    voisins = [(i_sommet + 1, j_sommet), (i_sommet - 1, j_sommet),
               (i_sommet, j_sommet + 1), (i_sommet, j_sommet - 1)]
    return voisins


def segments_testsV2(etat, sommet, fonction):
    """Renvoie la liste des segments tracés/interdits/vierges adjacents
     à sommet dans etat.
    Paramètres:
        etat    -> Dict: {((0, 1), (1, 1)): -1, ...}
        sommet  -> Tuple: (2, 1)
    Return:
        lst -> List[Tuple(Tuple, Tuple)]
            : [((1, 1), (2, 1)), ((1, 1), (1, 2))]
    """
    voisins = fonction_voisins(sommet)
    lst = []

    for voisin in voisins:
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
                         (i_case + 1, j_case + 1), (i_case + 1, j_case)]
        nb_traces = 0
        nb_inter = 0
        for i in range(len(sommet_autour)):
            seg = (sommet_autour[i - 1], sommet_autour[i])
            nb_traces += est_trace(etat, seg)
            nb_inter += est_interdit(etat, seg)
        if nb_traces == indices[case[0]][case[1]]:
            return 0
        if nb_traces < indices[case[0]][case[1]]:
            return 1
        if nb_traces + nb_inter > indices[case[0]][case[1]]:
            return -1



# Tache 2 - CONDITIONS DE VICTOIRE

def partie_finie(indices, etat):
    for i in range(len(indices) - 1):
        for j in range(len(indices)- 1):
            case = i, j
            res = statut_case(indices, etat, case)
            if res is not None and res != 0 :
                print(case)
                return False
    segment_depart = ((0, 0), (0, 1))
    if longueur_boucle(etat, segment_depart) is not None:
        return True
    else:
        return False


def longueur_boucle(etat, seg):
    i_seg, j_seg = seg
    depart = i_seg
    precedent, courant = i_seg, j_seg
    nb_seg = 1
    while courant != depart:
        voisins = fonction_voisins(courant)
        cmpt = 0
        for voisin in voisins:
            if est_trace(etat, (voisin, courant)) == True:
                cmpt += 1
                if voisin != precedent:
                    adjacent = voisin
                    nb_seg += 1
        if cmpt != 2:
            return None
        else:
            precedent = courant
            courant = adjacent
    return nb_seg


# Tache 3 - INTERFACE GRAPHIQUE

def clic_bouton(ev, absc, ordo):
    tev = fltk.type_ev(ev)
    if tev == "ClicGauche":
        if fltk.abscisse(ev) >= absc and fltk.abscisse(ev) <= absc + 200:
            if fltk.ordonnee(ev) >= ordo and fltk.ordonnee(ev) <= ordo + 100:
                return True
            return False

def Slitherlink():
    fltk.cree_fenetre(800, 600)
    slitherlink = True
    menu = True
    choix_grille = False
    charger_grille = False
    while slitherlink:
        if menu:
            res = fonction_menu()
            if res == "choix_grille":
                choix_grille = True
                menu = False
            elif res == "charger_grille":
                charger_grille = True
                menu = False
            elif res == "quitter":
                fltk.ferme_fenetre()
                menu = False
                slitherlink = False
        if choix_grille:
            choix = fonction_choix_grille()  # fonction pas encore définie
            if choix == "menu":
                choix_grille = False
                menu = True
        if charger_grille:
            fonction_charger_grille()  # fonction pas encore définie


def fonction_menu():
    """Affiche un menu et renvoie le choix de l'utilisateur
    Return:
        Str: "choix_grille"
        Str: "charger_grille"
        None"""
    # initialisation
    fltk.efface_tout()
    fltk.mise_a_jour()
    fltk.image(0, 0, "fond_d'ecran_menu.gif",
               ancrage = "nw", tag = "fond_menu")
    fltk.image(300, 195, "bouton_nouvelle_partie.gif",
               ancrage = "nw", tag = "new_partie")
    fltk.image(300, 330, "bouton_charger_partie.gif",
               ancrage = "nw", tag = "charger_partie")
    fltk.image(300, 465, "bouton_quitter.gif",
               ancrage = "nw", tag = "quitter")
    menu = True
    # Boucle majeure
    while menu:
        ev = fltk.donne_ev()
        if clic_bouton(ev, 300, 195) == True:
            menu = False
            return "choix_grille"
        if clic_bouton(ev, 300, 330) == True:
            menu = False
            return "charger_grille"
        if clic_bouton(ev, 300, 465) == True:
            menu = False
            return "quitter"
        fltk.mise_a_jour()



def fonction_choix_grille():
    """
    if choix_grille:
        fltk.cree_fenetre(800, 600)
        fltk.image(0, 0, "fond_d'ecran.gif",
                   ancrage = "nw", tag = "fond")
        fltk.image(300, 650, "bouton_quitter.gif",
                   ancrage = "nw", tag = "quitter")"""

    fltk.efface_tout()
    fltk.mise_a_jour()
    fltk.image(0, 0, "fond_d'ecran.gif",
               ancrage = "nw", tag = "fond")
    fltk.image(300, 490, "bouton_menu.gif",
               ancrage = "nw", tag = "menu")
    fltk.texte(200, 20, "Choix de la grille :", couleur = "#4CFF00",
               police = "sketchy in snow", taille = "50", tag = "choix")
    fltk.mise_a_jour()
    choix_grille = True
    while choix_grille:
        ev = fltk.donne_ev()
        if clic_bouton(ev, 300, 490) == True:
            choix_grille = False
            return "menu"
        fltk.mise_a_jour()


def fonction_charger_grille():
    pass


def fonction_jeu():
    taille_case = 75
    taille_marge = 40
    nom_fichier = saisie_nom_fichier(sys.argv)
    indices = fichier_vers_liste(nom_fichier)
    print(indices)
    initialisation_fenetre(indices, taille_case, taille_marge)
    Jouer = True
    while Jouer:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == "ClicGauche":
            absc, ordo = fltk.abscisse(ev), fltk.ordonnee(ev)
            indique_segment(absc, ordo, taille_case, taille_marge)
        elif tev == "ClicDroit" or tev == "Quitte":
            Jouer = False
        fltk.mise_a_jour()


def initialisation_fenetre(indices, taille_case, taille_marge):
    """Initialise la fenetre du jeu
    Paramètres:
        indices -> List[List], permet de connaitre la taille de la grille.
        taille_case -> Int
        taille_marge -> Int
    """
    largeur = len(indices) * taille_case + 2 * taille_marge
    hauteur = len(indices) * taille_case + 2 * taille_marge
    fltk.cree_fenetre(largeur, hauteur)
    """fltk.rectangle(taille_marge, taille_marge,
                   largeur - taille_marge, hauteur - taille_marge)"""
    trace_cases(indices, taille_case, taille_marge)
    return None


def trace_cases(indices, taille_case, taille_marge):
    """Fonction auxiliaire permettant de tracer les cases
    Paramètres:
        indices -> List[List], permet de connaitre la taille de la grille.
        taille_case -> Int
        taille_marge -> Int
    """
    for i in range(len(indices) + 1):
        for j in range(len(indices[0]) + 1):
            fltk.cercle(taille_marge + i * taille_case,
                        taille_marge + j * taille_case,
                        5)
            """if i != 0 and j != 0:
                fltk.rectangle(taille_marge + i * taille_case,
                               taille_marge + j *taille_case,
                               taille_marge + (i -1) * taille_case,
                               taille_marge + (j - 1) * taille_case)"""
    return None


def indique_segment(x, y, taille_case, taille_marge):
    for i in range(len(indices) + 1):
        for j in range(len(indices[0]) + 1):
            sommet_x = taille_marge + taille_case * j
            sommet_y = taille_marge + taille_case * i
            decalage_x = sommet_x + 0.2 * taille_case
            decalage_y = sommet_y + 0.2 * taille_case
            if sommet_x - decalage_x <= x <= sommet_x + decalage_x and\
               sommet_y - decalage_y <= y <= sommet_x + decalage_y:
               return (i, j)




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

"""etat = {((0, 1), (1, 1)): -1,
        ((1, 0), (1, 1)): -1,
        ((1, 2), (1, 1)): 1,
        ((2, 1), (1, 1)): 1,
        ((2, 1), (1, 2)): -1}"""

"""etat3 = {((1, 1), (1, 2)): 1,
         ((1, 2), (2, 2)): 1,
         ((2, 2), (2, 1)): 1,
         ((2, 1), (1, 1)): 0}"""


"""etat = {((0, 0), (0, 1)): 1,
        ((0, 1), (1, 1)): 1,
        ((1, 1), (1, 2)): 1,
        ((1, 2), (2, 2)): 1,
        ((2, 2), (2, 1)): 1,
        ((2, 1), (3, 1)): 1,
        ((3, 1), (3, 0)): 1,
        ((3, 0), (2, 0)): 1,
        ((2, 0), (1, 0)): 1,
        ((1, 0), (0, 0)): 1}

indices = [[3, 2, None, None, 0, None],
           [1 , 3 , 1, None, 0, None],
           [3, 2, None, None, None, None],
           [None, None, None, None, 0, 1],
           [None, None, None, None, 0, 1],
           [None, None, None, None, 0, 1]]"""


"""print(longueur_boucle(etat2, ((0, 0),(0, 1))))
print(segments_testsV2(etat, (1, 1), est_trace))
print(segments_testsV2(etat, (1, 1), est_interdit))
print(segments_testsV2(etat, (1, 1), est_vierge))"""


print("FIN DE ZONE DE TEST")


# Boucle principale

if __name__ == "__main__":
    Slitherlink()
