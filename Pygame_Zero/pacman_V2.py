# Importeren van de voor het spel noodzakelijke modules
# import pgzrun
from datetime import datetime
from random import randint

##########################################################
# import gameinput_V2
# Omdat bovenstaand statement niet werkt wordt de inhoud
# van gameinput hier opgenomen
##########################################################

# Importeren van voor dit onderdeel noodzakelijke modules
from pygame import joystick, key
from pygame.locals import *

# Functies van de gameinput module
def checkInput(p):
    """
    De checkInput functie controleert de gameinput. Als er een joystick is wordt de input daarvan
    gebruikt. Is er geen joystick, dan gebruikt deze functie de LEFT-, RIGHT-, UP- en DOWN-toetsen
    voor de besturing van de Player.
    Invoer:  'p' = Het object player uit het spel (de Actor)
    """
    global joyin, joystick_count
#Test1.7    global counter

    # Handel de toetsen of voor het bewegen van de speler
    p.movex = p.movey = p.angle = 0
    x_axis = y_axis = 0
    if joystick_count != 0:
        x_axis = joyin.get_axis(0)
        y_axis = joyin.get_axis(1)
    if key.get_pressed()[K_LEFT] or x_axis < -0.8:
        p.angle = 180
        p.movex = -20
    elif key.get_pressed()[K_RIGHT] or x_axis > 0.8:
        p.angle = 0
        p.movex = 20
    elif key.get_pressed()[K_UP] or y_axis < -0.8:
        p.angle = 90
        p.movey = -20
    elif key.get_pressed()[K_DOWN] or y_axis > 0.8:
        p.angle = 270
        p.movey = 20
#Test1.7    counter += 1
#           if counter % 100 == 0:
#               print(counter, x_axis, y_axis, p.angle, p.movex, p.movey)

    # Handel de RETURN af voor het starten van het volgende leven van de speler
    restartButton = False
    if joystick_count != 0:
        restartButton = joyin.get_button(1)
# Vastgesteld in stap 2.9 - Waarden van de buttons op de gamepad:
#    Button X = 0
#    Button A = 1
#    Button B = 2
#    Button Y = 3
#    Button L = 4
#    Button R = 5
#    Button SELECT = 8
#    Button START = 9
#Test2.7  print(p.status, key.get_pressed()[K_RETURN], restartButton, (p.status == 1 and (key.get_pressed()[K_RETURN] or restartButton))
    return (p.status == 1 and (key.get_pressed()[K_RETURN] or restartButton))
        

# Inhoud gameinput module
joystick.init()
joystick_count = joystick.get_count()
#Test1.5 print(joystick_count)

if joystick_count != 0:
    joyin = joystick.Joystick(0)
    joyin.init()
    
##########################################################


##########################################################
# import gamemaps
# Omdat bovenstaand statement niet werkt wordt de inhoud
# van gamemaps hier opgenomen
##########################################################

# Importeren van voor dit onderdeel noodzakelijke modules
from pygame import image, Color

# Functies van de gamemap module
def checkMovePoint(p):
    """
    De checkMovePoint functie controleert of de ingegeven beweging van de Player mogelijk is. De functie
    zorgt ervoor dat de zwarte lijnen van de pacmanmovemap gevolgd worden.
    Invoer:  'p' = Het object player uit het spel (de Actor)
    """
    global moveImage

    newX = p.x + p.movex
    newY = p.y + p.movey - 80
    if newX < 0: p.x += 600; newX += 600
    if newX > 600: p.x -= 600; newX -= 600
    if moveImage.get_at((int(newX), int(newY))) != Color('black'):
        p.movex = p.movey = 0
    

def getPossibleDirections(ghost):
    """
    De getPossibleDirections functie creeert een lijst van mogelijke richtingen waar in een spook zich kan
    bewegen vanuit zijn huidige positie.
    Invoer:  'ghost' = Het object ghost dat onderzocht moet worden
    Uitvoer: directions = lijst met 4 nullen en eenen
                        0 -> beweging niet mogelijk; 1 -> beweging mogelijk
                        opbouw lijst: ['rechts', 'omlaag', 'links', 'omhoog']
    """
    global moveImage
    x_pos = ghost.x
    y_pos = ghost.y
    directions = [0,0,0,0]
    if moveImage.get_at((int((x_pos+20)%600),int(y_pos-80))) == Color('black'): directions[0] = 1
    if moveImage.get_at((int(x_pos),int((y_pos-60)%579))) == Color('black'): directions[1] = 1
    if moveImage.get_at((int((x_pos-20)%600),int(y_pos-80))) == Color('black'): directions[2] = 1
    if moveImage.get_at((int(x_pos),int((y_pos-100)%579))) == Color('black'): directions[3] = 1
    return directions
    

