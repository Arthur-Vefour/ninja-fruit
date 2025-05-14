# Jeu du Serpent en utilisant les fonctions de la librairie Pygame
 
import pygame
import random
import sys
pygame.init()

# Initialisation des variables

fenetre = pygame.display.set_mode( (1000,600) ) # Définition de la taille du terrain de jeu
pygame.display.set_caption("Ninja Fruit")
imagefond = pygame.image.load("fond_jeu.png")

spritefruits = pygame.image.load("fruits.png").convert_alpha()
click = pygame.mouse.get_pressed()
pos_souris = pygame.mouse.get_pos()
spritesplahs = pygame.image.load("taches.png")
imagebombe = pygame.image.load("bomb.png")
bombeperdu = pygame.image.load("bombeperdu.png")
fruitperdu = pygame.image.load("fruitperdu.png")
appui = False 
slashs = []
fruits = []
erreur = 0
score = 0
coofruits = [(0,0),(383,0),(2*383,0),(0,383),(383,383)]
cootaches = [(0,0),(383,0),(2*383,0),(0,383),(383*2,383)]
taches = []
impactpolice = pygame.font.SysFont("impact", 40)
texteperdu1 = impactpolice.render("Tu croules sous les fruits!",True,(255,0,0))
texteperdu2 = impactpolice.render("Tu as perdu gros naze",True,(255,0,0))
texteperdu3 = impactpolice.render("Toute ressemblance avec un événement passé est fortuite",True,(255,255,255))
affichagescore = impactpolice.render("Score:"+str(score),True,(255,0,0))
affichageerreur = impactpolice.render("Fruits loupés"+str(erreur),True,(255,0,0))
texteperdu4 = impactpolice.render(str(score),True,(255,0,0))

def defsprite(img,x, y, largeur, hauteur, taille):
    image = pygame.Surface((largeur, hauteur), pygame.SRCALPHA).convert_alpha()
    image.blit(img, (0, 0), (x, y, largeur, hauteur))
    image = pygame.transform.scale(image, (largeur * taille, hauteur * taille))
    return image

