"""
    SUDOCUL - Génerateur & Solveur de grilles de Sudoku
    Keyne PEKAR & Jules DAVIDOU
"""

from jeu.algorithmes.generateur_solveur import *
from jeu.algorithmes.sauvegarde import *
from jeu.configuration import *
from jeu.interface.interface import *

if __name__ == "__main__":
    grille_save = lire_sauvegarde()
    grille_ = set_difficulte(grille_save, "Facile", difficultes, caracteres, 9, 3)
    interface(600, 600, 5, grille_)