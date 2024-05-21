import pygame
import sys
from jeu.algorithmes.generateur_solveur import *
from jeu.algorithmes.sauvegarde import *

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
        grille_sudoku = [["-"]*taille for _ in range(taille)]

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
            if grille_sudoku[i][j] != "-":
                color = (255, 0, 0) if (i, j) in cases_modifiables else (0, 0, 0)
                text = font.render(str(grille_sudoku[i][j]), True, color)
                text_rect = text.get_rect(center=rect.center)
                win.blit(text, text_rect)

    pygame.display.update()

def set_difficulte():
    pygame.init()
    pygame.display.set_caption("Choix de la difficulté")
    win = pygame.display.set_mode((500, 500))

    # Créer des boutons
    btn_facile = Bouton(50, 50, 150, 50, "Facile")
    btn_moyen = Bouton(200, 50, 150, 50, "Moyen")
    btn_difficile = Bouton(50, 100, 150, 50, "Difficile")
    btn_extreme = Bouton(200, 100, 150, 50, "Extreme")

    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                load=False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Détecter les clics de souris
                pos = pygame.mouse.get_pos()
                case_i = pos[1] 
                case_j = pos[0]
                if btn_facile.collidepoint(pos):
                    difficulte = "Facile"
                    running = False
                if btn_moyen.collidepoint(pos):
                    difficulte = "Moyen"
                    running = False
                if btn_difficile.collidepoint(pos):
                    difficulte = "Difficile"
                    running = False
                if btn_extreme.collidepoint(pos):
                    difficulte = "Difficile"
                    running = False

            #Dessiner les boutons
            btn_facile.dessiner(win)
            btn_moyen.dessiner(win)
            btn_difficile.dessiner(win)
            btn_extreme.dessiner(win)

            pygame.display.update()  
    # relier à la config de la difficulté
    pygame.quit()  

def charger_partie():
    pygame.init()
    pygame.display.set_caption("Chargement de la partie ?")
    win = pygame.display.set_mode((500, 500))
    
    # Créer des boutons
    btn_oui = Bouton(50, 50, 150, 50, "Oui")
    btn_non = Bouton(50, 150, 150, 50, "Non")

    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                load=False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Détecter les clics de souris
                pos = pygame.mouse.get_pos()
                case_i = pos[1] 
                case_j = pos[0]
                if btn_oui.collidepoint(pos):
                    load=True
                    running = False
                if btn_non.collidepoint(pos):
                    load=False
                    running = False
            #Dessiner les boutons
            btn_oui.dessiner(win)
            btn_non.dessiner(win)

            pygame.display.update()

    pygame.quit()
    return load


def interface(largeur=700, hauteur=700, taille=9, grille_=None):
    """
    Crée et gère l'interface graphique (fenêtre) du Sudocul.
    """
    load=charger_partie()
    if (load==True):
        grille_=lire_sauvegarde()
    pygame.init()
    cell_size = min(largeur // (taille + 2), hauteur // taille)  # Ajuster la largeur pour inclure les boutons
    largeur = cell_size * (taille + 2)  # Ajuster la largeur pour inclure les boutons
    hauteur = cell_size * taille
    win = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Sudocul")

    cases_modifiables = set()  # Initialisation des cases modifiables
    case_selectionnee = None  # Initialisation de la case sélectionnée

    # Charger les images des boutons
    btn_new_game = pygame.image.load('add.png')
    btn_verif_grid = pygame.image.load('circle.png')
    btn_save = pygame.image.load('diskette.png')

    btn_new_game = pygame.transform.scale(btn_new_game, (80, 80))  # Taille souhaitée : 80x80
    btn_verif_grid = pygame.transform.scale(btn_verif_grid, (80, 80))  # Taille souhaitée : 80x80
    btn_save = pygame.transform.scale(btn_save, (80, 80))

    button1_rect = btn_new_game.get_rect(topleft=(taille * cell_size + 40, 50)) # btn Nouvelle partie
    button2_rect = btn_verif_grid.get_rect(topleft=(taille * cell_size + 40, 175)) # btn Vérif grille
    button3_rect = btn_save.get_rect(topleft=(taille * cell_size + 40, 300)) # Btn sauvegarder partie

    # Initialiser la police pour le texte descriptif
    font = pygame.font.Font(None, 24)

    # Texte descriptif pour les boutons
    button1_text = font.render("Nouvelle partie", True, (0, 0, 0))
    button2_text = font.render("Vérifier la grille", True, (0, 0, 0))
    button3_text = font.render("Sauvegarder la partie", True, (0, 0, 0))

    button1_text_rect = button1_text.get_rect(center=(button1_rect.centerx, button1_rect.bottom + 20))
    button2_text_rect = button2_text.get_rect(center=(button2_rect.centerx, button2_rect.bottom + 20))
    button3_text_rect = button3_text.get_rect(center=(button3_rect.centerx, button3_rect.bottom + 20))

    # Identifier les cases modifiables dans la grille
    for i in range(taille):
        for j in range(taille):
            if grille_[i][j] == "-":
                cases_modifiables.add((i, j))

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
                        
                    elif button2_rect.collidepoint(pos) or button2_text_rect.collidepoint(pos):
                        print("vérification de la grille")
                    elif button3_rect.collidepoint(pos) or button3_text_rect.collidepoint(pos):
                        print("sauvegarde")
                        sauvegarde_grille(grille_)

            # Affichage
            win.fill((255, 255, 255))
            grille(win, taille, grille_, cases_modifiables, case_selectionnee)
            
            # Dessiner les boutons
            win.blit(btn_new_game, button1_rect)
            win.blit(btn_verif_grid, button2_rect)
            win.blit(btn_save, button3_rect)

            # Dessiner le texte descriptif des boutons
            win.blit(button1_text, button1_text_rect) # bouton charger partie
            win.blit(button2_text, button2_text_rect) # bouton vérifier
            win.blit(button3_text, button3_text_rect) # bouton sauvegarder

            pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    grille_ = [["1", "-", "3", "4", "6"],
               ["5", "6", "-", "8", "7"],
               ["-", "9", "1", "2", "8"],
               ["3", "4", "5", "-", "9"],
               ["3", "4", "-", "8", "9"]
              ]
    interface(600, 600, 5, grille_)
