from cmu_graphics import *
import random

class Player():
    def __init__(self, health, damage):
        self.health = health
        self.damage = damage
        self.speed = 8
        self.gravity = 10
        self.jumping = False
        self.weapons = [weapon1]
        self.equippedWeapon = weapon1
        self.firingWeapon1 = False
        self.firingMousePosition = [None, None]
    def removeHealth(self, damageInflicted):
        if self.health > damageInflicted:
            self.health -= damageInflicted

class Boss():
    def __init__(self, health, damage):
        self.health = health
        self.damage = damage 
        self.position = [200, 200]
        self.projectiles = []
        self.attack1Ready = True
        self.lineOfSightToPlayer = False
        self.projectX, self.projectY = None, None

class Weapon():
    def __init__(self, damage):
        self.damage = damage
    def __hash__(self):
        pass

class Armor():
    def __init__(self, shields):
        self.shield = shields
    def __hash__(self):
        pass

class Level():
    def __init__(self, platforms):
        self.border = None
        self.background = None
        self.platforms = platforms

leftBorder = [0, 0, 20, 800]
topBorder = [0, 0, 1600, 20]
rightBorder = [1580, 0, 20, 800]
bottomBorder = [0, 780, 1600, 20]

level1Platforms = [leftBorder, topBorder, rightBorder, bottomBorder, [1400, 600, 100, 15], 
                   [1500, 500, 15, 115], 
                   [300, 300, 100, 15], 
                   [500,600, 10, 100],
                   [455, 650, 100, 10]]


weapon1 = Weapon(1)

player = Player(100, 10)
level1 = Level(level1Platforms)
level2 = Level([])
level3 = Level([])
boss1 = Boss(500, 10)
boss2 = Boss(1000, 20)
boss3 = Boss(3000, 30)

def onAppStart(app):
    app.width, app.height = 1600, 800
    app.stepsPerSecond = 60
    app.setMaxShapeCount(10000)
    app.counter = 0
    app.homeScreen = True
    app.level1Loaded, app.level1Completed = False, False
    app.level2Loaded, app.level2Completed = False, False
    app.level3Loaded, app.level2Completed = False, False
    app.deathScreen = False
    app.victoryScreen = False
    app.position = [app.width/2, app.height/2]

def onMousePress(app, mouseX, mouseY):
    if app.homeScreen and distance(mouseX, mouseY, 200, 500) < 100:
        app.homeScreen = False
        app.level1Loaded = True
    if app.deathScreen and distance(mouseX, mouseY, app.width/2, app.height/2 + 150) < 100:
        resetLevelParameters(app)
    if app.victoryScreen and distance(mouseX, mouseY, app.width/2, app.height/2 + 150) < 100:
        level1VictoryParametersReset(app)
        
def onMouseDrag(app, mouseX, mouseY):
    if app.level1Loaded:
        player.firingMousePosition = [mouseX, mouseY]
        player.firingWeapon1 = True

def onMouseRelease(app, mouseX, mouseY):
    if app.level1Loaded and player.firingWeapon1:
        player.firingWeapon1 = False

def redrawAll(app):
    if app.homeScreen:
        drawHomeScreen(app)
    if app.level1Loaded:
        drawLevel1(app)
        bossAttack(app)
        if app.counter == 300:
            bossMove(app, boss1.projectX, boss1.projectY)
        elif 100 < app.counter < 300:
            projectBossNextSpot(app, boss1.projectX, boss1.projectY)
        if player.firingWeapon1 and lineOfSightCheck(app, *app.position, *player.firingMousePosition):
            if player.equippedWeapon == weapon1:
                drawLine(*app.position, *player.firingMousePosition, fill = 'green')
            if distance(*player.firingMousePosition, *boss1.position) < 100:
                boss1.health -= weapon1.damage
    if app.deathScreen:
        drawDeathScreen(app)
    if app.victoryScreen:
        drawVictoryScreen(app)

def onKeyPress(app, key):
    pass

def onKeyRelease(app, key):
    if app.level1Loaded or app.level2Loaded or app.level3Loaded and key == 'w':
        player.jumping = False

def onKeyHold(app, keys):
    if 'd' in keys and 'a' not in keys:
        makeMove(app, player.speed, 0)
    if 'a' in keys and 'd' not in keys:
        makeMove(app, -player.speed, 0)
    if 'w' in keys:
        player.jumping = True

def onStep(app):
    if app.level1Loaded:
        if app.counter == 1:
            boss1.projectX = random.randint(70, app.width - 70)
            boss1.projectY = random.randint(70 , app.height - 70)
        app.counter += 1
        makeMove(app, 0, player.gravity)
        if app.counter > 600:
            boss1.attack1Ready = not boss1.attack1Ready
            app.counter = 0
        if distance(*app.position, *boss1.position) < 100:
            player.health -= 1
        if player.health <= 0:
            app.level1Loaded = False
            app.deathScreen = True
        if boss1.health <= 0:
            app.level1Loaded = False
            app.victoryScreen = True
    if player.jumping:
        makeMove(app, 0, -19)

