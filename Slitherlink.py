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
        nom_fichier = ""
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
            fltk.texte(400, 300, lst_nom, ancrage = "center",
                       police = "sketchy in snow", taille = "50", tag="nom")
            fltk.mise_a_jour()


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
    effacer_segment(etat, seg)
    etat[seg] = 1


def interdire_segment(etat, seg):
    effacer_segment(etat, seg)
    etat[seg] = -1


def effacer_segment(etat, seg):
    """
    Modifiant etat afin de représenter le fait que segment est maintenant vierge.
    Attention, effacer un segment revient à retirer de l’information
    du dictionnaire etat.
    """
    if not est_vierge(etat, seg):
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
        indices -> List[List]
                : [[None, None, None, None, 0, None], ...]
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
    for i in range(len(indices)):
        for j in range(len(indices)):
            case = i, j
            res = statut_case(indices, etat, case)
            if res is not None and res != 0 :
                return False
    lst_segment_depart = choix_segment_depart(indices, 3)
    if lst_segment_depart == []:
        lst_segment_depart = choix_segment_depart(indices, 2)
        if lst_segment_depart == []:
            lst_segment_depart = choix_segment_depart(indices, 1)
            if lst_segment_depart == []:
                return False
    for segment_depart in lst_segment_depart:
        if longueur_boucle(etat, segment_depart) is not None:
            return True
    else:
        return False


def choix_segment_depart(indices, n):
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

def affiche_images(lst):
    fltk.efface_tout()
    for dico in lst:
        fltk.image(dico["xpos"], dico["ypos"], dico["nom"], ancrage = "nw")
    fltk.mise_a_jour()
    
def event(page, lst):
    if page == "charger_grille":
        nom_fichier = None
    boucle = True
    while boucle:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        for dico in lst:
            if dico["message"] != "inutile":
                if clic_bouton(ev, dico["xpos"], dico["ypos"], dico["dim"]) == True:
                    page = False
                    return dico["message"]
        if page == "charger_grille":
            if clic_bouton(ev, 500, 490, (200, 100)) == True:
                if nom_fichier is not None:
                    charger_grille = False
                    return nom_fichier, "etat_" + nom_fichier
            if clic_bouton(ev, 100, 270, (600, 60)) == True:
                fltk.efface("nom")
                nom_fichier = saisie_nom_fichier(sys.argv) 
        if tev == "Quitte":
            page = False
            return "quitter"
        fltk.mise_a_jour()


def clic_bouton(ev, absc, ordo, dimension):
    lg, ht = dimension
    tev = fltk.type_ev(ev)
    if tev == "ClicGauche":
        if fltk.abscisse(ev) >= absc and fltk.abscisse(ev) <= absc + lg:
            if fltk.ordonnee(ev) >= ordo and fltk.ordonnee(ev) <= ordo + ht:
                return True
            return False






def fonction_jeu(indices, etat):
    """Boucle pour la phase de jeu, doit retourner une instruction pour
    la fonction Slitherlink dans la partie avec 'elif partie'.
    Paramètres:
        indices -> List[List]
                : [[None, None, None, None, 0, None], ...]
        etat -> Dict
    Return:
        instruction -> Str
                    : "quitter", "menu", "sauvegarder", "solution", "choix_grille"
    """
    taille_case = 75
    taille_marge = 40
    initialisation_fenetre(indices, etat, taille_case, taille_marge)
    lg = len(indices[0]) * taille_case + 2 * taille_marge
    fltk.image(lg + 25, 40, "ressources/bouton_sauvergarder.gif", ancrage = "nw")
    fltk.image(lg + 25, 160, "ressources/bouton_solution.gif", ancrage = "nw")
    fltk.image(lg + 25, 280, "ressources/bouton_grille.gif", ancrage = "nw")
    fltk.image(lg + 15, 400, "ressources/bouton_maison.gif", ancrage = "nw")
    fltk.image(lg + 135, 400, "ressources/bouton_eteindre.gif", ancrage = "nw")
    Jouer = True
    while Jouer:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == "ClicGauche":
            absc, ordo = fltk.abscisse(ev), fltk.ordonnee(ev)
            seg = indique_segment(absc, ordo, taille_case, taille_marge, indices)
            if seg is not None:
                if est_trace(etat, seg):
                    effacer_segment(etat, seg)
                else:
                    tracer_segment(etat, seg)
            dessine_etat(indices, etat, taille_case, taille_marge)
            dessine_indices(indices, etat, taille_case, taille_marge)
            if seg is None:
                if clic_bouton(ev, lg + 135, 400, (100, 100)) == True:
                    Jouer = False
                    return "quitter"
                if clic_bouton(ev, lg + 15, 400, (100, 100)) == True:
                    Jouer = False
                    return "menu"
                if clic_bouton(ev, lg + 25, 40, (200, 100)) == True:
                    Jouer = False
                    return "sauvegarder", indices, etat
                if clic_bouton(ev, lg + 25, 160, (200, 100)) == True:
                    Jouer = False
                    return "solution"
                if clic_bouton(ev, lg + 25, 280, (200, 100)) == True:
                    Jouer = False
                    return "choix_grille"
        elif tev == "ClicDroit":
            absc, ordo = fltk.abscisse(ev), fltk.ordonnee(ev)
            seg = indique_segment(absc, ordo, taille_case, taille_marge, indices)
            if seg is not None:
                if est_interdit(etat, seg):
                    effacer_segment(etat, seg)
                else:
                    interdire_segment(etat, seg)
            dessine_etat(indices, etat, taille_case, taille_marge)
            dessine_indices(indices, etat, taille_case, taille_marge)
        elif tev == "Quitte":
            Jouer = False
            return "quitter"
        if partie_finie(indices, etat) == True:
            Jouer = False
            t_pol = len(indices)*25
            fltk.texte((lg + 250)//2, 265, "Bravo !!!", ancrage = "center",
                       couleur = "#B6FF00", police = "sketchy in snow",
                       taille = str(t_pol))
            return "victoire"
        fltk.mise_a_jour()
    fltk.ferme_fenetre()
    return False


