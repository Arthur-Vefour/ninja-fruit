# Jeu du Serpent en utilisant les fonctions de la librairie Pygame
 
import pygame
import random
import sys
pygame.init()

# Initialisation des variables

fenetre = pygame.display.set_mode( (1000,600) ) # Définition de la taille du terrain de jeu
pygame.display.set_caption("Ninja Fruit")
imagefond = pygame.image.load("fond_jeu.png")
#Initialisation des images
spritefruits = pygame.image.load("fruits.png").convert_alpha()
spritesplahs = pygame.image.load("taches.png")
imagebombe = pygame.image.load("bomb.png")
bombeperdu = pygame.image.load("bombeperdu.png")
fruitperdu = pygame.image.load("fruitperdu.png")
#Initialisation des capteurs souris

click = pygame.mouse.get_pressed()
pos_souris = pygame.mouse.get_pos()

appui = False 
slashs = []
fruits = [] #ici le nom de la variable est mal choisi puisque l'on loge les fruits et les bombes dans la même liste. On pourrait la nommer objet. Cette incohérence est du au regroupement de la liste Bombes et fruits dans une même Variable qui a été fait dans une version ulterieur 
erreur = 0
score = 0
coofruits = [(0,0),(383,0),(2*383,0),(0,383),(383,383)] #Coordonnés de chaque different fruit(graphiquement parlant)
cootaches = [(0,0),(383,0),(2*383,0),(0,383),(383*2,383)]#Marche de paire avec coofruits, on utilisera la même indentation pour définir la couleur de la tache. D'une pière de coup !
taches = []
#Variables assignés à de l'affichage 
impactpolice = pygame.font.SysFont("impact", 40)
texteperdu1 = impactpolice.render("Tu croules sous les fruits!",True,(255,0,0))
texteperdu2 = impactpolice.render("Tu as perdu gros naze !",True,(255,0,0))
texteperdu3 = impactpolice.render("Toute ressemblance avec un événement passé est fortuite",True,(255,255,255))
affichagescore = impactpolice.render("Score:"+str(score),True,(255,0,0))
affichageerreur = impactpolice.render("Fruits loupés"+str(erreur),True,(255,0,0))

#Permet de gérer les images, leur taille, leur redimention, et la portion de l'image que l'on séléctionne
def defsprite(img,x, y, largeur, hauteur, taille):
    image = pygame.Surface((largeur, hauteur), pygame.SRCALPHA).convert_alpha()
    image.blit(img, (0, 0), (x, y, largeur, hauteur))
    image = pygame.transform.scale(image, (largeur * taille, hauteur * taille))
    return image
#Ecran de fin selon la manière dont on a perdu(soit parce que l'on a touché une bombe ou que l'on à loupé un total de 3 fruits)
def dessinerperdu():
    global continuer, erreur,score
    continuer = False
    while continuer ==False :
        texteperdu4 = impactpolice.render("Ton score final : "+str(score),True,(255,0,0))
        if erreur ==3 : #Les erreurs sont les fruits non coupés
            fenetre.blit(imagefond, (0,0)) 
            fenetre.blit(fruitperdu,(0,0))
            fenetre.blit(texteperdu1,(200,25))
            
        else :#Quand on touche une bombe 
            fenetre.blit(bombeperdu,(0,0))
            fenetre.blit(texteperdu2,(100,25))
            fenetre.blit(texteperdu3,(0,550))
            
        fenetre.blit(texteperdu4,(680,25)) #On affiche toujours le score final lors de la mort 
        pygame.display.flip()
        while True :
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    