def drawLevel1(app):
    drawBoss()
    drawEnviornment1(app)
    drawPlayer(app)

def drawPlayer(app):
    drawRect(*app.position, 50, 70, fill = 'hotpink', align = 'center')
    drawCircle(*app.position, 25, fill = None, border = 'black')
    drawRect(1400, 740, 104, 10, fill = None, borderWidth = 2, border = 'black')
    drawLabel('Player Health', 1452, 730, align='center')
    if player.health > 0:
        drawRect(1402, 742, player.health, 8, fill = 'green')


def drawEnviornment1(app):
    for elem in level1.platforms:
        drawRect(*elem, fill = 'blue')

def drawBoss():
    if boss1.health > 0:
        drawRect(30, 30, 504, 10, fill = None, borderWidth = 2, border = 'black')
        drawRect(32, 32, boss1.health, 6, fill = 'red')
    if boss1.attack1Ready:
        drawCircle(*boss1.position, 100, fill = 'red')
        drawLabel('Attacking AHHGHH', *boss1.position)
    else:
        drawCircle(*boss1.position, 100, fill = 'green')
        drawLabel('Not Attacking', *boss1.position)

def bossMove(app, newX, newY):
    dx = newX - boss1.position[0]
    dy = newY - boss1.position[1]
    boss1.position = [dx + boss1.position[0], dy + boss1.position[1]]
    drawBoss()


def projectBossNextSpot(app, newX, newY):
    drawCircle(newX, newY, 100, fill = None, border = 'black', borderWidth = 2)
    drawLabel('boss is about to move here', newX, newY)

def bossAttack(app):
    if boss1.health > 300:
        boss1Attack1(app)
    else:
        boss1Attack2(app)
    
def boss1Attack1(app):
    los = lineOfSightCheck(app, *boss1.position, *app.position)
    if boss1.attack1Ready and los:
        drawLine(*boss1.position, *app.position, lineWidth = 5)
        player.health -= 0.025    


def lineOfSightCheck(app, object1X, object1Y, object2X, object2Y):
    dx = (object2X - object1X) // 25
    dy = (object2Y - object1Y) // 25
    rect1 = [object1X + dx, object1Y + dy, 10, 10]
    right = object2X > rect1[0]
    for i in range(25): #the amount of times before it will hit the player (same number as the // for dx and dy)
        drawRect(*rect1, fill = None)
        for platform in level1.platforms[4:]:
             if rectanglesOverlap(*platform, *rect1):
                return False
        rect1 = [rect1[0] + dx, rect1[1] + dy, 10, 10]
    return True

def boss1Attack2(app):
    pass

def moveRight(app):
    app.position[0] += player.speed

def moveLeft(app):
    app.position[0] -= player.speed    

def makeMove(app, dx, dy):
    app.position = [app.position[0] + dx, app.position[1] + dy]
    if 0 > app.position[0]-25 or app.position[0]+25 > app.width or 0 > app.position[1] or app.position[1]+35> app.height:
        app.position = [app.position[0] - dx, app.position[1] - dy]
    if app.level1Loaded:
        for platform in level1.platforms:
            if rectanglesOverlap(*platform, app.position[0]-25, app.position[1], 45, 30):
                app.position = [app.position[0] - dx, app.position[1] - dy]

def rectanglesOverlap(left1, top1, width1, height1,
                      left2, top2, width2, height2):
    bottom1 = top1 + height1
    bottom2 = top2 + height2
    right1 = left1 + width1
    right2 = left2 + width2
    return (bottom1 >= top2 and bottom2 >= top1 and right1 >= left2 and right2 >= left1 )

def drawHomeScreen(app):
    drawLabel('Welcome to Boss Fight 112', app.width/2, 100, align = 'center', size = 20)
    drawRect(100, 400, 200, 200, fill = None, borderWidth = 4, border = 'black')
    # Do all other home screen stuff\

def drawDeathScreen(app):
    drawLabel('You died bruh', app.width/2, app.height/2, align = 'center', size = 25)
    drawLabel('lol lmao', app.width/2, app.height/2 + 50, align = 'center', size = 25)
    drawRect(app.width/2, app.height/2 + 150, 100, 100, align  = 'center', fill = None, border = 'black')

def drawVictoryScreen(app):
    drawLabel('You won bruh', app.width/2, app.height/2, align = 'center', size = 25)
    drawLabel('lol lmao good work', app.width/2, app.height/2 + 50, align = 'center', size = 25)
    drawRect(app.width/2, app.height/2 + 150, 100, 100, align  = 'center', fill = None, border = 'black')

def level1VictoryParametersReset(app):
    app.level1Loaded = False
    app.homeScreen = True
    app.position = [app.width/2, app.height/2]
    boss1.position = [200, 200]
    boss1.health = 500
    player.health = 100
    app.counter = 0
    app.victoryScreen = False

def resetLevelParameters(app):
    app.level1Loaded = False
    app.deathScreen = False
    app.homeScreen = True
    app.position = [app.width/2, app.height/2]
    boss1.position = [200, 200]
    boss1.health = 500
    player.health = 100
    app.counter = 0

def main():
    runApp()
main()