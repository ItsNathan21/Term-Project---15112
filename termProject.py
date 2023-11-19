from cmu_graphics import *
import random

class Player():
    def __init__(self, health, damage):
        self.health = health
        self.damage = damage
        self.speed = 8
        self.gravity = 24
        self.jumping = False
    def removeHealth(self, damageInflicted):
        if self.health > damageInflicted:
            self.health -= damageInflicted

class Boss():
    def __init__(self, health, damage):
        self.health = health
        self.damage = damage 
        self.position = [100, 100]
        self.projectiles = []
        self.attack1Ready = True
        self.lineOfSightToPlayer = False

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

level1Platforms = [leftBorder, topBorder, rightBorder, bottomBorder, [600, 600, 300, 100], [300, 100, 300, 100]]

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
    app.level1Loaded = False
    app.level2Loaded = False
    app.level3Loaded = False
    app.position = [app.width/2, app.height/2]

def onMousePress(app, mouseX, mouseY):
    if app.homeScreen and distance(mouseX, mouseY, 200, 500) < 100:
        app.homeScreen = False
        app.level1Loaded = True

def redrawAll(app):
    if app.homeScreen:
        drawHomeScreen(app)
    if app.level1Loaded:
        drawLevel1(app)
        bossAttack(app)
        if app.counter == 300:
            bossMove(app, random.randint(0, app.width), random.randint(0, app.height))

def onKeyPress(app, key):
    pass

def onKeyRelease(app, key):
    if key == 'w':
        player.jumping = False

def onKeyHold(app, keys):
    if 'd' in keys and 'a' not in keys:
        makeMove(app, player.speed, 0)
    if 'a' in keys and 'd' not in keys:
        makeMove(app, -player.speed, 0)
    if 'w' in keys:
        player.jumping = True

def onStep(app):
    app.counter += 1
    if app.level1Loaded:
        makeMove(app, 0, 10)
        if app.counter > 600:
            boss1.attack1Ready = not boss1.attack1Ready
            app.counter = 0
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
    drawRect(1402, 742, player.health, 8, fill = 'green')
    drawLabel('Player Health', 1452, 730, align='center')

def drawEnviornment1(app):
    for elem in level1.platforms:
        drawRect(*elem, fill = 'blue')

def drawBoss():
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


def bossAttack(app):
    if boss1.health > 300:
        boss1Attack1(app)
    else:
        boss1Attack2(app)
    
def boss1Attack1(app):
    los = lineOfSightCheck(app)
    if boss1.attack1Ready and los:
        drawLine(*boss1.position, *app.position, lineWidth = 5)
        player.health -= 0.025
        print(player.health)
    
def lineOfSightCheck(app):
    dx = (app.position[0] - boss1.position[0]) // 10
    dy = (app.position[1] - boss1.position[1]) // 10
    rect1 = [boss1.position[0] + dx, boss1.position[1] + dy, 10, 10]
    right = app.position[0] > rect1[0]
    for i in range(10): #the amount of times before it will hit the player (same number as the // for dx and dy)
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
    # Do all other home screen stuff 

def main():
    runApp()
main()