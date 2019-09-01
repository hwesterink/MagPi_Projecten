# Importeer de benodigde modules
from random import randint

# Initialisatie van konstanten en variabelen
WIDTH = 700
HEIGHT = 800
SPEED = 4
car = Actor("racecar")
car.pos = (250, 500)
trackLeft = []
trackRight = []
trackCount = 0
trackPosition = 250
trackWidth = 120
trackDirection = False
gameStatus = 0

# Definieer functies
def draw():                             # Pygame Zero draw functie
    global gameStatus
    screen.fill((128, 128, 128))
    if gameStatus == 0:
        car.draw()
        for idx in range(len(trackLeft)):
            trackLeft[idx].draw()
            trackRight[idx].draw()
    if gameStatus == 1:                 # Rode vlag
        screen.blit("rflag", (300, 268))
    if gameStatus == 2:                 # Finish vlag
        screen.blit("cflag", (300, 268))

def update():                           # Pygame Zero update functie
    global trackCount, gameStatus
    if gameStatus == 0:
        if keyboard.left: car.x -= 2
        if keyboard.right: car.x += 2
        updateTrack()
    if trackCount > 200:
        gameStatus = 2                  # Geef finish vlag

def makeTrack():                        # Functie om een nieuwe sectie van de weg te maken
    global trackCount, trackLeft, trackRight, trackPosition, trackWidth
    trackLeft.append(Actor("barrier", pos=(trackPosition-trackWidth,0)))
    trackRight.append(Actor("barrier", pos=(trackPosition+trackWidth,0)))
    trackCount += 1

def updateTrack():                      # Functie die bijwerkt waar de grenzen van de weg verschijnen
    global trackCount, trackPosition, trackDirection, trackWidth, gameStatus
    for idx in range(len(trackLeft)):
        if car.colliderect(trackLeft[idx]) or car.colliderect(trackRight[idx]):
            gameStatus = 1              # Bij botsing: Geef de rode vlag
        trackLeft[idx].y += SPEED
        trackRight[idx].y += SPEED
    if trackLeft[len(trackLeft)-1].y > 32:
        if trackDirection: trackPosition -= 16
        else: trackPosition += 16
        if randint(0, 4) == 1: trackDirection = not trackDirection
        if trackPosition > (700 - trackWidth): trackDirection = True
        if trackPosition < trackWidth: trackDirection = False
        makeTrack()

# Start met het maken van de eerste sectie van de weg
makeTrack()