def dessinerperdu():
    global continuer, erreur,score
    continuer = False
    while continuer ==False :   
        if erreur ==3 :
            fenetre.blit(imagefond, (0,0)) 
            fenetre.blit(fruitperdu,(0,0))
            fenetre.blit(texteperdu1,(200,25))
            
        else :
            fenetre.blit(bombeperdu,(0,0))
            fenetre.blit(texteperdu2,(100,25))
            fenetre.blit(texteperdu3,(0,550))
            
        fenetre.blit(texteperdu4,(900,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Permet de gérer un clic sur le bouton de fermeture de la fenêtre
                continuer = 0
    
    
    
 

def dessiner(): 
    global serpent, fenetre, pomme, coofruits, erreur 
    fenetre.blit(imagefond, (0,0))
    affichagescore = impactpolice.render("Score: "+str(score),True,(255,0,0))
    affichageerreur = impactpolice.render("Fruits loupés : "+str(erreur),True,(255,0,0))
    fenetre.blit(affichagescore,(0,0))
    fenetre.blit(affichageerreur,(740,0))
    for slash in range (1,len(slashs)): 
          pygame.draw.line(fenetre, (255, 255, 245), slashs[slash-1], slashs[slash], 6)
    for tache in taches: 
        fenetre.blit(defsprite(spritesplahs,cootaches[tache[1]][0],cootaches[tache[1]][1], 383, 383, 0.25),tache[0])  
    for fruit in fruits :
        if fruit[7]=="fruit": 
            fenetre.blit(defsprite(spritefruits,coofruits[fruit[6]][0],coofruits[fruit[6]][1],383,383,0.25),fruit[1])
        if fruit[7]=="bombe":
            fenetre.blit(defsprite(imagebombe,0,0,383, 383, 0.25),fruit[1])
    
    pygame.display.flip()



def gererClavierEtSouris(): 
    global pos_souris, continuer,appui,slashs
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Permet de gérer un clic sur le bouton de fermeture de la fenêtre
            continuer = 0
    if click[0] == True : #paramètre la trainée blache qui suit le pointeur de la souris
        pos_souris = pygame.mouse.get_pos()
        if len(slashs)>5 : 
            slashs.pop(0) #supprime le premier élément de la liste si la trainée est trop longue (ici 5 points)
            slashs.append(pos_souris) #et apprend le point suivant
        else :
            slashs.append(pos_souris) #ici tant le trait est pas composé de 5 points il grandit

    elif click[0]== False or len(slashs)>5: 
        slashs.clear()

def parabole(objet):
    n, (x, y), vx, vy, t, compteur,nb,choix = objet
    gravity = 0.20
    x += vx
    y += vy + gravity * t
    t += 1
    return (n, (x, y), vx, vy, t, compteur,nb,choix)
    
def creerfruit(choix) : 
    compteur = 0
    nb = 0 
    hauteur = random.choice(["bas","moyen","haut"])
    if hauteur == "bas" : 
        vy = -12        #vy est le vecteur qui va permettre de faire une monté dépendamment de la puissance 
    elif hauteur == "moyen":
        vy = -13
    else : 
        vy = -14
    vx = random.choice([1,2,-1,-2]) #vx représente le déplacement totale fait sur l'axe des abcisses
    x= random.randint(200,800)
    y=600
    if choix == "fruit":
        nb = random.randint(0,4)
    
    return (0,(x,y),vx,vy,0,compteur,nb,choix)
def niveauf(score):
    
    if score< 10 :
        retour  = 60
    elif score//10 > 12 :
        retour = 5
    else : 
        retour = 60 -(score//10)*5
    return retour
def niveaub(score):
    
    if score< 10 :
        retour  = 100
    elif score//10 > 20 :
        retour = 5
    else : 
        retour = 100 -(score//10)*5
    return retour
    
         

    

continuer= True 
while continuer: # Cette boucle s'exécute jusqu'à ce que le joueur ferme la fenêtre
    pygame.time.Clock().tick(240) # Pas plus de 3 tours de boucle par secondes: i.e.: 3 pas par secondes ou 3 images par secondes
    dessiner()
    click = pygame.mouse.get_pressed()
    pos_souris = pygame.mouse.get_pos()
    gererClavierEtSouris()
    if random.randint(0, niveauf(score)) == 1:
        fruits.append(creerfruit("fruit"))
    elif random.randint(0, niveaub(score)) == 1:
        fruits.append(creerfruit("bombe"))
    
    for i in range(len(fruits)):
        fruit = fruits[i] #pour que ça soit pas chiant a écrire
        if fruit[5] < 2 and fruit[1]!=(-200,-200) : #si le fruit est toujours dans le cadre(est passé une fois pour rentrer et sortir)
            if fruit[1][1]>=600 : 
                fruit= [fruit[0],fruit[1],fruit[2],fruit[3],fruit[4],fruit[5]+1,fruit[6],fruit[7]]
            fruit = parabole(fruit)
        elif fruit[5] == 2 and fruit[1] !=(-200,-200):
            fruit = (fruit[0], (-200, -200), fruit[2], fruit[3], fruit[4], fruit[5],fruit[6],fruit[7])
            if fruit[7]=="fruit":
                erreur+=1 
                if erreur == 3: 
                    dessinerperdu()
        
        fruits[i] = fruit     #je réactualise à la fin  


    if click[0] == True :   
        for j in range(len(fruits)):
            hitbox = pygame.Rect(fruits[j][1][0],fruits[j][1][1], 383*0.25, 383*0.25)
            if hitbox.collidepoint(slashs[-1][0],slashs[-1][1]) == True and fruits[j][7]=="fruit":
                score +=1
                if len(taches)< 5 : 
                    taches.append((fruits[j][1],fruits[j][6]))
                else :
                    taches.pop(0) 
                    taches.append((fruits[j][1],fruits[j][6]))
                fruit_temp = list(fruits[j])
                fruit_temp[1] = (-200, -200)
                fruits[j] = tuple(fruit_temp)
            if hitbox.collidepoint(slashs[-1][0],slashs[-1][1]) == True and fruits[j][7]=="bombe":
                dessinerperdu()
        
             
        fruits = [fruit for fruit in fruits if fruit[1] != (-200, -200)]
        
affichagescore = impactpolice.render("Score: "+str(score),True,(255,0,0))
        

            

pygame.quit()
sys.exit()