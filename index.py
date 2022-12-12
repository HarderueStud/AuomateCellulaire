import sys, time
# Si version de Python == 3
if sys.version_info[0] == 3:        
    from tkinter import *
# Si version de Python != 3
else:
    from Tkinter import *

cellulesEnVie = {} # cellules en vie maintenant
cellulesEnVie2 = {}  # cellules en vie etape suivante
celluleSize = 14 # Taille d'une cellule, Largeur = Hauteur -> care
cellulesExaminees = {} # cellules deja examinées
cellulesVoisines = {} # cellules voisine des cellules en vie
    
grilleCouleur = "grey20" # Couleur des lignes de la grille
running = False # Sa tourne

# Calcul et retourne la position de la cellule a modifier, en fonction de la position du click a l'ecran, la ligne et la colonne.
def CalculCoordEtNumLigne(event):
    global celluleSize

    x = event.x - (event.x % celluleSize) # Coord x du click -> coord x de la cellule
    y = event.y - (event.y % celluleSize) # Coord y du click -> coord y de la cellule
    lig = int(y / celluleSize) # Ligne
    col = int(x / celluleSize) # Colonne
    return x, y, lig, col

# Retourne le nombre de cellules voisine en vie d'une cellule donné.
def RechercheCellulesVoisines(lig, col, rechercheVoisine):
    global cellulesVoisines

    voisinesEnVie = 0   # nbr cellules voisines en vie

    # a b c
    # d x e
    # f g h

    # -> a b c d e f g h
    for voisine in ((lig-1, col-1), (lig-1, col), (lig-1, col+1), (lig, col-1), (lig, col+1), 
    (lig+1, col-1), (lig+1, col), (lig+1, col+1)):

        if rechercheVoisine:
            cellulesVoisines.setdefault(voisine)
            #print("Cellule voisine de [", str(lig), ",", str(col), "] : ", voisine)

        if voisine in cellulesEnVie: # Si la cellule voisine est en vie
            voisinesEnVie += 1
            #print("Cellule [", str(lig), ",", str(col), "] : +1 voisine en vie : ", voisine)
    return voisinesEnVie # retourne le nombre de cellule voisine en vie


def JeuDeLaVie(voisineEnVie, lig, col):
    global cellulesEnVie
    global cellulesEnVie2
    # Moins de 2 cellules voisine vivante -> mort de la cellule
    if voisineEnVie == 2: # 2 cellules voisines en vie -> on ne change pas
        if (lig, col) in cellulesEnVie: # On verifie qu'elle est bien en vie maintenant
            cellulesEnVie2.setdefault((lig, col))
            #print("[", str(lig), ",", str(col), "] -> voisine = 2 -> stille alive")
    elif voisineEnVie == 3: # 3 cellules voisines en vie -> on change pas si deja vivante, une nouvelle cellule vivante si pas de cellules encore
            cellulesEnVie2.setdefault((lig, col))
            #print("[", str(lig), ",", str(col), "] -> voisine = 3 -> still alive / new one")
        
        # Au dela de 4, les cellules meurent de surpopulation


def DayAndNight(voisineEnVie, lig, col):
    global cellulesEnVie
    global cellulesEnVie2
     # En dessous de 3 cellules voisine vivante -> mort d ela cellule
    if voisineEnVie in [3, 4, 6, 7, 8]: # 3, 4, 6, 7 ou 8 cellules voisines en vie -> on ne change pas
        if (lig, col) in cellulesEnVie: # On verifie qu'elle est bien en vie maintenant
            cellulesEnVie2.setdefault((lig, col))
        else :
            if voisineEnVie != 4: # Si 3, 6, 7 ou 8 cellules voisine en vie ET la cellule est morte -> une nouvelle nait.
                cellulesEnVie2.setdefault((lig, col))
        
        # 1, 2, 5 voisines vivante tuera la cellule a coup sur, si la cellule a 4 voisines vivantes, ell restera en vie si elle l'est deja,
        # si elle est morte, elle le restera.


