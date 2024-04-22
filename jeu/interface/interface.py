import pygame
from pygame.locals import *


def affichage_console(grille : list) -> None :
    """
        Affichage d'une grille dans la console.
    """
    for i in grille:
        print(*i)


# INTERFACE GRAPHIQUE

pygame.init()

fenetre = pygame.display.set_mode((640, 480))
fond = pygame.image.load("").convert()
fenetre.blit(fond,(0,0))

# https://www.zonensi.fr/Miscellanees/Pygame/Base_pygame/
# https://github.com/Kistler21/pygame-sudoku

while 1 :
    for event in pygame.event.get() :
        if event.type == QUIT :
            pygame.quit()
            exit()
    pygame.display.update()
    
    