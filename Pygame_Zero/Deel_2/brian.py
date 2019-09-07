# Importeren van de benodigde modules
from random import randint
# import pgzrun

# De functies voor het spel


def draw():                                                 # Functie draw() voor Pygame Zero
    global myButtons, playButton, gameStatus, cycleCounter, score, buttonsLit, buttonsUnlit

    # Algemene draw opdrachten voor alle statussen
    screen.fill((30, 10, 30))
    for idx in range(4):
        if myButtons[idx].state: myButtons[idx].image = buttonsLit[idx]
        else: myButtons[idx].image = buttonsUnlit[idx]
    for slice in myButtons:
        slice.draw();

    if gameStatus == 0:
        # Status 0 ==> NOT_STARTED_YET
        screen.draw.text("Press Play to Start", (220, 20), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=60)
        playButton.draw()
        screen.draw.text("Play", (370, 525), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=40)
    elif gameStatus == 1:
        # Status 1 ==> PLAYBUTTON_PRESSED
        screen.draw.text("Initializing Game", (240, 20), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=60)
        screen.draw.text("Score 0", (330, 525), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=40)
    elif gameStatus == 2:
        # Status 2 ==> PLAYING_ANIMATION
        screen.draw.text("Watch", (350, 20), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=60)
        if score > 100:
            x_pos = 270
        elif score > 10:
            x_pos = 280
        else:
            x_pos = 290
        screen.draw.text("Current Score = "+str(score), (x_pos, 525), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=40)
    elif gameStatus == 3:
        # Status 3 ==> PLAYER_ENTERS_CHOICES
        screen.draw.text("Now You", (310, 20), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=60)
        screen.draw.text("Press Slice to Select", (270, 525), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=40)
    elif gameStatus == 4:
        # Status 4 ==> WRONG_CHOICE
        screen.draw.text("Wrong Choice!", (20, 20), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=60)
        if score > 100:
            x_pos = 440
        elif score > 10:
            x_pos = 460
        else:
            x_pos = 480
        screen.draw.text("Final Score = "+str(score), (x_pos, 20), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=60)
        x_pos = enterFromLeft(230)
        screen.draw.text("Press Play for New Game", (x_pos, 350), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=40)
        playButton.draw()
        screen.draw.text("Play", (370, 525), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=40)
    elif gameStatus == 5:
        # Status 5 ==> ALL_CHOICES_RIGHT
        screen.draw.text("Good Job! - Next Round Starting", (100, 20), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=60)
        x_pos = 290 - ( score // 10 ) * 10
        if score > 100:
            x_pos = 270
        elif score > 10:
            x_pos = 280
        else:
            x_pos = 290
        screen.draw.text("Current Score = "+str(score), (x_pos, 525), owidth=0.5, ocolor=(255,255,255), color=(255,128,0), fontsize=40)


def update():                                               # Functie update voor Pygame Zero
    global myButtons, buttonList, playerInput, gameStatus, cycleCounter, score

    if gameStatus == 1:
        # Status 1 ==> PLAYBUTTON_PRESSED
        if cycleCounter == 0:
            score = 0
            buttonList.clear()
            clearButtons()
        cycleCounter += 1
        if cycleCounter == LOOPDELAY:
            cycleCounter = 0
            gameStatus = 2
    elif gameStatus == 2:
        # Status 2 ==> PLAYING_ANIMATION
        if cycleCounter == 0:
            addButton()
            playerInput.clear()
        # Now playing the animation
        cycleCounter += 1
        listPos = cycleCounter // LOOPDELAY
        if listPos == len(buttonList):  # Animatie uitgespeeld
            gameStatus = 3
            clearButtons()
        else:                           # Afspelen van de animatie
            litButton = buttonList[listPos]
            if float(cycleCounter%LOOPDELAY) > (1-PAUZE) * LOOPDELAY: myButtons[litButton].state = False
            else: myButtons[litButton].state = True
    elif gameStatus == 3:
        # Status 3 ==> PLAYER_ENTERS_CHOICES
        if checkPlayerInput() == 1:     # Speler gaf de juiste input
            cycleCounter = 0
            gameStatus = 5
        elif checkPlayerInput() == 2:   # Speler heeft een foute button geklikt
            cycleCounter = 0
            gameStatus = 4
    elif gameStatus == 4:
        # Status 4 ==> WRONG_CHOICE
        cycleCounter += 1
    elif gameStatus == 5:
        # Status 5 ==> ALL_CHOICES_RIGHT
        if cycleCounter == 0:
            score += 1
        cycleCounter += 1
        if cycleCounter == LOOPDELAY:
            cycleCounter = 0
            gameStatus = 2


def on_mouse_down(pos):                                     # Functie on_mouse_down voor Pygame Zero
    global myButtons, gameStatus
    if gameStatus == 3:
        # Status 3 ==> PLAYER_ENTERS_CHOICES
        clearButtons()
        for idx in range(len(myButtons)):
            if myButtons[idx].collidepoint(pos):
                myButtons[idx].state = True


def on_mouse_up(pos):                                       # Functie on_mouse_up voor Pygame Zero
    global myButtons, playButton, gameStatus, cycleCounter, playerInput, score
    if gameStatus == 0:
        # Status 0 ==> PLAYBUTTON_PRESSED
        if playButton.collidepoint(pos):
            gameStatus = 1
    if gameStatus == 3:
        # Status 3 ==> PLAYER_ENTERS_CHOICES
        for idx in range(len(myButtons)):
            if myButtons[idx].collidepoint(pos):
                playerInput.append(idx)
                clearButtons()
    elif gameStatus == 4:
        # Status 4 ==> WRONG_CHOISE
        if playButton.collidepoint(pos):
            cycleCounter = 0
            gameStatus = 1


# Ondersteunende hulpfuncties
def addButton():
    global buttonList
    buttonList.append(randint(0,3))

def clearButtons():
    global myButtons
    for slice in myButtons: slice.state = False

def checkPlayerInput():
    global playerInput, buttonList
    for idx in range(len(playerInput)):
        if playerInput[idx] != buttonList[idx]:
            # Er is een foute button geselecteerd
            return 2
    if len(playerInput) == len(buttonList):
        # Speler heeft alle buttons goed geselecteerd
        return 1
    return 0

def enterFromLeft(_endPos):
    global cycleCounter, WIDTH, LOOPDELAY, TEXTDELAY
    startPos = - ( WIDTH - (2 * _endPos))
    rangeToMove = abs(startPos) + _endPos
    if cycleCounter < TEXTDELAY * LOOPDELAY:
        return startPos + int(rangeToMove * cycleCounter / (TEXTDELAY * LOOPDELAY) )
    else:
        return _endPos


# Initialiseren en definieren van konstanten en variabelen
WIDTH = 800
HEIGHT = 600
LOOPDELAY = 80
TEXTDELAY = 3
PAUZE = 0.25

myButtons = []
buttonsLit = ['redlit', 'greenlit', 'bluelit', 'yellowlit']
buttonsUnlit = ['redunlit', 'greenunlit', 'blueunlit', 'yellowunlit']
buttonList = []
playerInput = []
gameStatus = 0
cycleCounter = 0
score = 0


# Voorbereiden Actors voor het spel
myButtons.append(Actor('redunlit', bottomright=(400,270)))
myButtons[0].state = False
myButtons.append(Actor('greenunlit', bottomleft=(400,270)))
myButtons[1].state = False
myButtons.append(Actor('blueunlit', topright=(400,270)))
myButtons[2].state = False
myButtons.append(Actor('yellowunlit', topleft=(400,270)))
myButtons[3].state = False
playButton = Actor('play', pos=(400,540))

#test14 buttonList = [0,1,2,3]
#test14 playAnimation()
#test15 addButton()
#test15 addButton()
#test15 addButton()
#test15 playAnimation()
# pgzrun.go()