def QuadLife(voisineEnVie, lig, col):
    global cellulesEnVie
    global cellulesEnVie2
    # Une cellule morte y naît à l'étape suivante si elle est entourée de 3 voisines, une cellule vivante survit à l'étape suivante
    # si elle est entourée de 2 ou 3 cellules vivantes.
    # Lorsqu'une cellule naît, si toutes les cellules qui lui ont donné naissance se trouvent dans des états différents,
    # la nouvelle cellule prend l'état restant. Dans le cas contraire, elle prend l'état de la majorité des trois cellules.

    if voisineEnVie in [2, 3]: # entourée de 2 ou 3 cellules vivantes
        if (lig, col) in cellulesEnVie: # On verifie qu'elle est bien en vie maintenant
            cellulesEnVie2.setdefault((lig, col))
        else :
            if voisineEnVie != 2: # Si 3 cellules voisine en vie ET la cellule est morte -> une nouvelle nait.
                cellulesEnVie2.setdefault((lig, col))


# Application des regles du jeu de la vie pour determiner le futur d'une cellule donné, en fonction du nbr de cellule voisine en vie.
def FuturDeLaCellule(voisineEnVie, lig, col):
    global cellulesEnVie
    global cellulesEnVie2
    #print("NBR Cellule voisine de [", str(lig), ",", str(col), "] : ", voisineEnVie)

    if modeDeJeu == 1: # jeu de la vie
        JeuDeLaVie(voisineEnVie, lig, col)
    elif modeDeJeu == 2: # jeu du jour et de la nuit
       DayAndNight(voisineEnVie, lig, col)
    else : # jeu QuadLife
        QuadLife(voisineEnVie, lig, col)


# "Animation"
def MiseAJourCellules():
    global running
    global celluleSize
    global cellulesEnVie
    global cellulesEnVie2
    global cellulesExaminees
    global cellulesVoisines
    global grilleCouleur
    global Grille

    #print("\n AVANT MAJ : ")
    #print("\nCELLULE EN VIE T : ", cellulesEnVie)
    #print("\nCELLULE EN VIE T + 1 : ", cellulesEnVie2)

    for lig, col in cellulesEnVie.keys(): # test chaque cellule en vie
        cellulesExaminees.setdefault((lig, col))

        voisineEnVie = RechercheCellulesVoisines(lig, col, True) # cellules voisines de la cellule en vie
        FuturDeLaCellule(voisineEnVie, lig, col) # Decision sur son futur

    for lig, col in cellulesVoisines.keys(): # test chaque cellules voisines de chaque cellule en vie
        if not (lig, col) in cellulesExaminees: # si la cellule n'est pas deja examinee a la boucle precedente
            cellulesExaminees.setdefault((lig, col))
            voisineEnVie = RechercheCellulesVoisines(lig, col, False) # recherche voisine en vie
            FuturDeLaCellule(voisineEnVie, lig, col) # decision de son futur

    
    Grille.delete("celluleEnVie") # On supprime les cellules en vie graphiquement, pour mieu les redessiner apres

    # On redessine les cellules vivante qui vont arriver a la prochaine etape
    for lig, col in cellulesEnVie2:
        x = (col * celluleSize)
        y = (lig * celluleSize)
        Grille.create_rectangle(x, y, x + celluleSize, y + celluleSize, fill = "#C6C6C6", tags = ((lig, col), "celluleEnVie"))


    cellulesEnVie = dict(cellulesEnVie2) # Cellule actuel deviennent les cellules du futur, "simulation de temps qui passe" avec t et t + 1
    cellulesEnVie2 = {} # On vide
    cellulesExaminees = {} # On vide
    cellulesVoisines = {} # On vide

    #print("\n APRES MAJ : ")
    #print("\nCELLULE EN VIE T : ", cellulesEnVie)
    #print("\nCELLULE EN VIE T + 1 : ", cellulesEnVie2)

    if not cellulesEnVie: # verification au moins une cellule en vie sinon arret
        if(running):
            ArreterBtnEvent()
        return

    # "Animation" avec after()
    if running:
        # 100 -> speed
        Grille.after(100, MiseAJourCellules)

