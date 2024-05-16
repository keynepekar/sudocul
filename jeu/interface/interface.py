import pygame
import sys

def grille(win, taille=9, grille_sudoku=None, cases_modifiables=None, case_selectionnee=None): 
    """
    Crée une grille avec un nombre de lignes et un nombre de colonnes.
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
    cell_size = min(win.get_width() // taille, win.get_height() // taille)

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


def interface(largeur=700, hauteur=700, taille=9, grille_=None):
    """
    Crée et gère l'interface graphique (fenêtre) du Sudocul.
    """
    pygame.init()
    cell_size = min(largeur // taille, hauteur // taille)
    largeur = hauteur = cell_size * taille
    win = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Sudocul")

    cases_modifiables = set()  # Initialisation des cases modifiables
    case_selectionnee = None  # Initialisation de la case sélectionnée

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
                print("Clic de souris sur la case :", (case_i, case_j))

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
                # Mettre à jour la case sélectionnée
                case_selectionnee = (case_i, case_j)

            # Affichage
            win.fill((255, 255, 255))
            grille(win, taille, grille_, cases_modifiables, case_selectionnee)
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
