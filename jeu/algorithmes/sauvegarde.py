def sauvegarde_grille(grille : list) -> None :
    """
        Sauvegarde d'une grille.
    """
    with open("jeu/sauvegarde", "w") as fichier :
        for ligne in grille :
            fichier.write(" ".join(ligne) + "\n")
            
def lire_sauvegarde() -> list :
    """
        Lecture d'une sauvegarde de grille.
    """
    grille = []
    with open("jeu/sauvegarde", "r") as fichier :
        for ligne in fichier :
            grille.append(ligne.split())
    return grille