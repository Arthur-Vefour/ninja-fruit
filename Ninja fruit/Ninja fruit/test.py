 
import pygame
import random
import sys
pygame.init()

fenetre = pygame.display.set_mode( (1000,600) ) # Définition de la taille du terrain de jeu 
pygame.display.set_caption("Ninja Fruit") 
spritefruits = pygame.image.load("fruits.png").convert_alpha()


def defsprite(img,x, y, largeur, hauteur, taille):
    image = pygame.Surface((largeur, hauteur), pygame.SRCALPHA).convert_alpha()
    image.blit(img, (0, 0), (x, y, largeur, hauteur))
    image = pygame.transform.scale(image, (largeur * taille, hauteur * taille))
    return image







def gererClavierEtSouris(): # Procédure de Détection de la frappe clavier du joueur
    global pos_souris, continuer,appui,slashs
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Permet de gérer un clic sur le bouton de fermeture de la fenêtre
            continuer = 0
def dessiner(): 
    fenetre.fill( (10,10,10) )
    pygame.display.flip()



continuer = True # Déclaration de la variable
while continuer: # Cette boucle s'exécute jusqu'à ce que le joueur ferme la fenêtre
    pygame.time.Clock().tick(6) # Pas plus de 3 tours de boucle par secondes: i.e.: 3 pas par secondes ou 3 images par secondes
    dessiner()
    gererClavierEtSouris()
    defsprite(spritefruits,0, 0, 383, 383, 1)