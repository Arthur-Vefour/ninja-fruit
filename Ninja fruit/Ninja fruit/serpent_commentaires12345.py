# Jeu du Serpent en utilisant les fonctions de la librairie Pygame
 
import pygame
import random
import sys
pygame.init()

# Initialisation des variables

fenetre = pygame.display.set_mode( (600,600) ) # Définition de la taille du terrain de jeu
pygame.display.set_caption("Le jeu du serpent")


direction ="nord"
pomme=(10*random.randint(1,59),10*random.randint(1,59))
arial24 = pygame.font.SysFont("arial",24)
texteperdu = arial24.render("GAME OVER GROS NUL",True,(255,0,0))
serpent=[(300,300)]


def dessiner(): # Procédure d'affichage du cercle représentant la tête du serpent
    global serpent, fenetre, pomme
    fenetre.fill((0,0,0))
    pygame.draw.circle(fenetre, (212,0,0), pomme, 5)
    for i in range(0,len(serpent)):
        position = serpent[i]
        pygame.draw.circle(fenetre, (0,200,0), position, 5) # dessine le cercle de centre position et de rayon 5
    pygame.draw.rect(fenetre, (255,255,255), (0,0,600,600), width=5) 
    pygame.display.flip()

def dessinerperdu():
    fenetre.fill((0,0,0))
    fenetre.blit(texteperdu, (40,300)) 
    pygame.display.flip()
    pygame.time.wait(3000) 

def gererClavierEtSouris(): # Procédure de Détection de la frappe clavier du joueur
    global direction, continuer
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and direction != "ouest":
                direction = "est"
            if event.key == pygame.K_LEFT and direction != "est":
                direction = "ouest"
            if event.key == pygame.K_UP and direction != "sud":
                direction = "nord"
            if event.key == pygame.K_DOWN and direction != "nord":
                direction = "sud"



continuer = True # Déclaration de la variable
while continuer: # Cette boucle s'exécute jusqu'à ce que le joueur ferme la fenêtre
    pygame.time.Clock().tick(5) # Pas plus de 3 tours de boucle par secondes: i.e.: 3 pas par secondes ou 3 images par secondes
    dessiner() 
    gererClavierEtSouris()
    print(serpent)

    pas = 10 # Longueur du déplacement du cercle
    dernierePosition = serpent[0] # Mémorisation de la dernière position du cercle (abscisse,ordonnée)

    if direction == "nord":
        serpent.insert(0, (dernierePosition[0],dernierePosition[1] - pas) ) # 0 pour la première position du tableau et donnée de la nouvelle valeur de la position du serpent.
    elif direction == "sud":
        serpent.insert(0, (dernierePosition[0],dernierePosition[1] + pas) )
    elif direction == "est":
        serpent.insert(0, (dernierePosition[0] + pas,dernierePosition[1]) )
    elif direction == "ouest":
        serpent.insert(0, (dernierePosition[0] - pas,dernierePosition[1]) )
    
    if serpent[0]==pomme:
        pomme=(10*random.randint(1,59),10*random.randint(1,59))
        if pomme in serpent:
            pomme=(10*random.randint(1,59),10*random.randint(1,59))
    else:
        serpent.pop()
    
    if serpent[0][0]>595 or serpent[0][0]<5 or serpent[0][1]>595 or serpent[0][1]<5 or serpent[0] in serpent[1:]:
        dessinerperdu()
        serpent = [ (300,300) ]
        direction = "nord"



pygame.quit()
sys.exit()