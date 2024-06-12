from math import sqrt
from random import shuffle
import copy
from jeu import configuration as config

def positions_bloc(x: int, y: int, taille: int) -> list:
    """
        Détermine point ancrage du bloc (haut droit) et renvoie la liste des positions des éléments
        du bloc dans la grille.
    """
    x_anc = (x//taille) * taille
    y_anc = (y//taille) * taille
    return [(i, j) for i in range(x_anc, x_anc + taille) for j in range(y_anc, y_anc + taille)]


def possibilites(grille: list, pos: tuple, caracteres: str = config.caracteres) -> list:
    """
        Retourne la différence symétrique du set des caractères utilisés dans la ligne,
        dans la colonne ainsi que dans le bloc (matrice extraite de taille sqrt(n))
        d'une position donnée en argument et les caractères à compléter. 
    """
    taille_bloc = int(sqrt(len(grille)))
    x, y = pos
    ligne = set(grille[x])
    colonne = set(i[y] for i in grille)
    # dico des caractères utilisés aux n positions
    bloc = set(grille[i][j] for i, j in positions_bloc(x, y, taille_bloc))
    trouve = (ligne | colonne | bloc)
    if "." in trouve:
        trouve.remove(".")
    return list(set(caracteres) ^ trouve)


def backtracking(grille: list, taille: int, caracteres: str = config.caracteres) -> bool:
    """
        Fonction récursive complétant une grille.
        Traite sur la grille donnée et renvoie en booléen si backtracking réussi.
    """
    for i in range(taille):
        for j in range(taille):
            if grille[i][j] == ".":
                liste_possibilites = possibilites(grille, (i, j))
                for p in liste_possibilites:
                    grille[i][j] = p
                    if backtracking(grille, taille):
                        return True
                    grille[i][j] = "."
                return False
    return True


def set_difficulte(grille: list, difficulte: str, taille: int, difficultes: set = config.difficultes, caracteres: str = config.caracteres) -> list:
    """
        Selon la configuration de la difficulté, dispose sur la grille des ".". Traite sur une copie profonde
        de la grille pour vérifier si il y a toujours une possibilité.
    """
    positions = [(i, j) for i in range(len(grille))
                 for j in range(len(grille))]
    shuffle(positions)
    nb_cases = int((difficultes[difficulte]/100)*taille**2)

    while nb_cases > 0:
        i, j = positions.pop()
        caractere = grille[i][j]
        grille[i][j] = "."
        grille_copie = copy.deepcopy(grille)

        if not backtracking(grille_copie, taille):
            grille[i][j] = caractere
        else:
            nb_cases -= 1

    return grille


def generateur_grille(taille: int, caracteres: str = config.caracteres) -> list:
    """
        Génère une grille résolue de taille n avec les caractères donnés.
        Utilise le backtracking.
    """

    # La taille doit être un carré parfait
    assert len(caracteres) == taille
    assert sqrt(taille).is_integer()

    grille = [["." for _ in range(taille)] for _ in range(taille)]
    taille_bloc = int(sqrt(taille))
    
    # On dispose quelques nombres aléatoires pour un backtracking également random.
    ligne_random = list(caracteres)
    shuffle(ligne_random)
    grille[0] = ligne_random

    backtracking(grille, taille)
    return grille

def verif_grille(grille: list, taille : int) -> bool:
    """
        Vérifie si une grille être résolvable en l'état.
        On traite sur une copie profonde locale de la grille pour ne pas la flinguer avec le backtracking.
        On vérifie également si la grille a bien été traitée jusqu'à présent.
    """
    # Test des placements effectués
    for i in range(taille):
        for j in range(taille):
            elem = grille[i][j]
            if elem == "." : continue
            if grille[i].count(elem) + grille[:][j].count(elem) > 2: return False
            if [grille[pos[0]][pos[1]] for pos in positions_bloc(i, j, int(sqrt(taille)))].count(elem) > 1 : return False
    
    # Test de backtracking
    grille_copy = copy.deepcopy(grille)
    return backtracking(grille_copy, taille)