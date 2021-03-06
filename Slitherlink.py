#XU Audic
#BENAMARI Damien

import fltk

# Tache 1 - STRUCTURES DE DONNEES

def est_trace(etat, seg):
    """Indique si le segment est tracé.
    Paramètres:
        etat -> Dict
             : {((0, 1), (0, 2)): 1, ...}
        seg -> Tuple(Tuple)
            : ((0, 0), (0, 1))
    Return:
        Bool
    """
    seg_inv = seg[1], seg[0]
    if seg in etat and etat[seg] == 1:
        return True
    if seg_inv in etat and etat[seg_inv] == 1:
        return True
    return False


def est_interdit(etat, seg):
    """Indique si le segment 'seg' est interdit.
    Paramètres:
        etat -> Dict
             : {((0, 1), (0, 2)): 1, ...}
        seg -> Tuple(Tuple)
            : ((0, 0), (0, 1))
    Return:
        Bool
    """
    seg_inv = seg[1], seg[0]
    if seg in etat and etat[seg] == -1:
        return True
    if seg_inv in etat and etat[seg_inv] == -1:
        return True
    return False


def est_vierge(etat, seg):
    """Indique si le segment 'seg' n'est ni tracé ni interdit.
    Paramètres:
        etat -> Dict
             : {((0, 1), (0, 2)): 1, ...}
        seg -> Tuple(Tuple)
            : ((0, 0), (0, 1))
    Return:
        Bool
    """
    seg_inv = seg[1], seg[0]
    if seg in etat or seg_inv in etat:
        return False
    return True


def tracer_segment(etat, seg):
    """Trace un segment et modifie 'etat'.
    Paramètres:
        etat -> Dict
             : {((0, 1), (0, 2)): 1, ...}
        seg -> Tuple(Tuple)
            : ((0, 0), (0, 1))
    """
    effacer_segment(etat, seg)
    etat[seg] = 1


def interdire_segment(etat, seg):
    """Interdit un segment et modifie 'etat'.
    Paramètres:
        etat -> Dict
             : {((0, 1), (0, 2)): 1, ...}
        seg -> Tuple(Tuple)
            : ((0, 0), (0, 1))
    """
    effacer_segment(etat, seg)
    etat[seg] = -1


def effacer_segment(etat, seg):
    """Rend le segment vierge et modifie 'etat'.
    Paramètres:
        etat -> Dict
             : {((0, 1), (0, 2)): 1, ...}
        seg -> Tuple(Tuple)
            : ((0, 0), (0, 1))
    """
    inv_seg = seg[1], seg[0]
    if seg in etat:
        etat.pop(seg)
    elif inv_seg in etat:
        etat.pop(inv_seg)


def fonction_voisins(sommet):
    """Renvoie une liste de sommet qui sont voisins à 'sommet'.
    Paramètres:
        sommet -> Tuple
               : (0, 1)
    Return:
        voisins: List[Tuple]
    Exemples:
        >>> fonction_voisins((0, 1))
        [(1, 1), (-1, 1), (0, 2), (0, 0)]
        >>> fonction_voisins((0, 2))
        [(1, 2), (-1, 2), (0, 3), (0, 1)]
    """
    i_sommet, j_sommet = sommet
    voisins = [(i_sommet + 1, j_sommet), (i_sommet - 1, j_sommet),
               (i_sommet, j_sommet + 1), (i_sommet, j_sommet - 1)]
    return voisins


def segments_tests(etat, sommet, fonction):
    """Renvoie la liste des segments tracés/interdits/vierges adjacents par
     rapport à sommet dans etat.
    Paramètres:
        etat    -> Dict: {((0, 1), (1, 1)): -1, ...}
        sommet  -> Tuple: (2, 1)
        fonction -> function
    Return:
        lst -> List[Tuple(Tuple, Tuple)]
            : [((1, 1), (2, 1)), ((1, 1), (1, 2))]
    Exemple:
        >>> etat = {((0, 1), (0, 2)): 1, ((0, 0), (0, 1)): 1}
        >>> segments_tests(etat, (0, 1), est_trace)
        [((0, 1), (0, 2)), ((0, 1), (0, 0))]
    """
    voisins = fonction_voisins(sommet)
    lst = []

    for voisin in voisins:
        if fonction(etat, (voisin, sommet)):
            lst.append((sommet, voisin))
    return lst


