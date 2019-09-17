# Importeren van de benodigde modules
# import pgzrun
from random import randint

# Pygame Zero functies die in dit spel worden toegepast

def draw():                                                 # De Pygame Zero draw-functie
    global player, aliens, bases, lasers, boss, gameStatus
    screen.blit('background', (0,0))
    if gameStatus == 0:
        # Tonen introductiescherm
        drawCenterText("PYGAME ZERO INVADERS\n\n\nType your name\nThen press Return to start\n(use arrow keys to move - left, right)\n(use space to fire)")
        screen.draw.text(player.name, center=(400,530), owidth=0.5, ocolor=(255,0,0), color=(0,64,255), fontsize=60)
    elif gameStatus == 1:
        # Spelen van het spel
        for idx in range(player.lives): screen.blit("life", (10+idx*32, 10))
        player.image = player.images[player.status//6]
        player.draw()
        for laser in lasers: laser.draw()
        for alien in aliens: alien.draw()
        for base in bases: base.drawClipped()
        if boss.active: boss.draw()
        screen.draw.text(str(score), topright=(780,10), owidth=0.5, ocolor=(255,255,255), color=(0,64,255), fontsize=60)
        screen.draw.text("LEVEL " + str(level), midtop=(400,10), owidth=0.5, ocolor=(255,255,255), color=(0,64,255), fontsize=60)
        if player.status >= 30:
            if player.lives > 0:
                drawCenterText("YOU WERE HIT\nPress Home to re-spawn")
        if len(aliens) == 0:
            drawCenterText("LEVEL CLEARED!\nPress Home to go to the next level")
    elif gameStatus == 2:
        # Tonen van de ranglijst en herstarten spel
        drawHighScore()
        

def update():                                               # De Pygame Zero update-functie
    global player, lasers, level, moveCounter, gameStatus, startGame, MOVEDELAY
    if gameStatus == 0:
        # Tonen introductiescherm
        if startGame:
            gameStatus = 1
    elif gameStatus == 1:
        # Spelen van het spel
        if player.status <= 30 and len(aliens) > 0:
            # Afhandeling tijdens het lopende spel
            checkKeys()
            updateLasers()
            updateBoss()
            moveCounter += 1
            if moveCounter == MOVEDELAY:
                moveCounter = 0
                updateAliens()
            if player.status > 0:
                player.status += 1
        else:
            # Als alle aliens op zijn of de speler is geraakt leggen we het spel stil en wachten we op de <home> toets
            if keyboard.home:
                if len(aliens) == 0:
                    # Speler heeft een level leeg geschoten
                    level += 1
                    initAliens()
                    initBases()
                if player.lives > 0:
                    # Speler is geraakt maar heeft nog levens
                    player.status = 0
                    lasers = []
            if player.status == 31:
                # Speler is geraakt
                player.status += 1
                player.lives -= 1
            if player.lives == 0:
                # Speler is geraakt en het spel is uit
                readHighScore()
                gameStatus = 2
                writeHighScore()
#Test2.2        print(player.status, player.lives)
    elif gameStatus == 2:
        # Tonen van de ranglijst en herstarten spel
        if keyboard.escape:
            init()
            gameStatus = 1


def on_key_down(key):
    global player, gameStatus, startGame
    if gameStatus == 0:
        if key.name != "RETURN":
            if len(key.name) == 1:
                player.name += key.name
                player.name = player.name.capitalize()
            else:
                if key.name == "BACKSPACE":
                    player.name = player.name[:-1]
        elif player.name != "":
            startGame = True


# De hulpfuncties voor dit spel

def init():
    global moveSequence, moveCounter, score, level
    global player, aliens, bases, lasers, boss
    
    # Definitie en initialiseren van globale variabelen 
    moveSequence = 0
    moveCounter = 0
    score = 0
    level = 1

    # Initialisatie van diverse variablen van de Actor player
    player.x = 400
    player.y = 550
    player.status = 0
    player.laserActive = 1
    player.laserCountdown = 0
    player.lives = 3
    player.images = ["player", "explosion1", "explosion2", "explosion3", "explosion4", "explosion5"]

    # Definitie van de overige Actors van het spel
    initAliens()
    initBases()
    lasers = []
    boss = Actor("boss")
    boss.active = False


def initAliens():
    global aliens
    aliens = [Actor("alien1", (210+(idx%6)*80,100+(idx//6)*64)) for idx in range(18)]
    for alien in aliens: alien.status = 0


def initBases():
    global bases
    bases = [Actor("base1", midbottom=(150+(idx//3)*200+(idx%3)*40,520)) for idx in range(9)]
    for base in bases:
        base.drawClipped = drawClipped.__get__(base)
        base.collideLaser = collideLaser.__get__(base)
        base.height = 60


def drawCenterText(_out):
    screen.draw.text(_out, center=(400,300), owidth=0.5, ocolor=(255,255,255), color=(0,64,255), fontsize=60)


def drawHighScore():
    global highScore
    y_pos = 0
    screen.draw.text("TOP SCORES", midtop=(400,30), owidth=0.5, ocolor=(255,255,255), color=(0,64,255), fontsize=60)
    for line in highScore:
        if y_pos < 400:
            screen.draw.text(line, midtop=(400,100+y_pos), owidth=0.5, ocolor=(0,0,255), color=(255,255,0), fontsize=50)
            y_pos += 50
    screen.draw.text("Press Escape to play again", center=(400,550), owidth=0.5, ocolor=(255,255,255), color=(255,64,0), fontsize=60)


def updateAliens():
    global aliens, level, moveSequence, MOVEDELAY
    move_X = 0
    move_Y = 0

    # Bepaal de grootte van de bewegingen
    if moveSequence < 10 or moveSequence > 30: move_X = -15
    if moveSequence == 10 or moveSequence == 30: move_Y = 40 + 5 * level
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
            sounds.laser.play()
            lasers[-1].status = 0
            lasers[-1].type = 0

        # Als een alien is geland is het spel afgelopen
        if alien.y > 500 and player.status == 0:
            player.status = 1
#Test1.13     print(player.status)

    moveSequence += 1
    if moveSequence == MOVEDELAY:
        moveSequence = 0


def updateBoss():
    global boss, level

    if boss.active:
        boss.y += (0.3 * level)
        if boss.direction == 0:
            boss.x -= level
        else:
            boss.x += level
        if boss.x < 100: boss.direction = 1
        if boss.x > 700: boss.direction = 0
        if boss.y > 500:
#Test2.9    print(str(boss.y) + "; sounds reached")
            sounds.explosion.play()
            player.status = 1
            boss.active = False
        if randint(0,30) == 0:
            lasers.append(Actor("laser1", (boss.x, boss.y)))
            sounds.laser.play()
            lasers[-1].status = 0
            lasers[-1].type = 0
    else:
        if randint(0,800) == 0:
            boss.active = True
            boss.x = 800
            boss.y = 100
            boss.direction = 0


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


def readHighScore():
    global highScore, score, player
    highScore = []
    try:
        fileHandler = open("data/highscores.txt", "r")
        for line in fileHandler:
            highScore.append(line.rstrip())
        fileHandler.close()
    except:
        print("highScores.txt does not exist and will be created")
    highScore.append(str(score) + " - " + player.name)
    highScore.sort(key=natural_key, reverse=True)

def natural_key(string_):
    try:
        naturalKey = int(string_[:string_.find(' - ')])
    except:
        naturalKey = 0
#Test2.18    print(naturalKey)
    return naturalKey


def writeHighScore():
    global highScore
    if len(highScore) > 10:
        print("Er zijn te veel scores: Maximaal 10 scores worden bewaard.")
    fileHandler = open("data/highscores.txt", "w")
    for idx in range(10):
        fileHandler.write(highScore[idx] + "\n")
    fileHandler.close()


def checkKeys():
    global player, lasers

#Test1.12    if keyboard.p: print(len(lasers))
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
            sounds.gun.play()
            lasers[-1].status = 0
            lasers[-1].type = 1


def checkAlienLaserHit(_laser):
    global player, bases

    if player.collidepoint((_laser.x, _laser.y)):
        sounds.explosion.play()
        player.status = 1
        _laser.status = 1
    for base in bases:
        if base.collideLaser(_laser):
            base.height -= 10
            _laser.status = 1


def checkPlayerLaserHit(_laser):
    global aliens, bases, boss, score

    for base in bases:
        if base.collideLaser(_laser):
            _laser.status = 1
    for alien in aliens:
        if alien.collidepoint((_laser.x, _laser.y)):
            _laser.status = 1
            alien.status = 1
            score += 1000
    if boss.active:
        if boss.collidepoint((_laser.x, _laser.y)):
            _laser.status = 1
            boss.active = False
            score += 5000
        

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
startGame = False
highScore = []
gameStatus = 0
# Gebruikte waarden voor gameStatus:
#   0 = Tonen van het introductie scherm
#   1 = Spelen van het spel
#   2 = Tonen van het scorebord en het spel opnieuw starten

# Definitie van de Actor player
player = Actor("player", (400,550))
player.name = ""

# Benodigd om het spel te starten
init()
# pgzrun.go()
