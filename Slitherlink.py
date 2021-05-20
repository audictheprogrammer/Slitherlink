
import fltk
import sys
# Slitherlink game by Audic XU the best and Damien BENAMARI the almost best.


# Tache 1 - STRUCTURES DE DONNEES


def saisie_nom_fichier(argv):
    """Vérifie si le fichier a été saisi, sinon demande de le saisir.
    Paramètres:
        argv -> List
    Return:
        nom_fichier -> Str
    """

    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        return "grille0.txt"


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
    if seg in etat:
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
    inv_seg = seg[1], seg[0]
    if not est_vierge(etat, seg):
        etat.pop(seg)
    elif not est_vierge(etat, inv_seg):
        etat.pop(inv_seg)


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
        elif nb_traces < indices[case[0]][case[1]]:
            return 1
        else:
            return -1

# Tache 2 - CONDITIONS DE VICTOIRE


def partie_finie(indices, etat):
    for i in range(len(indices)):
        for j in range(len(indices[0])):
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
    for dico in lst:
        fltk.image(dico["xpos"], dico["ypos"], dico["nom"], ancrage = "nw")
    fltk.mise_a_jour()

def menus(page, lst):
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
            if clic_bouton(ev, 500, 490, (200, 100)) == True:
                if nom_fichier is not None:
                    return nom_fichier, "etat_" + nom_fichier
            if clic_bouton(ev, 100, 270, (600, 60)) == True:
                fltk.efface("nom")
                nom_fichier = saisie_nom_fichier_graphique()
        if tev == "Quitte":
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

def fonction_jeu(indices, etat, t_case, t_marge, lst_jeu, lst_condition, lg):
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

def event(ev, lst):
    for dico in lst:
        if dico["message"] != "inutile":
            if clic_bouton(ev, dico["xpos"], dico["ypos"], dico["dim"]) == True:
                return dico["message"]

def partie(ev, etat, lst, lst_jeu, taille_case, taille_marge, indices):
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

def calcul_sommets(taille_marge, taille_case, coef):
    return taille_marge + coef * taille_case