def initialisation_fenetre(indices, etat, taille_case, taille_marge):
    """Initialise la fenêtre du jeu
    Paramètres:
        indices -> List[List], permet de connaitre la taille de la grille.
        taille_case -> Int
        taille_marge -> Int
    """
    largeur = len(indices[0]) * taille_case + 2 * taille_marge + 250
    hauteur = max(6, len(indices)) * taille_case + 2 * taille_marge
    fltk.cree_fenetre(largeur, hauteur)
    fltk.rectangle(0, 0, largeur - 250, hauteur, couleur = "#00C8FF",
                   remplissage = "#00C8FF", tag = "cote_jeu")
    fltk.rectangle(largeur - 250, 0, largeur, hauteur, couleur = "#007F7F",
                   remplissage = "#007F7F", tag = "menu_cote")
    trace_fenetre(indices, taille_case, taille_marge)
    dessine_etat(indices, etat, taille_case, taille_marge)
    dessine_indices(indices, etat, taille_case, taille_marge)
    return None

def trace_fenetre(indices, taille_case, taille_marge):
    """Fonction auxiliaire permettant de tracer les cases
    Paramètres:
        indices -> List[List], permet de connaitre la taille de la grille.
        taille_case -> Int
        taille_marge -> Int
    """
    for i in range(len(indices[0]) + 1):
        for j in range(len(indices) + 1):
            sommet_x = taille_marge + i * taille_case
            sommet_y = taille_marge + j * taille_case
            sommet_x2 = taille_marge + (i + 1) * taille_case
            sommet_y2 = taille_marge + (j + 1) * taille_case

            # Trace les sommets
            fltk.cercle(sommet_x, sommet_y, r=5)
            if i != len(indices[0]) and j != len(indices):

                # Trace les segments
                fltk.rectangle(sommet_x, sommet_y, sommet_x2, sommet_y2,
                               couleur="#FFFFFF")

    return None


def indique_segment(x, y, taille_case, taille_marge, indices):
    for i in range(len(indices)):
        for j in range(len(indices[0])):
            sommet_x = taille_marge + i * taille_case
            sommet_y = taille_marge + j * taille_case
            sommet_x2 = taille_marge + (i + 1) * taille_case
            sommet_y2 = taille_marge + (j + 1) * taille_case
            # dx pour décalage x, idem pour dy
            dx = 0.2 * taille_case
            dy = 0.2 * taille_case

            if sommet_x <= x <= sommet_x2 and\
               sommet_y - dy <= y <= sommet_y + dy:
               return ((j, i), (j, i + 1))
            if sommet_y <= y <= sommet_y2 and\
               sommet_x - dx <= x <= sommet_x + dx:
               return ((j, i), (j + 1, i))

            # Pour les cas qui n'ont pas été pris en compte
            if i == len(indices) - 1:
                if sommet_x2 - dx <= x <= sommet_x2 + dx and\
                   sommet_y <= y <= sommet_y2:
                   return ((j, i + 1), (j + 1, i + 1))
            if j == len(indices[0]) - 1:
                if sommet_x <= x <= sommet_x2 and\
                   sommet_y2 - dy <= y <= sommet_y2 + dy:
                    return ((j + 1, i), (j + 1, i + 1))
    return None


