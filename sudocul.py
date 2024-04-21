"""
    SUDOCUL - Génerateur & Solveur de grilles de Sudoku
    Keyne PEKAR & Jules DAVIDOU
"""

from jeu.algorithmes.generateur_solveur import *
from jeu.algorithmes.sauvegarde import *
from jeu.configuration import *
from jeu.interface.interface import *

"""
taille = 9

grille = generateur_grille(taille, caracteres)
affichage_console(grille)

print()
grille2 = set_difficulte(grille, "Extrême", difficultes, caracteres, taille, 3)
affichage_console(grille2)
"""

grille = lire_sauvegarde()
affichage_console(grille)

print()

backtracking(grille, 9, caracteres, 3)
affichage_console(grille)

sauvegarde_grille(grille)