def trace_fenetre(indices, taille_case, taille_marge):
    """Fonction auxiliaire permettant de tracer les cases
    Paramètres:
        indices -> List[List], permet de connaitre la taille de la grille.
        taille_case -> Int
        taille_marge -> Int
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
               return ((j, i), (j, i + 1))
            if sommets_y[0] <= y <= sommets_y[1] and\
               sommets_x[0] - dx <= x <= sommets_x[0] + dx:
               return ((j, i), (j + 1, i))

            # Pour les cas qui n'ont pas été pris en compte
            if i == len(indices[0]) - 1:
                if sommets_x[1] - dx <= x <= sommets_x[1] + dx and\
                   sommets_y[0] <= y <= sommets_y[1]:
                   return ((j, i + 1), (j + 1, i + 1))
            if j == len(indices) - 1:
                if sommets_x[0] <= x <= sommets_x[1] and\
                   sommets_y[1] - dy <= y <= sommets_y[1] + dy:
                   return ((j + 1, i), (j + 1, i + 1))
    return None



def dessine_indices(indices, etat, taille_case, taille_marge):
    """Retrace tous les segments en fonction de la variable indices"""
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
                fltk.texte(x_mid, y_mid, chaine = indices[j][i],
                    couleur = couleur_indices, ancrage = "center",
                    police = "sketchy in snow", taille = 50, tag="indices")

def dessine_etat(indices, etat, taille_case, taille_marge):
    """Retrace tous les segments en fonction de la variable etat"""
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
            for k in range (2):
                if est_trace(etat, segments[k]):
                    trace_ligne(k, x_sommets[0], y_sommets[0], x_sommets[1], y_sommets[1], "#004A7F")
                elif est_interdit(etat, segments[k]):
                    trace_ligne(k, x_sommets[0], y_sommets[0], x_sommets[1], y_sommets[1], "#FF0000")

#fonction pour dessine_etat
def trace_ligne(k, x_sommet1, y_sommet1, x_sommet2, y_sommet3, couleurs):
    """Sous-fonction de dessine_etat
    Paramètres:
        k -> Int
        x_sommet1 -> Int
        y_sommet1 -> Int
        x_sommet2 -> Int
        y_sommet3 -> Int
        couleurs -> Str, une couleur de type: "#FF00FF"
    """
    if k == 0:
        fltk.ligne(x_sommet1, y_sommet1, x_sommet2, y_sommet1,
                   couleur = couleurs, epaisseur=3, tag="etat")
    if k == 1:
        fltk.ligne(x_sommet1, y_sommet1, x_sommet1, y_sommet3,
                   couleur = couleurs, epaisseur=3, tag="etat")


def saisie_nom_fichier_graphique():
    """Permet de saisir le nom du fichier pour choisir la partie à charger.
    """

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
            nom_fichier = saisie_nom_fichier_graphique()
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
    lst_condition = ["ClicGauche", "ClicDroit"]
    print("Debut du jeu")
    fltk.cree_fenetre(800, 600)
    fenetre = True
    slitherlink = True
    menu = True
    choix_grille = False
    choix = None
    charger_grille = False
    partie = False
    sauvegarde = False
    while slitherlink:
        if fenetre == False and partie == False:
            fltk.cree_fenetre(800, 600)
            fenetre = True
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
        elif choix_grille:
            affiche_images(lst_choix)
            fltk.texte(200, 20, "Choix de la grille :", couleur = "#4CFF00",
               police = "sketchy in snow", taille = "50", tag = "choix")
            choix = menus(choix_grille, lst_choix)
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
            charger = menus("charger_grille", lst_charger)
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
            lg = len(indices[0]) * taille_case + 2 * taille_marge
            lst_jeu = [{"xpos": lg + 25, "ypos": 40, "nom": "ressources/bouton_sauvegarder.gif", "dim": (200, 100), "message": ("sauvegarder", indices, etat)},
                       {"xpos": lg + 25, "ypos": 160, "nom": "ressources/bouton_solution.gif", "dim": (200, 100), "message": "solution"},
                       {"xpos": lg + 25, "ypos": 280, "nom": "ressources/bouton_grille.gif", "dim": (200, 100), "message": "choix_grille"},
                       {"xpos": lg + 15, "ypos": 400, "nom": "ressources/bouton_maison.gif", "dim": (100, 100), "message": "menu"},
                       {"xpos": lg + 135, "ypos": 400, "nom": "ressources/bouton_eteindre.gif", "dim": (100, 100), "message": "quitter"}]
            initialisation_fenetre(indices, etat, taille_case, taille_marge)
            jouer = fonction_jeu(indices, etat, taille_case, taille_marge, lst_jeu, lst_condition, lg)
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
            if jouer == "solution":
                if choix is not None:
                    if choix == "grille1.txt" or choix == "grille2.txt" or\
                 choix == "grille3.txt" or choix =="grille4.txt":
                     grille = choix
                else:
                    grille = nom_fichier

                # A modifier
                etat_solution = applique_solveur(grille)
                if etat_solution is not None:
                    dessine_etat(indices, etat_solution, taille_case, taille_marge)
                # partie_finie(indices, etat_solution)

                partie = False
                slitherlink = False
                fltk.attend_clic_gauche()
                fltk.ferme_fenetre()
        elif sauvegarde:
            message, indices, etat = jouer
            sauvegarder(indices, etat)
            sauvegarde = False
            slitherlink = False
            fltk.ferme_fenetre()

    print("Fin du jeu")


# Tache 4 - RECHERCHE DE SOLUTIONS

def applique_solveur(grille):
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
        res = solveur(indices, etat_temporaire, sommet_depart)
        if res is not False:
            print(f"Solution trouvé: \n{res}")
            return res
        #effacer_segment(etat_temporaire, segment_depart)

    print("Pas de solution")
    return None


def solveur(indices, etat, sommet):
    voisins = fonction_voisins(sommet)
    nb_voisins = 0
    lst_seg = []
    for voisin in voisins:
        if est_trace(etat, (voisin, sommet)) == True:
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
            if est_vierge(etat, (voisin, sommet)) is True:
                if 0 <= voisin[0] <= len(indices) and\
                0 <= voisin[1] <= len(indices[0]):
                    tracer_segment(etat, (sommet, voisin))
                    res_appel = solveur(indices, etat, voisin)
                    if res_appel is not False:
                        return res_appel
                    else:
                        effacer_segment(etat, (sommet, voisin))
        return False

# nom_fichier = saisie_nom_fichier(sys.argv)
# nom_fichier = "grille1.txt"
# applique_solveur(nom_fichier)



if __name__ == "__main__":
    Slitherlink()
