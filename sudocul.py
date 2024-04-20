"""
    SUDOCUL - Génerateur & Solveur de grilles de Sudoku
    Keyne PEKAR & Jules DAVIDOU
"""

from jeu.algorithmes.generateur_solveur import *
from jeu.configuration import *

grille = generateur_grille(9, caracteres)

for i in grille:
    print(*i)

print()
grille2 = set_difficulte(grille, "Extrême", difficultes, caracteres, 9, 3)

for i in grille2:
    print(*i)