def ChangeModeDeJeu():
    global modeDeJeu

    modeDeJeu += 1
    if modeDeJeu > 3:
        modeDeJeu = 1
        changeMode_textBtn.set("Mode : Jeu de la vie")
    if modeDeJeu == 2:
        changeMode_textBtn.set("Mode : Jeu du jour et de la nuit")
    elif modeDeJeu == 3:
        changeMode_textBtn.set("Mode : Jeu QuadLife")
        

# Dessine le "quadrillage" de la grille (lignes vertical et horizontal).
def CreationGrille():
    global celluleSize
    global nbrCellules

    Grille.delete(ALL) # On supprime tout pour refaire
    ligneSize = celluleSize * nbrCellules # On calcul la taille des lignes en fonction du onombre de cellule et de leur taille
    x = 0 # On commence a 0

    for _j in range(nbrCellules + 1):
        # Creation ligne vertical & horizontal
        Grille.create_line(x, 0, x, ligneSize, fill = grilleCouleur, tags = "ligne")
        Grille.create_line(0, x, ligneSize, x, fill = grilleCouleur, tags = "ligne")
        x += celluleSize

# Reinitialisation de la grille -> on nettoie les cellules en vie et redessine la grille vide.
def ReinitialiseGrille():
    global running
    global cellulesEnVie
    global cellulesEnVie2
    global cellulesExaminees
    global cellulesVoisines

    cellulesEnVie = {} # cellules en vie maintenant
    cellulesEnVie2 = {}  # cellules en vie etape suivante
    cellulesExaminees = {} # cellules deja examinées
    cellulesVoisines = {} # cellules voisine des cellules en vie

    if running:
        ArreterBtnEvent()
    
    CreationGrille()

    #print("\nREINIT\n")

# Event souris click droit sur la grille -> suppression cellule vivante.
def CliqueDroitSurCellule(event):
    global cellulesEnVie
    x, y, lig, col = CalculCoordEtNumLigne(event)
    Grille.delete((lig, col)) # Suppression de la cellule sur la grille

    if (lig, col) in cellulesEnVie: # Si la cellule est bien en vie
        del cellulesEnVie[(lig, col)] #Suppression de la cellule du dictionnaire des cellules en vie

# Event souris click gauche sur la grille -> creation nouvelle cellule vivante.
def CliqueGaucheSurCellule(event):
    global nbrCellules
    global cellulesEnVie

    x, y, lig, col = CalculCoordEtNumLigne(event)
    if lig <= nbrCellules and col <= nbrCellules: # on verifie que lig et col sont sur la grille
        if not (lig, col) in cellulesEnVie: # Si pas encore cree de cellule a cet endroit
            # On rajoute dans le dictionnaire la cellule en vie
            cellulesEnVie.setdefault((lig, col))
            # On montre la cellule en vie graphiquement
            Grille.create_rectangle(x, y, x + celluleSize, y + celluleSize, fill = "#C6C6C6", tags = ((lig, col), "celluleEnVie"))

# Btn demarrer -> demarre "l'animation".
def DemarrerBtnEvent():
    global running

    running = True
    print("Runnig : " + str(running))

    Clear.configure(state=DISABLED) # on desactive le btn clear
    Demarrer.configure(state = DISABLED) # on desactive le btn demarrer
    NextStep.configure(state = DISABLED) # on desactive le btn Avancer prochaine etape

    Grille.itemconfigure("ligne", fill = "black") # Lorsque demarrer, on cache la grille
    MiseAJourCellules()

