# Importeren van de benodigde modules
# import pgzrun
from random import randint

# Pygame Zero functies die in dit spel worden toegepast

def draw():                                                 # De Pygame Zero draw-functie
    global tileList
    screen.fill((150, 100, 200))
    screen.blit('board', (150,50))
    for tile in tileList:
        tile.draw()
    if gameStatus == 0:
        screen.draw.text("Please wait while the image is scrammbled", (120,540), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=40)
    elif gameStatus == 1:
        screen.draw.text("Click on a tile to move it or use the arrow keys", (95,540), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=40)
    elif gameStatus == 3:
        x_pos = 120 - len(str(moveCounter)) * 10
        screen.draw.text("Success, it took "+str(moveCounter)+" moves to solve the puzzle", (x_pos,540), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=40)


def update():                                               # De Pygame Zero update-functie
    global gameStatus
    if gameStatus == 1:
        if keyboard.left: findMoveTile("left")
        if keyboard.right: findMoveTile("right")
        if keyboard.up: findMoveTile("up")
        if keyboard.down: findMoveTile("down")


def on_mouse_down(pos):                                     # Bepaal hier wat er gebeurt als de linker muisknop wordt ingedrukt
    global tileList, gameStatus, moveCounter
    if gameStatus == 1:
        setLock()
        for tile in tileList:
            if tile.collidepoint(pos):
                canMove = moveTile(tile)
                if canMove != False:
                    animate(tile, on_finished=releaseLock, pos=(tile.x+canMove[1], tile.y+canMove[2]))
                    moveCounter += 1
                    return True
        releaseLock()
        

# De hulpfuncties voor dit spel

def scrambleImage():
    global gameStatus, scrambleCounter, moveDone, TILEDIRS, SCRAMBLESTEPS, SCRAMBLELIST

    if scrambleCounter < SCRAMBLESTEPS:
        moveDone = False
        while moveDone == False and scrambleCounter < SCRAMBLESTEPS:
            scrambleCounter += 1
            moveDone = findMoveTile(TILEDIRS[SCRAMBLELIST[scrambleCounter-1]])
#Test17            if moveDone == False:
#Test17                print("Move "+str(scrambleCounter-1)+": "+TILEDIRS[SCRAMBLELIST[scrambleCounter-1]]+" is not possible.")
#Test17                print("No tile could make this move.")
#FinalTest             print(scrambleCounter, gameStatus)
        if scrambleCounter >= SCRAMBLESTEPS: gameStatus = 1
    else:
        gameStatus = 1


def findMoveTile(_direction):
    global moveCounter
    setLock()
    for tile in tileList:
        canMove = moveTile(tile)
        if canMove != False:
            if canMove[0] == _direction:
                animate(tile, on_finished=releaseLock, pos=(tile.x+canMove[1], tile.y+canMove[2]))
                if gameStatus == 2: moveCounter += 1
                return True
    releaseLock()
    return False


def moveTile(_tile):
    global TESTSTEP
    borderRight = 551
    borderLeft = 251
    borderTop = 151
    borderBottom = 451
    rValue = False

    if _tile.x < borderRight:                                # We can try right
        _tile.x += TESTSTEP
        if not checkCollide(_tile):
            rValue = ("right", 100, 0)
        _tile.x -= TESTSTEP
    if _tile.x > borderLeft:                                 # We can try left
        _tile.x -= TESTSTEP
        if not checkCollide(_tile):
            rValue = ("left", -100, 0)
        _tile.x += TESTSTEP
    if _tile.y < borderBottom:                               # We can try down
        _tile.y += TESTSTEP
        if not checkCollide(_tile):
            rValue = ("down", 0, 100)
        _tile.y -= TESTSTEP
    if _tile.y > borderTop:                                  # We can try up
        _tile.y -= TESTSTEP
        if not checkCollide(_tile):
            rValue = ("up", 0, -100)
        _tile.y += TESTSTEP

    return rValue


def setLock():
    global gameStatus
    if gameStatus == 1:
        gameStatus = 2


def releaseLock():
    global gameStatus, moveDone
#Test17    print(gameStatus)
    if gameStatus == 0:
        if moveDone: scrambleImage()
    else:
        gameStatus = checkSuccess()


def checkCollide(_tile):
    global tileList
    for tile in tileList:
        if _tile.colliderect(tile) and _tile != tile:
            return True
    return False

def checkSuccess():
    global tileList, solvedPositions
    currentPositions = [(tile.x,tile.y) for tile in tileList]
    if currentPositions == solvedPositions:
        return 3
    else:
        return 1


# Definitie van constanten en variabelen
WIDTH = 800
HEIGHT = 600
TESTSTEP = 1
TILEDIRS = ["right", "left", "down", "up"]
SCRAMBLESTEPS = 75
#                                   1                   2                   3
#                 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# SCRAMBLELIST = [2,0,2,0,3,1,2,1,3,0,0,2,1,2,1,3,3,0,3,0,2,0,2,2,1,3,1,3,3,1,2]
SCRAMBLELIST = [randint(0,3) for idx in range(SCRAMBLESTEPS)]
#FinalTest print(SCRAMBLELIST)
scrambleCounter = 0
moveDone = False
moveCounter = 0
gameStatus = 0
# Als gamestatus definitie de volgende statussen doorgevoerd:
#   0 = Initialiseren een opbouwen van de geshuffelde puzzel
#   1 = De speler kan een zet invoeren
#   2 = Bezig met het verwerken van de zet, de speler kan nu niet zetten
#   3 = Puzzel opgelost

# Definitie van de actors van het spel en vastleggen van de opgeloste situatie
tileList = [Actor("img"+str(idx), pos=(251+(idx%4)*100, 151+(idx//4)*100)) for idx in range(15)]
solvedPositions = [(tile.x,tile.y) for tile in tileList]

# Benodigd om het spel te starten
scrambleImage()
# pgzrun.go()