# Inhoud gameinput module
moveImage = image.load('images/pacmanmovemap.png')

##########################################################


# Pygame Zero functies die gebruikt worden in het spel
def draw():
    """
    De draw functie tekent het spel binnen het speelveld
    """
    global player, pacDots, ghosts, gameStatus
    
    screen.blit('header', (0,0))
    screen.blit('colourmap', (0,80))

    if gameStatus == 1:
        
        # Teken de resterende leven en de score
        for idx in range(player.lives):
            screen.blit("player", (10+(idx*32),40))
        screen.draw.text("Score: "+str(player.score), topright=(590,25), owidth=0.5, ocolor=(255,255,255), color=(0,64,255), fontsize=30)

        if player.status == 0:
            # Teken het scherm tijdens het spelen van het spel
            getPlayerImage()
            player.draw()

            # Teken de nog eetbare dots en beeindig het spel als alle dots op zijn
            pacDotsLeft = 0
            for dot in pacDots:
                if dot.status == 0:
                    if dot.collidepoint((player.x, player.y)):
                        dot.status = 1
                        if dot.type == 1:
                            player.score += 10
                        else:
                            for ghost in ghosts:
                                ghost.status = 1200
                    else:
                        dot.draw()
                        pacDotsLeft += 1
            if pacDotsLeft == 0: player.status = 2

            # Teken de geesten
            for idx in range(len(ghosts)):
                if ghosts[idx].x > player.x:
                    if ghosts[idx].status > 200 or (ghosts[idx].status > 1 and (ghosts[idx].status % 2) == 0):
                        ghosts[idx].image = "ghost5r"
                    else:
                        ghosts[idx].image = "ghost" + str(idx+1) + "r"
                else:
                    if ghosts[idx].status > 200 or (ghosts[idx].status > 1 and (ghosts[idx].status % 2) == 0):
                        ghosts[idx].image = "ghost5"
                    else:
                        ghosts[idx].image = "ghost" + str(idx+1)
                ghosts[idx].draw()

        elif player.status == 1:
            # Teken het scherm als de speler gevangen is
            drawCenterText("CAUGHT!\nPress <ENTER> or Button A\nto Continue")
#Test2.7    print("Draw bij player status 1")

        # Handel de einde spel situaties af
        elif player.status == 2:
            screen.draw.text("YOU WIN!", center=(300,434), owidth=0.5, ocolor=(255,255,255), color=(255,64,0), fontsize=40)
        elif player.status == 3:
            screen.draw.text("GAME OVER", center=(300,434), owidth=0.5, ocolor=(255,255,255), color=(255,64,0), fontsize=40)
    

def update():
    """
    De update functie werkt de inhoud van het scherm bij
    """
    global player, moveGhostsFlag, ghosts, gameStatus, SPEED

    if gameStatus == 1:
        
        if player.status == 0:
            
            # We kunnen het spel alleen spelen als de spelerstatus 0 is

            if moveGhostsFlag == 4:
                # Alleen bij moveGhostsFlag vier laten we de geesten bewegen
                moveGhosts()
                
            for ghost in ghosts:

                # Wanneer het spook een status > 0 heeft (de speler kan hem dan vangen) verlagen we de status geleidelijk terug naar nul
                if ghost.status > 0: ghost.status -= 1

                # Als de speler een spook raakt hangt het van de status van het spook af wat er gebeurt
                if ghost.collidepoint((player.x,player.y)):
                    if ghost.status == 0:
                        player.lives -= 1
                        if player.lives > 0:
                            player.status = 1
                        else:
                            player.status = 3
                    else:
                        player.score += 100
                        ghost.respawning = True

            # Verplaats de speler alleen als er geen speleranimatie meer loopt
            if player.inputActive:
                checkInput(player)
                checkMovePoint(player)
                if player.movex != 0 or player.movey != 0:
                    inputLock()
                    animate(player, pos=(player.x+player.movex, player.y+player.movey), duration=1/SPEED, tween='linear', on_finished=inputUnlock)

        elif player.status == 1:

            # Wacht op RETURN of button A van de speler, zet de spoken terug naar hun startposities en speel daarna verder met een leven minder
            invoerControle = checkInput(player)
#Test2.7    print(invoerControle)
            if invoerControle:
                # Zet de speler op zijn uitgangspositie
                player.status = 0
                player.x = 290
                player.y = 570
                # En zet de spoken terug naar het centrum voor de herstart
                initGhosts()
                

