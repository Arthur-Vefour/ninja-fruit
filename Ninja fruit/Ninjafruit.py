# Jeu du Serpent en utilisant les fonctions de la librairie Pygame
 
import pygame
import random
import sys
pygame.init()

# Initialisation des variables

fenetre = pygame.display.set_mode( (1000,600) ) # Définition de la taille du terrain de jeu
pygame.display.set_caption("Ninja Fruit")
imagefond = pygame.image.load("fond_jeu.png")
imagealien = pygame.image.load("alien.png")
click = pygame.mouse.get_pressed()
pos_souris = pygame.mouse.get_pos()
appui = False 
slashs = []
fruits = []
erreur = 0 


 

def dessiner(): # Procédure d'affichage du cercle représentant la tête du serpent
    global serpent, fenetre, pomme
    fenetre.blit(imagefond, (0,0))
    for slash in range (1,len(slashs)): 
          pygame.draw.line(fenetre, (255, 255, 245), slashs[slash-1], slashs[slash], 6)
    for fruit in fruits : 
        fenetre.blit(imagealien,fruit[1])
         
    pygame.display.flip()



def gererClavierEtSouris(): # Procédure de Détection de la frappe clavier du joueur
    global pos_souris, continuer,appui,slashs
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Permet de gérer un clic sur le bouton de fermeture de la fenêtre
            continuer = 0
    if click[0] == True :
        pos_souris = pygame.mouse.get_pos()
        if len(slashs)>5 : 
            slashs.pop(0) 
            slashs.append(pos_souris)
        else :
            slashs.append(pos_souris) 

    elif click[0]== False or len(slashs)>5: 
        slashs.clear()

def parabole(fruit):
    n, (x, y), vx, vy, t, compteur = fruit
    gravity = 0.20
    x += vx
    y += vy + gravity * t
    t += 1
    return (n, (x, y), vx, vy, t, compteur)
    
def creerfruit() : 
    compteur = 0 
    hauteur = random.choice(["bas","moyen","haut"])
    if hauteur == "bas" : 
        vy = -11        #vy est le vecteur qui va permettre de faire une monté dépendamment de la puissance 
    elif hauteur == "moyen":
        vy = -12
    else : 
        vy = -13
    vx = random.choice([1,2,-1,-2]) #vx représente le déplacement totale fait sur l'axe des abcisses
    x= random.randint(200,800)
    y=600 
    return (0,(x,y),vx,vy,0,compteur)
    


continuer = True # Déclaration de la variable
while continuer: # Cette boucle s'exécute jusqu'à ce que le joueur ferme la fenêtre
    pygame.time.Clock().tick(60) # Pas plus de 3 tours de boucle par secondes: i.e.: 3 pas par secondes ou 3 images par secondes
    dessiner()
    click = pygame.mouse.get_pressed()
    pos_souris = pygame.mouse.get_pos()
    gererClavierEtSouris()
    if random.randint(0, 60) == 1:
        fruits.append(creerfruit())
    for i in range(len(fruits)):
        fruit = fruits[i] #pour que ça soit pas chiant a écrire
        if fruit[5] < 2 and fruit[1]!=(-200,-200) : #si le fruit est toujours dans le cadre(est passé une fois pour rentrer et sortir)
            if fruit[1][1]==600 : 
                fruit= [fruit[0],fruit[1],fruit[2],fruit[3],fruit[4],fruit[5]+1]
            fruit = parabole(fruit)
        elif fruit[5] >= 2:
            erreur+=1 
            fruit = (fruit[0], (-200, -200), fruit[2], fruit[3], fruit[4], fruit[5])
        fruits[i] = fruit     #je réactualise à la fin    
    fruits = [fruit for fruit in fruits if fruit[1] != (-200, -200)]
            

        
        
   


    

    




pygame.quit()
sys.exit()