def statut_case(indices, etat, case):
    """Renvoie le statut de la case: None, 0, 1 ou -1.
    Paramètres:
        indices -> List[List]
                : [[None, None, None, None, 0, None], ...]
        etat: Dict
        case: Tuple
    Return:
        Int or None
    Exemple:
        >>> indices, etat, case = [[2, 2], [2, 2]], {}, (1, 1)
        >>> statut_case(indices, etat, case)
        1
        >>> etat = {((1, 2), (2, 2)): 1, ((1, 1), (1, 2)): 1}
        >>> indices, case = [[2, 2], [2, 2]], (1, 1)
        >>> statut_case(indices, etat, case)
        0
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
        elif 4 - nb_inter < indices[case[0]][case[1]]:
            return -1
        elif nb_traces > indices[case[0]][case[1]]:
            return -1
        else:
            return 1


# Tache 2 - CONDITIONS DE VICTOIRE

def partie_finie(indices, etat):
    """Détecte la fin de la partie: lorsque la grille est résolue. Se décompose
    de deux conditions:
    - Chaque indice est satisfait
    - L'ensemble des segments tracés forme une unique boucle fermée.
    Paramètres:
        indices -> List[List]
                : [[None, None, None, None, 0, None], ...]
        etat: Dict
    Return:
        Bool: True or False
    """
    # Première condition
    for i in range(len(indices)):
        for j in range(len(indices[0])):
            case = i, j
            res = statut_case(indices, etat, case)
            if res is not None and res != 0:
                return False
    # Deuxième condition
    lst_segment_depart = choix_segment_depart(indices, 3)
    if lst_segment_depart == []:
        lst_segment_depart = choix_segment_depart(indices, 2)
        if lst_segment_depart == []:
            lst_segment_depart = choix_segment_depart(indices, 1)
            if lst_segment_depart == []:
                # Si aucun segment de départ
                return False
    lg = len([cle for cle, val in etat.items() if val == 1])
    for segment_depart in lst_segment_depart:
        if est_trace(etat, segment_depart) is True:
            res = longueur_boucle(etat, segment_depart)
            if res is not None and res == lg:
                return True
    return False


def choix_segment_depart(indices, n):
    """Sous fonction de partie_finie. Choisit un sommmet pour être le sommet
     de départ ou les sommets de départ.
    Paramètres:
        indices -> List[List]
                : [[None, None, None, None, 0, None], ...]
        n -> Int
    """
    lst_segment_depart = []
    for i in range(len(indices)):
        for j in range(len(indices[0])):
            if n == 3:
                if indices[i][j] == n:
                    lst_segment_depart.append(((i, j), (i, j + 1)))
            if n == 2 or n == 1:
                if indices[i][j] == n:
                    lst_segment_depart.append(((i, j), (i, j + 1)))
                    lst_segment_depart.append(((i + 1, j), (i + 1, j + 1)))
    return lst_segment_depart


def longueur_boucle(etat, seg):
    """Sous fonction de partie_finie. Vérifie que la boucle soit bien fermée.
    Paramètres:
        etat -> Dict
             : {((0, 1), (0, 2)): 1, ...}
        seg -> Tuple(Tuple)
            : ((0, 0), (0, 1))
    Return:
        nb_seg: Int or None
    """
    sommet1, sommet2 = seg
    depart = sommet1
    precedent, courant = sommet1, sommet2
    nb_seg = 1
    while courant != depart:
        voisins = fonction_voisins(courant)
        cmpt = 0
        for voisin in voisins:
            if est_trace(etat, (voisin, courant)) is True:
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

def affiche_images(lst):
    """Affiche toutes les images en utilisant une liste prédéfinie.
    Paramètres:
        lst -> List[Dict]
            : [{'xpos': 0, 'ypos': 0, 'nom': "ressources/fond_d'ecran_menu.gif",...]
    """
    for dico in lst:
        fltk.image(dico["xpos"], dico["ypos"], dico["nom"], ancrage="nw")
    fltk.mise_a_jour()


def menus(page, lst):
    """
    Affiche le menu choisi avec la liste 'lst' et le paramètre 'page'
    Paramètres:
        page -> Bool
        lst -> List[Dict]
            : [{'xpos': 0, 'ypos': 0, 'nom': "ressources/fond_d'ecran_menu.gif",...]
    Return:
        instruction -> Str
    """
    if page == "charger_grille":
        nom_fichier = None
    boucle = True
    while boucle:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        msg = event(ev, lst)
        if msg is not None:
            return msg
        if page == "charger_grille":
            if clic_bouton(ev, 500, 490, (200, 100)) is True:
                if nom_fichier is not None:
                    return nom_fichier, "etat_" + nom_fichier
            if clic_bouton(ev, 100, 270, (600, 60)) is True:
                fltk.efface("nom")
                nom_fichier = saisie_nom_fichier_graphique()
        if tev == "Quitte":
            return "quitter"
        fltk.mise_a_jour()


def clic_bouton(ev, absc, ordo, dimension):
    """Indique si la zone a été cliquée.
    Paramètres:
        ev -> fltk.event
        absc, ordo -> Tuple(Int)
                   : correspond au point en haut à gauche
        dimension -> tuple
    Return:
        Bool -> True or False
    """
    lg, ht = dimension
    tev = fltk.type_ev(ev)
    if tev == "ClicGauche":
        if fltk.abscisse(ev) >= absc and fltk.abscisse(ev) <= absc + lg:
            if fltk.ordonnee(ev) >= ordo and fltk.ordonnee(ev) <= ordo + ht:
                return True
            return False


def fonction_jeu(indices, etat, t_case, t_marge, lst_jeu, lst_condition, lg):
    """Boucle pour la phase de jeu, doit retourner une instruction pour
    la fonction Slitherlink dans la partie avec 'elif partie'.
    Paramètres:
        indices -> List[List]
                : [[None, None, None, None, 0, None], ...]
        etat -> Dict
             : {((0, 1), (0, 2)): 1, ...}
    Return:
        instruction -> Str
                    : "quitter", "menu", "sauvegarder", "solution", "choix_grille"
    """
    affiche_images(lst_jeu)
    Jouer = True
    while Jouer:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        jeu = partie(ev, etat, lst_condition, lst_jeu, t_case, t_marge, indices)
        if jeu is not None:
            return jeu
        if tev == "Quitte":
            Jouer = False
            return "quitter"
        if partie_finie(indices, etat) is True:
            Jouer = False
            t_pol = len(indices) * 25
            fltk.texte((lg + 250) // 2, 265, "Bravo !!!", ancrage="center",
                       couleur="#B6FF00", police="sketchy in snow",
                       taille=str(t_pol))
            return "victoire"
        fltk.mise_a_jour()
    fltk.ferme_fenetre()
    return False


def event(ev, lst):
    """Indique l'instruction choisie par le joueur.
    Paramètres:
        ev -> fltk.event
        lst -> List[Dict]
            : [{"xpos": 123, "ypos": 234...}, {}...]
    Return:
        instruction -> Str
    """
    for dico in lst:
        if dico["message"] != "inutile":
            if clic_bouton(ev, dico["xpos"], dico["ypos"], dico["dim"]) is True:
                return dico["message"]


def partie(ev, etat, lst, lst_jeu, taille_case, taille_marge, indices):
    """Utilisé par fonction_jeu et fait partie des intructions pour 'elif partie'.
    Paramètres:
        ev -> fltk.event
        etat -> Dict
        lst -> List: ["ClicGauche", "ClicDroit"]
        lst_jeu -> List[Dict]
        taille_case -> Int: 75
        taille_marge -> Int: 40
        indices -> List[List]
    """
    tev = fltk.type_ev(ev)
    for elem in lst:
        if tev == elem:
            absc, ordo = fltk.abscisse(ev), fltk.ordonnee(ev)
            seg = indique_segment(absc, ordo, taille_case, taille_marge, indices)
            if seg is not None:
                if elem == "ClicGauche":
                    if est_trace(etat, seg):
                        effacer_segment(etat, seg)
                    else:
                        tracer_segment(etat, seg)
                if elem == "ClicDroit":
                    if est_interdit(etat, seg):
                        effacer_segment(etat, seg)
                    else:
                        interdire_segment(etat, seg)
            dessine_etat(indices, etat, taille_case, taille_marge)
            dessine_indices(indices, etat, taille_case, taille_marge)
            if seg is None:
                msg = event(ev, lst_jeu)
                return msg


def initialisation_fenetre(indices, etat, taille_case, taille_marge):
    """Initialise la fenêtre du jeu
    Paramètres:
        indices -> List[List], permet de connaitre la taille de la grille.
        taille_case -> Int: 75
        taille_marge -> Int: 40
    """
    largeur = len(indices[0]) * taille_case + 2 * taille_marge + 250
    hauteur = max(6, len(indices)) * taille_case + 2 * taille_marge
    fltk.cree_fenetre(largeur, hauteur)
    fltk.rectangle(0, 0, largeur - 250, hauteur, couleur="#00C8FF",
                   remplissage="#00C8FF", tag="cote_jeu")
    fltk.rectangle(largeur - 250, 0, largeur, hauteur, couleur="#007F7F",
                   remplissage="#007F7F", tag="menu_cote")
    trace_fenetre(indices, taille_case, taille_marge)
    dessine_etat(indices, etat, taille_case, taille_marge)
    dessine_indices(indices, etat, taille_case, taille_marge)
    return None


def calcul_sommets(taille_marge, taille_case, coef):
    return taille_marge + coef * taille_case


def trace_fenetre(indices, taille_case, taille_marge):
    """Fonction auxiliaire permettant de tracer les cases.
    Paramètres:
        indices -> List[List], permet de connaitre la taille de la grille.
        taille_case -> Int: 75
        taille_marge -> Int: 40
    """
    for i in range(len(indices[0]) + 1):
        for j in range(len(indices) + 1):
            sommets_x = []
            sommets_y = []
            for k in range(2):
                sommets_x.append(calcul_sommets(taille_marge, taille_case, i + k))
                sommets_y.append(calcul_sommets(taille_marge, taille_case, j + k))
            # Trace les sommets
            fltk.cercle(sommets_x[0], sommets_y[0], r=5)
            if i != len(indices[0]) and j != len(indices):
                # Trace les segments
                fltk.rectangle(sommets_x[0], sommets_y[0], sommets_x[1],
                               sommets_y[1], couleur="#FFFFFF")

    return None


def indique_segment(x, y, taille_case, taille_marge, indices):
    """Indique quel segment vient d'être cliqué.
    Paramètres:
        x -> Int
        y -> Int
        taille_case -> Int: 75
        taille_marge -> Int: 40
        indices -> List[List]
                : [[None, None, None, None, 0, None], ...]
    Return:
        segment -> Tuple(Tuple)
                : ((1, 0), (1, 1))
    """
    for j in range(len(indices)):
        for i in range(len(indices[0])):
            sommets_x = []
            sommets_y = []
            for k in range(2):
                sommets_x.append(calcul_sommets(taille_marge, taille_case, i + k))
                sommets_y.append(calcul_sommets(taille_marge, taille_case, j + k))
            # dx pour décalage x, idem pour dy
            dx = 0.2 * taille_case
            dy = 0.2 * taille_case
            if sommets_x[0] <= x <= sommets_x[1] and\
               sommets_y[0] - dy <= y <= sommets_y[0] + dy:
                return (j, i), (j, i + 1)
            if sommets_y[0] <= y <= sommets_y[1] and\
               sommets_x[0] - dx <= x <= sommets_x[0] + dx:
                return (j, i), (j + 1, i)

            # Pour les cas qui n'ont pas été pris en compte
            if i == len(indices[0]) - 1:
                if sommets_x[1] - dx <= x <= sommets_x[1] + dx and\
                   sommets_y[0] <= y <= sommets_y[1]:
                    return (j, i + 1), (j + 1, i + 1)
            if j == len(indices) - 1:
                if sommets_x[0] <= x <= sommets_x[1] and\
                   sommets_y[1] - dy <= y <= sommets_y[1] + dy:
                    return (j + 1, i), (j + 1, i + 1)
    return None


def dessine_indices(indices, etat, taille_case, taille_marge):
    """Efface puis retrace tous les indices c'est-à-dire les chiffres sur les cases
    Paramètres:
        indices -> List[List]
                : [[None, None, None, None, 0, None], ...]
        etat -> Dict
             : {((0, 1), (0, 2)): 1, ...}
        taille_case -> Int: 75
        taille_marge -> Int: 40
    """
    fltk.efface("indices")
    for i in range(len(indices[0])):
        for j in range(len(indices)):
            x_mid = calcul_sommets(taille_marge, taille_case, i + 0.5)
            y_mid = calcul_sommets(taille_marge, taille_case, j + 0.5)
            if indices[j][i] is not None:
                res = statut_case(indices, etat, (j, i))
                if res == 0:
                    couleur_indices = "#004A7F"
                elif res > 0:
                    couleur_indices = "#000000"
                elif res < 0:
                    couleur_indices = "#B12B3B"
                fltk.texte(x_mid, y_mid, chaine=indices[j][i],
                           couleur=couleur_indices, ancrage="center",
                           police="sketchy in snow", taille=50, tag="indices")


def dessine_etat(indices, etat, taille_case, taille_marge):
    """Efface puis retrace tous les segments.
    Paramètres:
        indices -> List[List]
                : [[None, None, None, None, 0, None], ...]
        etat -> Dict
             : {((0, 1), (0, 2)): 1, ...}
        taille_case -> Int: 75
        taille_marge -> Int: 40
    """
    fltk.efface("etat")
    for j in range(len(indices) + 1):
        for i in range(len(indices[0]) + 1):
            sommets = [(j, i), (j, i + 1), (j + 1, i)]
            segments = [(sommets[0], sommets[1]), (sommets[0], sommets[2])]
            x_sommets = []
            y_sommets = []
            for a in range(2):
                x_sommets.append(calcul_sommets(taille_marge, taille_case, (i + a)))
                y_sommets.append(calcul_sommets(taille_marge, taille_case, (j + a)))
            for k in range(2):
                if est_trace(etat, segments[k]):
                    trace_ligne(k, x_sommets[0], y_sommets[0], x_sommets[1], y_sommets[1], "#004A7F")
                elif est_interdit(etat, segments[k]):
                    trace_ligne(k, x_sommets[0], y_sommets[0], x_sommets[1], y_sommets[1], "#FF0000")


def trace_ligne(k, x_sommet1, y_sommet1, x_sommet2, y_sommet3, couleurs):
    """Sous fonction de dessine_etat.
    Paramètres:
        k -> Int
        x_sommet1, y_sommet -> Tuple(Int)
                            : sommet de référence
        x_sommet2 -> Int, l'abscisse + 1 case
        y_sommet3 -> Int, l'ordonnée + 1 case
        couleurs -> Str, une couleur de type: "#FF00FF"
    """
    if k == 0:
        fltk.ligne(x_sommet1, y_sommet1, x_sommet2, y_sommet1,
                   couleur=couleurs, epaisseur=3, tag="etat")
    if k == 1:
        fltk.ligne(x_sommet1, y_sommet1, x_sommet1, y_sommet3,
                   couleur=couleurs, epaisseur=3, tag="etat")


def saisie_nom_fichier_graphique():
    """Permet de saisir le nom du fichier pour choisir la partie à charger.
    """
    touches = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
               "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
               "y", "z"]
    lst_nom = []
    nom_fichier = ""
    saisie = True
    while saisie:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == "Touche":
            touche = fltk.touche(ev)
            # Str.isdigit() True: All characters are digits
            # Str.lower(): returns a string where all characters are lower case
            if touche.isdigit() or touche.lower() in touches:
                lst_nom.append(touche)
            if touche == "underscore":
                lst_nom.append("_")
            if touche == "Return":
                for lettre in lst_nom:
                    nom_fichier += lettre
                nom_fichier += ".txt"
                saisie = False
                return nom_fichier
            if touche == "BackSpace" and lst_nom != []:
                lst_nom.pop()
        fltk.efface("nom")
        fltk.texte(400, 300, lst_nom, ancrage="center",
                   police="sketchy in snow", taille="50", tag="nom")
        fltk.mise_a_jour()


def fichier_vers_liste(nom_fichier):
    """Vérifie le format et convertie le fichier en indices puis le renvoie.
    Paramètres:
        nom_fichier -> Str
                    : grille0.txt
    Return:
        indices -> List[List]
                : [[None, None, None, None, 0, None], ...]
    """
    carac_autorise = ["0", "1", "2", "3", "4", "_", "\n"]
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
        elif carac not in carac_autorise:
            return False
        else:
            liste_temporaire.append(int(carac))
    return indices


def fichier_vers_dico(nom_fichier):
    """Convertie le fichier en dictionnaire et le renvoie.
    Paramètres:
        nom_fichier -> Str
                    : etat_grille0.txt
    Return:
        dico : {((0, 1), (0, 2)): 1, ...}
    """
    f = open(nom_fichier, "r")
    contenu = f.read()
    cles = []
    valeurs = []
    dico = {}
    contenu = contenu[1:]
    contenu = contenu[:-1]
    while len(contenu) != 0:
        tuples = []
        chaine_a = contenu[0:16]
        for i in range(2):
            tuples.append((int(chaine_a[8 * i + 2]), int(chaine_a[8 * i + 5])))
        res = (tuples[0], tuples[1])
        cles.append(res)
        contenu = contenu[18:]
        if contenu[0] == "-":
            chaine_b = contenu[0:2]
            contenu = contenu[4:]
            valeurs.append(int(chaine_b))
        else:
            chaine_b = contenu[0]
            contenu = contenu[3:]
            valeurs.append(int(chaine_b))
    for i in range(len(cles)):
        dico[cles[i]] = valeurs[i]
    return dico


def sauvegarder(indices, etat):
    """Dans 'elif sauvegarde'. Pour gérer l'interface graphique lors de la sauvegarde.
    Paramètres:
        indices -> List[List]
        etat -> Dict
             : {((0, 1), (0, 2)): 1, ...}
    """
    fltk.image(0, 0, "ressources/fond_d'ecran.gif",
               ancrage="nw", tag="fond")
    fltk.image(500, 490, "ressources/bouton_valider.gif",
               ancrage="nw", tag="valider")
    fltk.image(100, 490, "ressources/bouton_retour.gif",
               ancrage="nw", tag="retour")
    fltk.rectangle(100, 270, 700, 330, couleur="black",
                   remplissage="white", tag="barre_blanche")
    fltk.texte(75, 70, "Saisissez le nom du fichier :", couleur="#4CFF00",
               police="sketchy in snow", taille="50", tag="choix")
    sauvegarde = True
    while sauvegarde:
        ev = fltk.donne_ev()
        if clic_bouton(ev, 100, 270, (600, 60)) is True:
            fltk.efface("nom")
            nom_fichier = saisie_nom_fichier_graphique()
        if clic_bouton(ev, 500, 490, (200, 100)) is True:
            sauvegarde = False
        if clic_bouton(ev, 100, 490, (200, 100)) is True:
            return True
        fltk.mise_a_jour()
    f_etat = open("etat_" + nom_fichier, "w")
    chaine_a = str(etat)
    contenu_a = f_etat.write(chaine_a)
    f_etat.close()
    f_indices = open(nom_fichier, "w")
    chaine_b = ""
    for liste in indices:
        for elem in liste:
            elem = str(elem)
            if elem != "None":
                chaine_b += elem
            else:
                chaine_b += "_"
        chaine_b += "\n"
    contenu_b = f_indices.write(chaine_b)
    f_indices.close()
    return False

# Tache 4 - RECHERCHE DE SOLUTIONS

def filtre_etat_solution(etat_solution):
    """Fonction utilisé pour rendre la solution plus visible. Renvoie un
    dictionnaire 'etat' sans les segments interdits.
    Paramètres:
        etat_solution -> Dict
    Return:
        etat_solution_filtre -> Dict
    """
    etat_solution_filtre = {}
    for segment in etat_solution:
        if etat_solution[segment] == 1:
            etat_solution_filtre[segment] = 1
    return etat_solution_filtre


def verif_case_autour_sommet(indices, etat, sommet):
    """Sous fonction de solveur, vérifie si les indices sont respectés.
    """
    cases = fonction_voisins((sommet[0] - 1, sommet[1] - 1))
    for case in cases:
        if 0 <= case[0] < len(indices) and 0 <= case[1] < len(indices[0]):
            res = statut_case(indices, etat, case)
            if res is not None and res < 0:
                return False
    return True


def applique_solveur(grille, graphique):
    """Détermine le sommet de départ et applique le solveur depuis ce sommet.
    Paramètres:
        grille -> Str: "grille3.txt"
    Return
        res -> Dict or None: La solution 'etat' ou pas de solution
    """
    etat_temporaire = {}
    indices = fichier_vers_liste(grille)
    lst_segment_depart = choix_segment_depart(indices, 3)
    if lst_segment_depart == []:
        lst_segment_depart = choix_segment_depart(indices, 2)
        if lst_segment_depart == []:
            lst_segment_depart = choix_segment_depart(indices, 1)

    for segment_depart in lst_segment_depart:
        sommet_depart, sommet_courant = segment_depart
        # tracer_segment(etat_temporaire, segment_depart)
        res = solveur(indices, etat_temporaire, sommet_depart, graphique)
        if res is not False:
            return res
        # effacer_segment(etat_temporaire, segment_depart)

    return None


def solveur(indices, etat, sommet, graphique):
    """Résout la grille actuelle et l'affiche. Peut afficher toutes les étapes
    graphiquement si graphique vaut True.
    Paramètres:
        indices -> List[List]
        etat -> Dict
        sommet -> Tuple
        graphique -> Bool
    """
    voisins = fonction_voisins(sommet)
    nb_voisins = 0
    for voisin in voisins:
        if est_trace(etat, (voisin, sommet)) is True:
            nb_voisins += 1
    if nb_voisins == 2:
        # verifie les indices
        for i in range(len(indices)):
            for j in range(len(indices[0])):
                case = i, j
                res_statut_case = statut_case(indices, etat, case)
                if res_statut_case != 0 and res_statut_case is not None:
                    return False
        return etat
    elif nb_voisins > 2:
        # on a cree un branchement
        return False
    elif nb_voisins < 2:
        for voisin in voisins:
            if 0 <= voisin[0] <= len(indices) and\
               0 <= voisin[1] <= len(indices[0]):
                if est_vierge(etat, (voisin, sommet)) is True:
                    tracer_segment(etat, (sommet, voisin))
                    if graphique is True:
                        dessine_etat(indices, etat, 75, 40)
                        fltk.mise_a_jour()

                    if len(etat) != 1:
                        # Interdit les segments pouvant causer un branchement
                        for voisin2 in voisins:
                            if est_vierge(etat, (sommet, voisin2)) is True:
                                if 0 <= voisin2[0] <= len(indices) and\
                                   0 <= voisin2[1] <= len(indices[0]):
                                    interdire_segment(etat, (sommet, voisin2))

                    if verif_case_autour_sommet(indices, etat, sommet) is True:
                        res_appel = solveur(indices, etat, voisin, graphique)
                        if res_appel is not False:
                            return res_appel

                    # Efface les interdictions
                    for voisin2 in voisins:
                        if est_interdit(etat, (sommet, voisin2)):
                            effacer_segment(etat, (sommet, voisin2))
                    effacer_segment(etat, (sommet, voisin))
        return False

# Fonction principale
def Slitherlink():
    
    #initialisation
    taille_case = 75
    taille_marge = 40
    lst_menu = [
    {"xpos": 0, "ypos": 0, "nom": "ressources/fond_d'ecran_menu.gif", "dim": (800, 600), "message": "inutile"},
    {"xpos": 300, "ypos": 195, "nom": "ressources/bouton_nouvelle_partie.gif", "dim": (200, 100), "message": "choix_grille"},
    {"xpos": 300, "ypos": 330, "nom": "ressources/bouton_charger_partie.gif", "dim": (200, 100), "message": "charger_grille"},
    {"xpos": 300, "ypos": 465, "nom": "ressources/bouton_quitter.gif", "dim": (200, 100), "message": "quitter"}
    ]
    lst_choix = [
    {"xpos": 0, "ypos": 0, "nom": "ressources/fond_d'ecran.gif", "dim": (800, 600), "message": "inutile"},
    {"xpos": 300, "ypos": 490, "nom": "ressources/bouton_menu.gif", "dim": (200, 100), "message": "menu"},
    {"xpos": 40, "ypos": 215, "nom": "ressources/bouton_grille1_bisbis.gif", "dim": (150, 150), "message": "grille1.txt"},
    {"xpos": 230, "ypos": 215, "nom": "ressources/bouton_grille2_bisbis.gif", "dim": (150, 150), "message": "grille2.txt"},
    {"xpos": 420, "ypos": 215, "nom": "ressources/bouton_grille3_bisbis.gif", "dim": (150, 150), "message": "grille3.txt"},
    {"xpos": 610, "ypos": 215, "nom": "ressources/bouton_grille4_bisbis.gif", "dim": (150, 150), "message": "grille4.txt"}
        ]
    lst_charger = [
    {"xpos": 0, "ypos": 0, "nom": "ressources/fond_d'ecran.gif", "dim": (800, 600), "message": "inutile"},
    {"xpos": 100, "ypos": 490, "nom": "ressources/bouton_menu.gif", "dim": (200, 100), "message": "menu"},
    {"xpos": 500, "ypos": 490, "nom": "ressources/bouton_valider.gif", "dim": (200, 100), "message": "inutile"},
    {"xpos": 100, "ypos": 270, "nom": "ressources/barre.gif", "dim": (600, 60), "message": "inutile"}
    ]
    lst_condition = ["ClicGauche", "ClicDroit"]
    print("Début du jeu")
    fltk.cree_fenetre(800, 600)
    fenetre = True
    slitherlink = True
    menu = True
    choix_grille = False
    choix = None
    charger_grille = False
    partie = False
    sauvegarde = False
    
    #boucle principale    
    while slitherlink:
        
        #crée une fenêtre si besoin
        if fenetre is False and partie is False:
            fltk.cree_fenetre(800, 600)
            fenetre = True
            
        #menu principal
        if menu:
            affiche_images(lst_menu)
            res = menus(menu, lst_menu)
            if res == "choix_grille":
                choix_grille = True
                menu = False
            elif res == "charger_grille":
                charger_grille = True
                menu = False
            elif res == "quitter":
                fltk.ferme_fenetre()
                fenetre = False
                menu = False
                slitherlink = False
                
        #menu de choix de grille
        elif choix_grille:
            affiche_images(lst_choix)
            fltk.texte(200, 20, "Choix de la grille :", couleur="#4CFF00",
               police="sketchy in snow", taille="50", tag="choix")
            choix = menus(choix_grille, lst_choix)
            nom_fichier = choix
            
            #quitter
            if choix == "quitter":
                choix_grille = False
                slitherlink = False
                fltk.ferme_fenetre()
                
            #retour au menu
            elif choix == "menu":
                choix_grille = False
                menu = True

            #lance la partie avec la grille choisie
            elif choix == "grille1.txt" or choix == "grille2.txt" or\
                 choix == "grille3.txt" or choix == "grille4.txt":
                indices = fichier_vers_liste(choix)
                if indices is not False:
                    choix_grille = False
                    partie = True
                    fenetre = False
                    etat = {}
                    fltk.ferme_fenetre()
                #vérification que la grille soit valide
                if indices is False:
                    fltk.texte(190, 100, "Grille invalide", couleur="#FF0000",
                               police="sketchy in snow", taille="70", tag="erreur")
                    fltk.attend_clic_gauche()

        #menu pour charger une grille
        elif charger_grille:
            affiche_images(lst_charger)
            fltk.texte(75, 70, "Saisissez le nom du fichier :", couleur="#4CFF00",
               police="sketchy in snow", taille="50", tag="choix")
            charger = menus("charger_grille", lst_charger)
            
            #quitter
            if charger == "quitter":
                charger_grille = False
                slitherlink = False
                fltk.ferme_fenetre()
            
            #retour au menu
            elif charger == "menu":
                charger_grille = False
                menu = True
            #lance la partie avec la grille et l'état chargé
            else:
                nom_fichier, etat_fichier = charger
                indices = fichier_vers_liste(nom_fichier)
                etat = fichier_vers_dico(etat_fichier)
                if indices is not False:
                    charger_grille = False
                    partie = True
                    fenetre = False
                    fltk.ferme_fenetre()
                #vérfication que la grille soit valide
                if indices is False:
                    fltk.texte(190, 150, "Grille invalide", couleur="#FF0000",
                               police="sketchy in snow", taille="70", tag="erreur")
                    fltk.attend_clic_gauche()

        #ecran de partie
        elif partie:
            
            #initialisation
            lg = len(indices[0]) * taille_case + 2 * taille_marge
            lst_jeu = [{"xpos": lg + 25, "ypos": 40, "nom": "ressources/bouton_sauvegarder.gif", "dim": (200, 100), "message": ("sauvegarder", indices, etat)},
                       {"xpos": lg + 25, "ypos": 160, "nom": "ressources/bouton_solution.gif", "dim": (200, 100), "message": "solution"},
                       {"xpos": lg + 25, "ypos": 280, "nom": "ressources/bouton_solution_graphique.gif", "dim": (200, 100), "message": "solution_graphique"},
                       {"xpos": lg + 15, "ypos": 400, "nom": "ressources/bouton_maison.gif", "dim": (100, 100), "message": "menu"},
                       {"xpos": lg + 135, "ypos": 400, "nom": "ressources/bouton_eteindre.gif", "dim": (100, 100), "message": "quitter"}]
            initialisation_fenetre(indices, etat, taille_case, taille_marge)
            jouer = fonction_jeu(indices, etat, taille_case, taille_marge, lst_jeu, lst_condition, lg)
            
            #utilisation solveur graphique
            if jouer == "solution_graphique":
                if choix is not None:
                    if choix == "grille1.txt" or choix == "grille2.txt" or\
                            choix == "grille3.txt" or choix == "grille4.txt":
                        grille = choix
                else:
                    grille = nom_fichier
                    
                etat_solution = applique_solveur(grille, True)
                if etat_solution is not None:
                    #affichage de la solution sans les segments interdits
                    etat_solution = filtre_etat_solution(etat_solution)
                    dessine_etat(indices, etat_solution, taille_case, taille_marge)
                    t_pol = len(indices)*25
                    #affichage d'un message pour dire qu'on est mauvais
                    fltk.texte((lg + 250)//2, 265, "Bouuuh !!!", ancrage="center",
                               couleur="#FF0000", police="sketchy in snow",
                               taille=str(t_pol))
                fltk.attend_clic_gauche()
                fltk.ferme_fenetre()

            #quitter la partie
            if jouer == "quitter":
                fltk.ferme_fenetre()
                partie = False
                slitherlink = False
                
            #retour au menu
            if jouer == "menu":
                fltk.ferme_fenetre()
                partie = False
                menu = True

            #victoire
            if jouer == "victoire":
                etat = {}
                fltk.attend_clic_gauche()
                fltk.ferme_fenetre()
            
            #sauvegarde d'une partie
            if len(jouer) == 3:
                fltk.ferme_fenetre()
                sauvegarde = True
                partie = False

            #utilisation solveur instantanné
            if jouer == "solution":
                if choix is not None:
                    if choix == "grille1.txt" or choix == "grille2.txt" or\
                            choix == "grille3.txt" or choix == "grille4.txt":
                        grille = choix
                else:
                    grille = nom_fichier
                    
                etat_solution = applique_solveur(grille, False)
                if etat_solution is not None:
                    #affichage de la solution sans les segments interdits
                    etat_solution = filtre_etat_solution(etat_solution)
                    dessine_etat(indices, etat_solution, taille_case, taille_marge)
                    t_pol = len(indices)*25
                    #affichage d'un message pour dire qu'on est mauvais
                    fltk.texte((lg + 250)//2, 265, "Bouuuh !!!", ancrage="center",
                               couleur="#FF0000", police="sketchy in snow",
                               taille=str(t_pol))
                fltk.attend_clic_gauche()
                fltk.ferme_fenetre()
                
        #sauvegarde la partie
        elif sauvegarde:
            message, indices, etat = jouer
            partie = sauvegarder(indices, etat)
            sauvegarde = False
            if partie is False:
                slitherlink = False
            else:
                fenetre = False
            fltk.ferme_fenetre()

    print("Fin du jeu")

# Lance le jeu

if __name__ == "__main__":
    Slitherlink()