def init():
    """
    De init functie initialiseert de variabelen inhet spel
    """
    global player, pacDots, ghosts
    
    # Definieren van de player voor het spel
    player = Actor("pacman_o0")
    player.inputActive = True
    player.x = 290
    player.y = 570
    player.status = 0
    player.score = 0
    player.lives = 3

    # Definieren van de dots voor het spel
    dotImage = image.load("images/pacmandotmap.png")
    pacDots = []
    for idx_x in range(30):
        for idx_y in range(29):
            positionOnMap = (10+idx_x*20, 10+idx_y*20)
            position = (10+idx_x*20, 90+idx_y*20)
            if dotImage.get_at(positionOnMap) == Color('black'):
                pacDots.append(Actor('dot', position))
                pacDots[-1].status = 0
                pacDots[-1].type = 1
            elif dotImage.get_at(positionOnMap) == Color('red'):
                pacDots.append(Actor('power', position))
                pacDots[-1].status = 0
                pacDots[-1].type = 2

    # Definieren van de spoken
    initGhosts()

    
# Hulpfuncties voor dit spel
def initGhosts():
    """
    De initGhosts functie wordt telkens gebruikt wanneer het speelveld opnieuw wordt opgestart, bv. bij een nieuw leven
    """
    global ghosts, GHOSTSTARTUPS, ghostsStartupCounter, moveGhostsFlag
    ghostsStartupCounter = 0
    moveGhostsFlag = 4
    ghosts = [Actor("ghost"+str(idx+1), (270+idx*20,370)) for idx in range(4)]
    for idx in range(len(ghosts)):
        ghosts[idx].sequence = GHOSTSTARTUPS[idx]
        ghosts[idx].status = 0
        ghosts[idx].respawning = False



def getPlayerImage():
    """
    De functie getPlayerImage selecteert de juist geplaatste afbeelding van de pacman
    """
    global player, SPEED
#Test1.13    global counter

    dt = datetime.now()
    testAngle = player.angle
    
    # We willen een float genereren tussen 0 en 5 afhankelijk van de tijd en de ingestelde snelheid
    tc = dt.microsecond % (500000/SPEED) / (100000/SPEED)
    if tc > 2.5 and (player.movex != 0 or player.movey != 0):
        if testAngle == 0: player.image = "pacman_c0"
        elif testAngle == 90: player.image = "pacman_c90"
        elif testAngle == 180: player.image = "pacman_c180"
        elif testAngle == 270: player.image = "pacman_c270"
    else:
        if testAngle == 0: player.image = "pacman_o0"
        elif testAngle == 90: player.image = "pacman_o90"
        elif testAngle == 180: player.image = "pacman_o180"
        elif testAngle == 270: player.image = "pacman_o270"
#Test1.13    counter += 1
#Test1.13    if counter % 100 == 0:
#Test1.13        print(tc, player.image, player.angle, player.movex, player.movey)


def moveGhosts():
    """
    De functie moveGhosts handelt alle mogelijke bewegingen van de spoken af
    """
    global gosts, moveGhostsFlag, ghostsStartupCounter, GHOSTSTARTUPSTEPS, DMOVES, SPEED
    moveGhostsFlag = 0

    if ghostsStartupCounter < GHOSTSTARTUPSTEPS:

        # Om het middenvlak te verlaten voeren de spoken eerst een aantal voorgeprogrammerde stappen uit
        for ghost in ghosts:
            ghost.dir = ghost.sequence[ghostsStartupCounter]
        ghostsStartupCounter += 1
        
    else:

        # Laat de spoken bewegen nadat de initiele bewegingen zijn afgerond
        ghostCollided = False
        for ghost in ghosts:

            # We gaan alleen de bewegingen bepalen als de ghost niet aan het respawnen is
            if not ghost.respawning:

                for otherGhost in ghosts:
                    if otherGhost != ghost and ghost.colliderect(otherGhost):

                        # Als het spook botst met een ander spook, laten we het spook omkeren
                        ghost.dir = (ghost.dir+2) % 4
                        ghostCollided = True
                        
                if not ghostCollided:

                    # Als het spook niet gebotst is met een ander spook, blijven er een aantal andere mogelijkheden over:
                    dirs = getPossibleDirections(ghost)

                    # 1. We houden de spoken uit de passage naar de andere kant van het speelveld
                    if ghost.y>360 and ghost.y<380 and ghost.x<150:
                        dirs[2] = 0
                    elif ghost.y>360 and ghost.y<380 and ghost.x>450:
                        dirs[0] = 0

                    # 2. Als het spook niet verder kan en verder op 2% random momenten kiest het spook een mogelijke nieuwe richting
                    if dirs[ghost.dir] == 0 or randint(0,50) == 0:
                        direction = -1
                        while direction == -1:
                            testDirection = randint(0,3)
                            if dirs[testDirection] == 1:
                                direction = testDirection
                        ghost.dir = direction

                    # 3. We sturen het rode spook doelbewust achter de speler aan om het spel wat moeilijker te maken
                    if ghost.image == "ghost1" or ghost.image == "ghost1r":
                        followPacman(ghost, dirs)

                    # 4. We laten een tweede spook parallel met de speler bewegen, samen met #3 levert dit een handige val op voor de spoken
                    if ghost.image == "ghost2" or ghost.image == "ghost2r":
                        ambushPacman(ghost, dirs)
                        