# Btn arreter -> arrete "l'animation".
def ArreterBtnEvent():
    global running
    global cellulesEnVie2
    global cellulesExaminees
    global cellulesVoisines

    if running:
        running = False
        print("Runnig : " + str(running))
        Clear.configure(state=NORMAL) # on reactive le btn clear
        Demarrer.configure(state = NORMAL) # on reactive le btn demarrer
        NextStep.configure(state = NORMAL) # on reactive le btn Avancer prochaine etape
        
        Grille.itemconfigure("ligne", fill = grilleCouleur) # Lorsque arreter, on remontre la grille
        Grille.configure(bg = "black")

        cellulesEnVie2 = {} # On vide
        cellulesExaminees = {} # On vide
        cellulesVoisines = {} # On vide


### Fenetre TK()
Ecran = Tk()
Ecran.title("Automates cellulaires : Jeu de la vie & Jeu du jour et de la nuit") # Nom de la fenetre
Ecran.geometry("+0+0") # "redimensionnable" par le canvas (la grille)
Ecran.resizable(0, 0) # On peut pas redimensionner la fenetre
Ecran.configure(bg="#484848")

diffecran = 168 # 196 -> 14 (celluleSize) * 12 -> la diff a appliquer pour taille ecran, pour eviter que la fenetre soit coller aux bords
grilleSize = Ecran.winfo_screenheight() - diffecran # On calcul la taille de la grille en fonction de la taille de l'ecran
nbrCellules = int(grilleSize / celluleSize) # nombre de cellule / ligne

### Creation du canvas qui aura la grille contenant les cellules
Grille = Canvas(Ecran, width = grilleSize, height = grilleSize, bg = "black")
Grille.bind("<Button-1>", CliqueGaucheSurCellule) # event click souris gauche
Grille.bind("<Button-3>", CliqueDroitSurCellule) # event click souris droit
Grille.grid(row=1, column=0)
#Grille.pack()

buttonFrame = Frame(Ecran)
buttonFrame.configure(bg="#757575")
buttonFrame.grid(row=2, column=0)


# MODE DE JEU = 1 -> Jeu de la vie
#             = 2 -> Jeu du jour et de la nuit
modeDeJeu = 1

changeMode_textBtn = StringVar()
changeMode_textBtn.set("Mode : Jeu de la vie")

textColor = "White"

Demarrer = Button(buttonFrame, text = "Demarrer", bg = "#38A027", fg = textColor, width = 16, height = 2, takefocus = False, command = DemarrerBtnEvent)
Demarrer.grid(row=2, column = 0, padx=10, pady=4)

NextStep = Button(buttonFrame, text = "Avancer x 1", bg = "#4040D5", fg = textColor, width = 16, height = 2, takefocus = False, command = MiseAJourCellules)
NextStep.grid(row=2, column = 1, padx=10, pady=4)

Arreter = Button(buttonFrame, text = 'Arreter', bg = "#EC8B30", fg = textColor, width = 16, height = 2, takefocus = False, command = ArreterBtnEvent)
Arreter.grid(row=2, column = 2, padx=10, pady=4)

Clear = Button(buttonFrame, text = 'Clear', bg = "#E25DB2", fg = textColor, width = 16, height = 2, takefocus = False, command = ReinitialiseGrille)
Clear.grid(row=2, column = 3, padx=10, pady=4)

Quitter = Button(buttonFrame, text = 'Quitter', bg = "#E82B2B", fg = textColor, width = 16, height = 2, takefocus = False, command = Ecran.destroy)
Quitter.grid(row=2, column = 4, padx=10, pady=4)

ChangeModeJeu = Button(buttonFrame, textvariable = changeMode_textBtn, bg = "#7442B3", fg = textColor, width = 24, height = 2, takefocus = False, command = ChangeModeDeJeu)
ChangeModeJeu.grid(row=2, column = 4, padx=40, pady=4)

CreationGrille()
Ecran.mainloop()
