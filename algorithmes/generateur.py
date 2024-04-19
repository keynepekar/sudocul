from random import choice

def difference(grille : list, caracteres : str, pos : tuple) -> list:
    """
        Retourne la différence symétrique des sets des caractères utilisés dans la ligne
          et dans la colonne d'une position donnée en argument et les caractères à compléter. 
    """
    utilise = [i for i in grille[pos[0]] if i !="."]
    utilise += [i for i in [j[pos[1]] for j in grille] if i !="."]
    utilise = list(dict.fromkeys(utilise))
    return list({i for i in caracteres} ^ set(utilise))


def generateur(taille : int, caracteres : str):
    assert len(caracteres) == taille

    cpt = 0

    def generation():
        grille = [["." for _ in range(taille)] for _ in range(taille)]
        
        for i in range(taille):
            for j in range(taille):
                possibilites = difference(grille, caracteres, (i,j))
                if possibilites == [] : return None
                grille[i][j] = choice(possibilites)
        
        return grille
    
    while True :
        grille = generation()
        cpt +=1
        if grille : break

    return grille, cpt

# TESTS ---
#tab = [["1","2","3"],["2",".","."],[".",".","."]]
#print(difference(tab,"123",(1,2)))

grille = generateur(9, "123456789"[:9])

for i in grille[0] : print(*i)