#Test1.17 - Doortesten wat er gebeurt als een spook door de passage naar de andere kant van het speelveld gaat
#Test1.17       if ghost.y>360 and ghost.y<380 and ghost.x<150:
#                   ghost.dir = 2
#Test1.17       if ghost.y>360 and ghost.y<380 and ghost.x>450:
#                   ghost.dir = 0

    # De nieuwe richting is bepaald, die kunnen we nu doorvoeren.
    # Alleen bij ghost.dir = -1 is er geen beweging maar wordt de geest wel geteld.
    for ghost in ghosts:
        if ghost.respawning:
#Test2.14   print(moveGhostsFlag)
            animate(ghost, pos=(290,370), duration=1/SPEED, tween='linear', on_finished=flagMoveGhost)
            ghost.respawning = False
        else:
            if ghost.dir != -1:
                newX = ghost.x+DMOVES[ghost.dir][0]*20
                newY = ghost.y+DMOVES[ghost.dir][1]*20
                if newX < 0:
                    ghost.x += 600
                    newX += 600
#Test1.17       print("A", ghost.dir, newX, ghost.x)
                if newX > 600:
                    ghost.x -= 600
                    newX -= 600
#Test1.17       print("B", ghost.dir, newX, ghost.x)
                animate(ghost, pos=(newX, newY), duration=1/SPEED, tween='linear', on_finished=flagMoveGhost)
            else:
                flagMoveGhost()


def followPacman(ghost, directions):
    """
    De functie followPacman(ghost, direction) zorgt ervoor dat het meegegeven spook zo veel mogelijk richting de speler blijft bewegen.
    Door de functie wordt de variabele ghost.dir in een gewenste richting gezet.
    Input:  ghost = het spook dat we richting speler willen sturen.
            directions = de eerder bepaalde lijst van mogelijke richtingen voor het spook.
    """
    if ghost.dir == 1 or ghost.dir == 3:
        if player.x > ghost.x and directions[0] == 1: ghost.dir = 0
        if player.x < ghost.x and directions[2] == 1: ghost.dir = 2
    if ghost.dir == 0 or ghost.dir == 2 and not aboveCenter(ghost):
        if player.y > ghost.y and directions[1] == 1: ghost.dir = 1
        if player.y < ghost.y and directions[3] == 1: ghost.dir = 3


def ambushPacman(ghost, directions):
    """
    De functie ambushPacman(ghost, direction) zorgt ervoor dat het meegegeven spook zo veel mogelijk parellel met de speler blijft bewegen.
    Door de functie wordt de variabele ghost.dir in een gewenste richting gezet.
    Input:  ghost = het spook dat we parallel aan de speler willen laten bewegen.
            directions = de eerder bepaalde lijst van mogelijke richtingen voor het spook.
    """
    if player.movex > 0 and directions[0] == 1: ghost.dir = 0
    if player.movex < 0 and directions[2] == 1: ghost.dir = 2
    if player.movey > 0 and directions[1] == 1 and not aboveCenter(ghost): ghost.dir = 0
    if player.movey < 0 and directions[3] == 1: ghost.dir = 3


# Eenvoudige kleine hulpfuncties
def inputLock():
    global player
    player.inputActive = False


def inputUnlock():
    global player
    player.movex = player.movey = 0
    player.inputActive = True


def flagMoveGhost():
    global moveGhostsFlag
    moveGhostsFlag += 1


def aboveCenter(ghost):
    return ((ghost.x > 220 and ghost.x < 380) and (ghost.y > 300 and ghost.y < 320))


def drawCenterText(text):
    screen.draw.text(text, center=(300,434), owidth=0.5, ocolor=(255,255,255), color=(255,64,0), fontsize=60)
    

# Definieren en initialiseren van variablen en constanten voor het spel
WIDTH = 600
HEIGHT = 660
SPEED = 3
DMOVES = [(1,0), (0,1), (-1,0), (0,-1)]
GHOSTSTARTUPS = [[-1,-1,0,3,3,3,2,2,2], [3,3,3,2,2,2,2,1,1], [-1,3,3,3,0,0,0,0,1], [-1,-1,-1,-1,2,3,3,3,0]]
GHOSTSTARTUPSTEPS = len(GHOSTSTARTUPS[0])
gameStatus = 1

#Test1.7-1.13
#counter = 0

# Uitvoeren van het spel
init()
# pgzrun.go()
