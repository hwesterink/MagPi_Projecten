# Importeren van de benodigde modules
# import pgzrun
from random import randint

# Pygame Zero functies die in dit spel worden toegepast

def draw():                                                 # De Pygame Zero draw-functie
    global player, aliens, bases, lasers
    screen.blit('background', (0,0))
    player.image = player.images[player.status//6]
    player.draw()
    for laser in lasers: laser.draw()
    for alien in aliens: alien.draw()
    for base in bases: base.drawClipped()
    screen.draw.text(str(score), topright=(780,10), owidth=0.5, ocolor=(255,255,255), color=(0,64,255), fontsize=60)
    if player.status >= 30:
        screen.draw.text("GAME OVER\nPress Home to Play Again", center=(400,300), owidth=0.5, ocolor=(255,255,255), color=(0,64,255), fontsize=60)
    if len(aliens) == 0:
        screen.draw.text("YOU WON!\nPress Home to Play Again", center=(400,300), owidth=0.5, ocolor=(255,255,255), color=(0,64,255), fontsize=60)
        

def update():                                               # De Pygame Zero update-functie
    global moveCounter, MOVEDELAY
    if player.status <= 30 and len(aliens) > 0:
        checkKeys()
        updateLasers()
        moveCounter += 1
        if moveCounter == MOVEDELAY:
            moveCounter = 0
            updateAliens()
        if player.status > 0:
            player.status += 1
    else:
        if keyboard.home: init()


# De hulpfuncties voor dit spel

def init():
    global moveSequence, moveCounter, score
    global player, aliens, bases, lasers
    
    # Definitie en initialiseren van globale variabelen 
    moveSequence = 0
    moveCounter = 0
    score = 0

    # Definitie van de actors van het spel
    player = Actor("player", (400,550))
    player.status = 0
    player.laserActive = 1
    player.laserCountdown = 0
    player.images = ["player", "explosion1", "explosion2", "explosion3", "explosion4", "explosion5"]
    aliens = [Actor("alien1", (210+(idx%6)*80,100+(idx//6)*64)) for idx in range(18)]
    for alien in aliens: alien.status = 0
    bases = [Actor("base1", midbottom=(150+(idx//3)*200+(idx%3)*40,520)) for idx in range(9)]
    for base in bases:
        base.drawClipped = drawClipped.__get__(base)
        base.collideLaser = collideLaser.__get__(base)
        base.height = 60
    lasers = []


def updateAliens():
    global aliens, moveSequence, MOVEDELAY
    move_X = 0
    move_Y = 0

    # Bepaal de grootte van de bewegingen
    if moveSequence < 10 or moveSequence > 30: move_X = -15
    if moveSequence == 10 or moveSequence == 30: move_Y = 50
    if moveSequence > 10 and moveSequence < 30: move_X = 15

    for alien in aliens:
        # Voer de bewegingen uit
        animate(alien, pos=(alien.x+move_X, alien.y+move_Y), duration=0.5, tween='linear')
        if randint(0,1):
            alien.image = "alien1"
        else:
            alien.image = "alien1b"

        # Laat de aliens hun lasers afschieten
        if randint(0,5) == 0:
            lasers.append(Actor("laser1", (alien.x, alien.y)))
            lasers[-1].status = 0
            lasers[-1].type = 0

        # Als een alien is geland is het spel afgelopen
        if alien.y > 500 and player.status == 0:
            player.status = 1
#Test13     print(player.status)

    moveSequence += 1
    if moveSequence == MOVEDELAY:
        moveSequence = 0


def updateLasers():
    global lasers, aliens, DIFFICULTY
    for laser in lasers:
        
        if laser.type == 0:                                 # Laser afgeschoten door een alien
            laser.y += 2 * DIFFICULTY
            checkAlienLaserHit(laser)
            if laser.y > 600:
                laser.status = 1

        if laser.type == 1:                                 # Laser afgeschoten door de speler
            laser.y -= 5
            checkPlayerLaserHit(laser)
            if laser.y < 10:
                laser.status = 1

    # Ruim vernietigde lasers en aliens op
    lasers = listCleanup(lasers)
    aliens = listCleanup(aliens)


def checkKeys():
    global player, lasers

#Test12    if keyboard.p: print(len(lasers))

    # Check voor de bewegingen van de speler
    if keyboard.left:
        if player.x > 40: player.x -= 5
    if keyboard.right:
        if player.x < 760: player.x += 5

    # Check voor het schieten door de speler
    if keyboard.space:
        if player.laserActive == 1:
            player.laserActive = 0
            clock.schedule(makeLaserActive, 1.0)
            lasers.append(Actor("laser2", (player.x, player.y-32)))
            lasers[-1].status = 0
            lasers[-1].type = 1


def checkAlienLaserHit(_laser):
    global player, bases

    if player.collidepoint((_laser.x, _laser.y)):
        player.status = 1
        _laser.status = 1
    for base in bases:
        if base.collideLaser(_laser):
            base.height -= 10
            _laser.status = 1


def checkPlayerLaserHit(_laser):
    global aliens, bases, score

    for base in bases:
        if base.collideLaser(_laser):
            _laser.status = 1
    for alien in aliens:
        if alien.collidepoint((_laser.x, _laser.y)):
            _laser.status = 1
            alien.status = 1
            score += 1000
        

def listCleanup(_list):
    newList = []
    for item in _list:
        if item.status == 0:
            newList.append(item)
    return newList


def makeLaserActive():
    global player
    player.laserActive = 1


# Uitbreiding van de Pygame Zero functies t.b.v. onze bases
def drawClipped(self):
    screen.surface.blit(self._surf, (self.x-32, self.y-self.height+30), (0,0,64,self.height))


def collideLaser(self, other):
    return ( self.x-20 < other.x+5 and
             self.y-self.height+30 < other.y and
             self.x+32 > other.x+5 and
             self.y-self.height+30+self.height > other.y ) 


# Definitie en initalisatie van constanten
MOVEDELAY = 40
DIFFICULTY = 1

# Benodigd om het spel te starten
init()
# pgzrun.go()