def dessine_indices(indices, etat, taille_case, taille_marge):
    fltk.efface("indices")
    for i in range(len(indices[0])):
        for j in range(len(indices)):
            sommet_x = taille_marge + i * taille_case
            sommet_y = taille_marge + j * taille_case
            sommet_x2 = taille_marge + (i + 1) * taille_case
            sommet_y2 = taille_marge + (j + 1) * taille_case
            if indices[j][i] is not None:
                res = statut_case(indices, etat, (j, i))
                if res == 0:
                    couleur_indices = "#004A7F"
                elif res > 0:
                    couleur_indices = "#000000"
                elif res < 0:
                    couleur_indices = "#B12B3B"
                fltk.texte((sommet_x + sommet_x2)/2, (sommet_y + sommet_y2)/2,
                           chaine=indices[j][i], couleur=couleur_indices,
                           ancrage = "center", police = "sketchy in snow",
                           taille = 50, tag="indices")

def dessine_etat(indices, etat, taille_case, taille_marge):
    fltk.efface("etat")
    for i in range(len(indices) + 1):
        for j in range(len(indices[0]) + 1):
            sommet1 = (j, i)
            sommet2 = (j, i + 1)
            sommet3 = (j + 1, i)
            seg1 = (sommet1, sommet2)
            seg2 = (sommet1, sommet3)
            if est_trace(etat, seg1):
                x_sommet1 = taille_marge + i * taille_case
                y_sommet1 = taille_marge + j * taille_case
                x_sommet2 = x_sommet1 + taille_case
                fltk.ligne(x_sommet1, y_sommet1, x_sommet2, y_sommet1,
                           couleur="#004A7F", epaisseur=3, tag="etat")
            elif est_interdit(etat, seg1):
                x_sommet1 = taille_marge + i * taille_case
                y_sommet1 = taille_marge + j * taille_case
                x_sommet2 = x_sommet1 + taille_case
                fltk.ligne(x_sommet1, y_sommet1, x_sommet2, y_sommet1,
                           couleur="#FF0000", epaisseur=3, tag="etat")

            if est_trace(etat, seg2):
                x_sommet1 = taille_marge + i * taille_case
                y_sommet1 = taille_marge + j * taille_case
                y_sommet3 = y_sommet1 + taille_case
                fltk.ligne(x_sommet1, y_sommet1, x_sommet1, y_sommet3,
                           couleur="#004A7F", epaisseur=3, tag="etat")
            elif est_interdit(etat, seg2):
                x_sommet1 = taille_marge + i * taille_case
                y_sommet1 = taille_marge + j * taille_case
                y_sommet3 = y_sommet1 + taille_case
                fltk.ligne(x_sommet1, y_sommet1, x_sommet1, y_sommet3,
                           couleur="#FF0000", epaisseur=3, tag="etat")

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


def fichier_vers_dico(nom_fichier):
    f = open(nom_fichier, "r")
    contenu = f.read()
    cles = []
    valeurs = []
    dico = {}
    contenu = contenu[1:]
    contenu = contenu[:-1]
    while len(contenu)!= 0:
        chaine_a = contenu[0:16]
        elem_a = int(chaine_a[2])
        elem_b = int(chaine_a[5])
        elem_c = int(chaine_a[10])
        elem_d = int(chaine_a[13])
        tuple_a = (elem_a, elem_b)
        tuple_b = (elem_c, elem_d)
        res = (tuple_a, tuple_b)
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
    fltk.efface_tout()
    fltk.mise_a_jour()
    fltk.image(0, 0, "ressources/fond_d'ecran.gif",
               ancrage = "nw", tag = "fond")
    fltk.image(300, 490, "ressources/bouton_valider.gif",
               ancrage = "nw", tag = "menu")
    fltk.rectangle(100, 270, 700, 330, couleur = "black",
                   remplissage = "white", tag = "barre_blanche")
    fltk.texte(75, 70, "Saisissez le nom du fichier :", couleur = "#4CFF00",
               police = "sketchy in snow", taille = "50", tag = "choix")
    sauvegarde = True
    while sauvegarde:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if clic_bouton(ev, 100, 270, (600, 60)) == True:
            fltk.efface("nom")
            nom_fichier = saisie_nom_fichier(sys.argv)
        if clic_bouton(ev, 300, 490, (200, 100)) == True:
            sauvegarde = False
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
    return None

