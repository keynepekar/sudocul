from math import sqrt
from random import shuffle
import copy


def positions_bloc(x: int, y: int, taille: int) -> list:
    """
        Détermine point ancrage du bloc (haut droit) et renvoie la liste des positions des éléments
        du bloc dans la grille.
    """
    x_anc = (x//taille) * taille
    y_anc = (y//taille) * taille
    return [(i, j) for i in range(x_anc, x_anc + taille) for j in range(y_anc, y_anc + taille)]


def possibilites(grille: list, caracteres: str, pos: tuple, taille_bloc: int) -> list:
    """
        Retourne la différence symétrique du set des caractères utilisés dans la ligne,
        dans la colonne ainsi que dans le bloc (matrice extraite de taille sqrt(n))
        d'une position donnée en argument et les caractères à compléter. 
    """
    x, y = pos
    ligne = set(grille[x])
    colonne = set(i[y] for i in grille)
    # dico des caractères utilisés aux n positions
    bloc = set(grille[i][j] for i, j in positions_bloc(x, y, taille_bloc))
    trouve = (ligne | colonne | bloc)
    if "." in trouve:
        trouve.remove(".")
    return list(set(caracteres) ^ trouve)


def backtracking(grille: list, taille: int, caracteres: str, taille_bloc: int) -> bool:
    """
        Fonction récursive complétant une grille.
        Traite sur la grille donnée et renvoie en booléen si backtracking réussi.
    """
    for i in range(taille):
        for j in range(taille):
            if grille[i][j] == ".":
                liste_possibilites = possibilites(
                    grille, caracteres, (i, j), taille_bloc)
                for p in liste_possibilites:
                    grille[i][j] = p
                    if backtracking(grille, taille, caracteres, taille_bloc):
                        return True
                    grille[i][j] = "."
                return False
    return True


def set_difficulte(grille: list, difficulte: str, difficultes: set, caracteres: str, taille: int, taille_bloc: int) -> list:
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

        if not backtracking(grille_copie, taille, caracteres, taille_bloc):
            grille[i][j] = caractere
        else:
            nb_cases -= 1

    return grille


def generateur_grille(taille: int, caracteres: str) -> list:
    """
        Génère une grille résolue de taille n avec les caractères donnés.
        Utilise le backtracking.
    """

    # La taille doit être un carré parfait
    assert len(caracteres) == taille
    assert sqrt(taille).is_integer()

    grille = [["." for _ in range(taille)] for _ in range(taille)]
    taille_bloc = int(sqrt(taille))

    backtracking(grille, taille, caracteres, taille_bloc)
    return grille