def dessiner(): 
    global  fenetre, coofruits, erreur 
    fenetre.blit(imagefond, (0,0))
    affichagescore = impactpolice.render("Score: "+str(score),True,(255,0,0))
    affichageerreur = impactpolice.render("Fruits loupés : "+str(erreur)+"/3",True,(255,0,0)) #actualisation des varaibles 
    fenetre.blit(affichagescore,(0,0))
    fenetre.blit(affichageerreur,(700,0))#Affichage du score et des erreurs
    for tache in taches: #affiche les taches selon la couleur du fruit coupé 
        fenetre.blit(defsprite(spritesplahs,cootaches[tache[1]][0],cootaches[tache[1]][1], 383, 383, 0.25),tache[0])
    
    for fruit in fruits :
        if fruit[7]=="fruit": 
            fenetre.blit(defsprite(spritefruits,coofruits[fruit[6]][0],coofruits[fruit[6]][1],383,383,0.25),fruit[1])
        if fruit[7]=="bombe": 
            fenetre.blit(defsprite(imagebombe,0,0,383, 383, 0.25),fruit[1])
    for slash in range (1,len(slashs)):
        #permet de déciné la trainée qui précède la souris quand le click est activé ce qui permet d'imiter un couteau tranchant
        #Le 1, len(slashs) permet d'utiliser l'indentation précédente sans risque d'erreur, maintenant que j'y pense on peut faire avec le suivant s et s+1 ce qui reviendrai au même
          pygame.draw.line(fenetre, (255, 255, 245), slashs[slash-1], slashs[slash], 6)
    pygame.display.flip()



def gererClavierEtSouris(): 
    global pos_souris, continuer,appui,slashs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = 0
    if click[0] == True : #paramètre la trainée blache qui suit le pointeur de la souris quand elle est active
        pos_souris = pygame.mouse.get_pos() #actualise la postition de la souris
        if len(slashs)>5 : 
            slashs.pop(0) #supprime le premier élément de la liste si la trainée est trop longue (ici 5 points)
            slashs.append(pos_souris) #et apprend le point suivant
        else :
            slashs.append(pos_souris) #ici tant le trait est pas composé de 5 points il grandit

    elif click[0]== False : 
        slashs.clear() #efface la trainée quand on ne clique plus

def parabole(objet):
    n, (x, y), vx, vy, t, compteur,nb,choix = objet
    gravity = 0.20 
    x += vx 
    y += vy + gravity * t #on multiplie par le temps pour faire un effet d'accélération lors de la chute
    t += 1
    return (n, (x, y), vx, vy, t, compteur,nb,choix) 
    
def creerfruit(choix) : #Encore une fois creerfruit est une ancienne fonction mais la fonction actuel crée aussi des bombes, ce choix se fait lors du paramétrage de "choix"
    compteur = 0
    nb = 0 
    hauteur = random.choice(["bas","moyen","haut"]) #on va définir l'allure qu'aura la parabole de notre fruit/bombe
    if hauteur == "bas" : 
        vy = -12        #vy est le vecteur qui va permettre de faire une monté dépendamment de la puissance 
    elif hauteur == "moyen":
        vy = -13
    else : 
        vy = -14
    vx = random.choice([1,2,-1,-2]) #vx représente le déplacement totale fait sur l'axe des abcisses(2 type de déplacement, et deux direction différentes)
    x= random.randint(200,800)
    y=600
    if choix == "fruit": #on définit quel est le fruit(banane, poire,pasteque, ou orange) uniquement quand c'est un fruit si c'est une bombe pas besoin de définir il reste à 0
        nb = random.randint(0,4)
    return (0,(x,y),vx,vy,0,compteur,nb,choix)#compteur est le nombre de fois que l'iteme a franchit la bordure, nb est le fruit(banane,pastèque...), et choix le type (fruit ou bombe) 

