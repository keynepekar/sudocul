import pygame
import sys
import os

# Chemin vers le répertoire parent contenant 'sudocul'
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Importation des programmes supplémentaires
from jeu.algorithmes.generateur_solveur import *
from jeu.algorithmes.sauvegarde import *
from jeu.configuration import *

class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, couleur=(0, 0, 0), couleur_texte=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur = couleur
        self.couleur_texte = couleur_texte
        self.police = pygame.font.Font(None, 24)

    def dessiner(self, surface):
        # Dessiner le rectangle du bouton
        pygame.draw.rect(surface, self.couleur, self.rect)
        # Dessiner le texte
        texte_surface = self.police.render(self.texte, True, self.couleur_texte)
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        surface.blit(texte_surface, texte_rect)


def grille(win, taille=9, grille_sudoku=None, cases_modifiables=None, case_selectionnee=None): 
    """
    Crée une grille d'une certaine taille (9*9 par défaut) avec un nombre de lignes et un 
    nombre de colonnes.
    """
    if grille_sudoku is None:
        grille_sudoku = [["."]*taille for _ in range(taille)]

    if cases_modifiables is None:
        cases_modifiables = set()

    if case_selectionnee is None:
        case_selectionnee = (-1, -1)

    # Calcul de la taille de la police en fonction de la taille de la grille
    font_size = int(36 * (9 / taille))
    font = pygame.font.Font(None, font_size)

    # Calcul de la taille de chaque case en fonction de la taille de la fenêtre et de la grille
    cell_size = min(win.get_width() // (taille + 2), win.get_height() // taille)  # Ajuster la largeur pour inclure les boutons

    for i in range(taille):
        for j in range(taille):
            # Dessiner les cases
            rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
            pygame.draw.rect(win, (255, 255, 255), rect, 2)
            pygame.draw.rect(win, (166, 166, 166), rect, 1)

            # Colorier la case si elle est sélectionnée
            if (i, j) == case_selectionnee:
                pygame.draw.rect(win, (187, 222, 251), rect)

            # Afficher les nombres dans les cases
            if grille_sudoku[i][j] != ".":
                color = (255, 0, 0) if (i, j) in cases_modifiables else (0, 0, 0)
                text = font.render(str(grille_sudoku[i][j]), True, color)
                text_rect = text.get_rect(center=rect.center)
                win.blit(text, text_rect)

    pygame.display.update()

def choix_difficulte(win, largeur, hauteur):
    win.fill((255, 255, 255))

    # Créer des boutons
    btn_facile = Bouton((largeur/2)-(300/2), hauteur/2-60, 150, 50, "Facile")
    btn_moyen = Bouton(160+(largeur/2)-(300/2), hauteur/2-60, 150, 50, "Moyen")
    btn_difficile = Bouton((largeur/2)-(300/2), (hauteur/2), 150, 50, "Difficile")
    btn_extreme = Bouton(160+(largeur/2)-(300/2), (hauteur/2), 150, 50, "Extreme")

    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                difficulte=False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Détecter les clics de souris
                pos = pygame.mouse.get_pos()
                case_i = pos[1] 
                case_j = pos[0]
                if btn_facile.rect.collidepoint(pos):
                    difficulte = "Facile"
                    running = False
                if btn_moyen.rect.collidepoint(pos):
                    difficulte = "Moyen"
                    running = False
                if btn_difficile.rect.collidepoint(pos):
                    difficulte = "Difficile"
                    running = False
                if btn_extreme.rect.collidepoint(pos):
                    difficulte = "Difficile"
                    running = False

            #Dessiner les boutons
            btn_facile.dessiner(win)
            btn_moyen.dessiner(win)
            btn_difficile.dessiner(win)
            btn_extreme.dessiner(win)

            pygame.display.update()  
    # relier à la config de la difficulté

    #del btn_difficile
    #del btn_extreme
    #del btn_facile
    #del btn_extreme

    return difficulte

def charger_partie(win, largeur, hauteur):
    win.fill((255, 255, 255))

    # Crée une zone de texte
    font = pygame.font.Font(None, 40)
    text_surface = font.render("Voulez-vous charger la partie précédente ?", True, (0,0,0))

    text_rect = text_surface.get_rect(center=(largeur/2, 50))
    
    # Créer des boutons
    btn_oui = Bouton((largeur/2)-(150/2), (hauteur/2)-35, 150, 50, "Oui", couleur=(0,0,0), couleur_texte=(255,255,255))
    btn_non = Bouton((largeur/2)-(150/2), (hauteur/2)+35, 150, 50, "Non",couleur=(0,0,0), couleur_texte=(255,255,255))

    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                load=None
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Détecter les clics de souris
                pos = pygame.mouse.get_pos()
                case_i = pos[1] 
                case_j = pos[0]
                if btn_oui.rect.collidepoint(pos):
                    load=True
                    running = False
                if btn_non.rect.collidepoint(pos):
                    load=False
                    running = False
            #Dessiner les boutons
            btn_oui.dessiner(win)
            btn_non.dessiner(win)

            # Dessiner la zone de texte
            win.blit(text_surface, text_rect)

            pygame.display.update()

    del text_surface
    del text_rect
    del btn_oui
    del btn_non      

    return load


def interface(largeur=700, hauteur=700, taille=9, grille_=None):
    """
    Crée et gère l'interface graphique (fenêtre) du Sudocul.
    """

    #---------------------------------------------------------------------------------------------------
    # Set up interface
    #---------------------------------------------------------------------------------------------------
    pygame.init()
    cell_size = min(largeur // (taille + 2), hauteur // taille)  # Ajuster la largeur pour inclure les boutons
    largeur = cell_size * (taille + 2)  # Ajuster la largeur pour inclure les boutons
    hauteur = cell_size * taille
    win = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Sudocul")
   
    #---------------------------------------------------------------------------------------------------
    # Fenêtre de chargement de la partie précédente et choix difficulté
    #---------------------------------------------------------------------------------------------------
    load=charger_partie(win, largeur, hauteur)
    
    win.fill((0, 0, 0))
    largeur=600
    hauteur=600
    
    if load == True :
        grille_ = lire_sauvegarde()
    if (load==False):
        # A MODIF
        win.fill((0, 0, 0))
        generation_grille = generateur_grille(taille)
        difficulte=choix_difficulte(win, largeur, hauteur)
        grille_=set_difficulte(generation_grille, difficulte, taille) # A MODIF
        sauvegarde_grille(grille_)
    elif (load==None):
        pygame.quit()
        sys.exit()
    
    #---------------------------------------------------------------------------------------------------
    # Set up des éléments
    #---------------------------------------------------------------------------------------------------
    cases_modifiables = set()  # Initialisation des cases modifiables
    case_selectionnee = None  # Initialisation de la case sélectionnée

    # Charger les images des boutons
    btn_new_game = pygame.image.load('jeu/interface/assets/add.png')
    btn_verif_grid = pygame.image.load('jeu/interface/assets/circle.png')

    btn_new_game = pygame.transform.scale(btn_new_game, (80, 80))  # Taille souhaitée : 80x80
    btn_verif_grid = pygame.transform.scale(btn_verif_grid, (80, 80))  # Taille souhaitée : 80x80

    button1_rect = btn_new_game.get_rect(topleft=(taille * cell_size + 40, 50)) # btn Nouvelle partie
    button2_rect = btn_verif_grid.get_rect(topleft=(taille * cell_size + 40, 175)) # btn Vérif grille

    # Initialiser la police pour le texte descriptif
    font = pygame.font.Font(None, 24)

    # Texte descriptif pour les boutons
    button1_text = font.render("Nouvelle partie", True, (0, 0, 0))
    button2_text = font.render("Vérifier la grille", True, (0, 0, 0))

    button1_text_rect = button1_text.get_rect(center=(button1_rect.centerx, button1_rect.bottom + 20))
    button2_text_rect = button2_text.get_rect(center=(button2_rect.centerx, button2_rect.bottom + 20))

    # Identifier les cases modifiables dans la grille
    for i in range(taille):
        for j in range(taille):
            if grille_[i][j] == ".":
                cases_modifiables.add((i, j))

    #---------------------------------------------------------------------------------------------------
    # Boucle principale
    #---------------------------------------------------------------------------------------------------
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Détecter les clics de souris
                pos = pygame.mouse.get_pos()
                case_i = pos[1] // cell_size
                case_j = pos[0] // cell_size
                if case_j < taille:  # S'assurer que le clic est dans la grille
                    print("Clic de souris sur la case :", (case_i, case_j))
                    # Mettre à jour la case sélectionnée
                    case_selectionnee = (case_i, case_j)
                    # Affichage
                    win.fill((255, 255, 255))
                    grille(win, taille, grille_, cases_modifiables, case_selectionnee)

                    # Dessiner les boutons
                    win.blit(btn_new_game, button1_rect)
                    win.blit(btn_verif_grid, button2_rect)

                    # Dessiner le texte descriptif des boutons
                    win.blit(button1_text, button1_text_rect) # bouton charger partie
                    win.blit(button2_text, button2_text_rect) # bouton vérifier
                    
                    pygame.display.update()

                    # Vérifier si la case est modifiable
                    if (case_i, case_j) in cases_modifiables:
                        # Gérer la saisie des nombres
                        pygame.event.clear(pygame.KEYDOWN)  
                        while True:
                            for event_key in pygame.event.get():
                                if event_key.type == pygame.KEYDOWN:
                                    if event_key.unicode.isdigit():
                                        number = int(event_key.unicode)
                                        print("Chiffre saisi :", number)
                                        grille_[case_i][case_j] = str(number)
                                        case_selectionnee=None
                                        grille(win, taille, grille_, cases_modifiables, case_selectionnee)
                                        break
                            else:
                                continue
                            break
                else:
                    # Détecter les clics de souris
                    pos = pygame.mouse.get_pos()
                    case_i = pos[1] 
                    case_j = pos[0]
                    print("Clic de souris sur la case :", (case_i, case_j))
                    if button1_rect.collidepoint(pos) or button1_text_rect.collidepoint(pos):
                        print("lancement d'une nouv partie")
                        # A MODIF
                        win.fill((0, 0, 0))
                        generation_grille = generateur_grille(taille)
                        difficulte=choix_difficulte(win, largeur, hauteur)
                        grille_=set_difficulte(generation_grille, difficulte, 9) # A MODIF
                        cases_modifiables = set()
                        # Identifier les cases modifiables dans la grille
                        for i in range(taille):
                            for j in range(taille):
                                if grille_[i][j] == ".":
                                    cases_modifiables.add((i, j))
                        largeur=600
                        hauteur=600
                        
                        
                    elif button2_rect.collidepoint(pos) or button2_text_rect.collidepoint(pos):
                        print("vérification de la grille")
                        match verif_grille(grille_, taille):
                            case True : 
                                print("Résolvable.")
                                sauvegarde_grille(grille_) # tu me diras si ça te convient
                            case False : print("Non résolvable.")

            # Affichage
            win.fill((255, 255, 255))
            grille(win, taille, grille_, cases_modifiables, case_selectionnee)
            
            # Dessiner les boutons
            win.blit(btn_new_game, button1_rect)
            win.blit(btn_verif_grid, button2_rect)

            # Dessiner le texte descriptif des boutons
            win.blit(button1_text, button1_text_rect) # bouton charger partie
            win.blit(button2_text, button2_text_rect) # bouton vérifier

            pygame.display.update()

    pygame.quit()
    sys.exit()

# Sources
# https://geekyhumans.com/fr/voici-le-jeu-sudoku-en-code-source-python/
# ChatGPT