# Boucle principale
def Slitherlink():
    lst_menu = [
    {"xpos": 0, "ypos": 0, "nom": "ressources/fond_d'ecran_menu.gif", "dim": (800, 600), "message": "inutile"}, 
    {"xpos": 300, "ypos": 195, "nom": "ressources/bouton_nouvelle_partie.gif", "dim": (200, 100), "message": "choix_grille"}, 
    {"xpos": 300, "ypos": 330, "nom": "ressources/bouton_charger_partie.gif", "dim": (200, 100), "message": "charger_grille"}, 
    {"xpos": 300, "ypos": 465, "nom": "ressources/bouton_quitter.gif", "dim": (200, 100), "message": "quitter"}
    ]
    lst_choix = [
    {"xpos": 0, "ypos": 0, "nom": "ressources/fond_d'ecran.gif", "dim": (800, 600), "message": "inutile"},
    {"xpos": 300, "ypos": 490, "nom": "ressources/bouton_menu.gif", "dim": (200, 100), "message": "menu"},
    {"xpos": 40, "ypos": 215, "nom": "ressources/bouton_grille1.gif", "dim": (150, 150), "message": "grille1.txt"},
    {"xpos": 230, "ypos": 215, "nom": "ressources/bouton_grille2.gif", "dim": (150, 150), "message": "grille2.txt"},
    {"xpos": 420, "ypos": 215, "nom": "ressources/bouton_grille3.gif", "dim": (150, 150), "message": "grille3.txt"},
    {"xpos": 610, "ypos": 215, "nom": "ressources/bouton_grille4.gif", "dim": (150, 150), "message": "grille4.txt"}
        ]
    lst_charger = [
    {"xpos": 0, "ypos": 0, "nom": "ressources/fond_d'ecran.gif", "dim": (800, 600), "message": "inutile"}, 
    {"xpos": 100, "ypos": 490, "nom": "ressources/bouton_menu.gif", "dim": (200, 100), "message": "menu"}, 
    {"xpos": 500, "ypos": 490, "nom": "ressources/bouton_valider.gif", "dim": (200, 100), "message": "inutile"}, 
    {"xpos": 100, "ypos": 270, "nom": "ressources/barre.gif", "dim": (600, 60), "message": "inutile"}
    ]
    print("Debut du jeu")
    fltk.cree_fenetre(800, 600)
    fenetre = True
    slitherlink = True
    menu = True
    choix_grille = False
    charger_grille = False
    partie = False
    sauvegarde = False
    while slitherlink:
        if fenetre == False and partie == False:
            fltk.cree_fenetre(800, 600)
            fenetre = True
        if menu:
            affiche_images(lst_menu)
            res = event(menu, lst_menu)
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
        elif choix_grille:
            affiche_images(lst_choix)
            fltk.texte(200, 20, "Choix de la grille :", couleur = "#4CFF00",
               police = "sketchy in snow", taille = "50", tag = "choix")
            choix = event(choix_grille, lst_choix)
            nom_fichier = choix
            if choix == "quitter":
                choix_grille = False
                slitherlink = False
                fltk.ferme_fenetre()
            elif choix == "menu":
                choix_grille = False
                menu = True
            elif choix == "grille1.txt" or choix == "grille2.txt" or\
                 choix == "grille3.txt" or choix =="grille4.txt":
                choix_grille = False
                partie = True
                fenetre = False
                indices = fichier_vers_liste(choix)
                etat = {}
                fltk.ferme_fenetre()
        elif charger_grille:
            affiche_images(lst_charger)
            fltk.texte(75, 70, "Saisissez le nom du fichier :", couleur = "#4CFF00",
               police = "sketchy in snow", taille = "50", tag = "choix")
            charger = event("charger_grille", lst_charger)
            if charger == "quitter":
                charger_grille = False
                slitherlink = False
                fltk.ferme_fenetre()
            elif charger == "menu":
                charger_grille = False
                menu = True
            else:
                charger_grille = False
                partie = True
                fenetre = False
                nom_fichier, etat_fichier = charger
                indices = fichier_vers_liste(nom_fichier)
                etat = fichier_vers_dico(etat_fichier)
                fltk.ferme_fenetre()
        elif partie:
            jouer = fonction_jeu(indices, etat)
            if jouer == "choix_grille":
                choix_grille = True
                partie = False
                fltk.ferme_fenetre()
            if jouer == "quitter":
                fltk.ferme_fenetre()
                partie = False
                slitherlink = False
            if jouer == "menu":
                fltk.ferme_fenetre()
                partie = False
                menu = True
            if jouer == "victoire":
                partie = False
                slitherlink = False
                fltk.attend_clic_gauche()
                fltk.ferme_fenetre()
            if len(jouer) == 3:
                fltk.ferme_fenetre()
                sauvegarde = True
                partie = False
        elif sauvegarde:
            message, indices, etat = jouer
            sauvegarder(indices, etat)
            sauvegarde = False
            slitherlink = False
            fltk.ferme_fenetre()

    print("Fin du jeu")

if __name__ == "__main__":
    Slitherlink()