def niveau(score): # on paramètre le random.randint(1, avec notre fonction en réduisant l'écart pour augmenter la spawn rate
    retour=[0,0] #premier indent correspond au fruits/ le deuxième aux bombes
    if score< 10 : #spawn de base lors du lancement du jeu
        retour[0]  = 60
        retour[1]  = 100
    elif score > 125 : # quand on dépasse le seuil de 125 on à un niveau qui stagne sinon c'est impossible
        retour[0] = 8
        retour[1] = 8
    else : #Pour tout les autres niveaux
        retour[0] = 60 -(score//10)*5 #La division euclidienne du score permet de changer le taux de spawn tout les 10 points
        retour[1] = 100 -(score//10)*5 #Paril pour les bombes mais à un nombre moins important
    return retour

    
         

    

continuer= True 
while continuer: # Cette boucle s'exécute jusqu'à ce que le joueur ferme la fenêtre
    pygame.time.Clock().tick(240) #240 tics permettent une bonne fluidité du jeu et un jeu pas trop lent
    dessiner()
    click = pygame.mouse.get_pressed()#On actualise nos varaibles pour avoir notre position actualisé
    pos_souris = pygame.mouse.get_pos()
    gererClavierEtSouris()
    if random.randint(0, niveau(score)[0]) == 1:#S'occupe du spawn rate des fruits 
        fruits.append(creerfruit("fruit"))
    elif random.randint(0, niveau(score)[1]) == 1:#S'occupe du spawn rate des bombes 
        fruits.append(creerfruit("bombe"))
    
    for i in range(len(fruits)):
        fruit = fruits[i] #pour que ça soit pas chiant a écrire
        if fruit[5] < 2 and fruit[1]!=(-200,-200) : #si le fruit est toujours dans le cadre(est passé une fois pour rentrer et sortir)
            if fruit[1][1]>=600 : 
                fruit= [fruit[0],fruit[1],fruit[2],fruit[3],fruit[4],fruit[5]+1,fruit[6],fruit[7]]
            fruit = parabole(fruit) #On fait faire la fonction Parabole à notre objet (fruit ou bombe) lorsque lui dépace le bas du cadre
        elif fruit[5] == 2 and fruit[1] !=(-200,-200):
            fruit = (fruit[0], (-200, -200), fruit[2], fruit[3], fruit[4], fruit[5],fruit[6],fruit[7]) #Si l'objet à passer le rebord bas 2 fois(lors de la monté puisqu'il apparait en dessouset lorqu'il disparait lors de la retombée) On l'envoie en -200,-200 qui sert de poubelle
            if fruit[7]=="fruit": #Si le l'objet qu'on nomme fruit est bien un fruit et qu'il retombe on le compte comme perdu 
                erreur+=1 
                if erreur == 3: #au bout de 3 erreurs la partie est perdue 
                    dessinerperdu()
        
        fruits[i] = fruit     #je réactualise à la fin  comme je ne voulais pas multiplier les intendations inutiles 


    if click[0] == True :   #Ici j'ai décidé de n'effectuer ces conditions que si on clique pour ne pas mobilisé de la puissance de calcul pour rien
        for j in range(len(fruits)):
            hitbox = pygame.Rect(fruits[j][1][0],fruits[j][1][1], 383*0.25, 383*0.25)# Je définis la hitbox à la taille de mon sprite 
            if hitbox.collidepoint(slashs[-1][0],slashs[-1][1]) == True and fruits[j][7]=="fruit": #pour les fruits de Type "FRUIT" la colision est détécté lors de l'impact avec le dernier point de la liste slashs[]
                score +=1 
                if len(taches)< 5 : #un maximum de 5 taches sur l'écran
                    taches.append((fruits[j][1],fruits[j][6]))#on ajoute à la liste la position.Et l'indentation de la sprite des fruits qui est similaire à celle des taches (banane = tache jaune)
                else :
                    taches.pop(0) #si <5 alors on pop la première ajoutée
                    taches.append((fruits[j][1],fruits[j][6]))
                fruit_temp = list(fruits[j])
                fruit_temp[1] = (-200, -200)
                fruits[j] = tuple(fruit_temp)
            if hitbox.collidepoint(slashs[-1][0],slashs[-1][1]) == True and fruits[j][7]=="bombe": #si collision avec une bombe la partie est perdue
                dessinerperdu()
        
             
        fruits = [fruit for fruit in fruits if fruit[1] != (-200, -200)] #poubelle qui élimine tout les éléments en -200,-200
pygame.quit()
sys.exit()