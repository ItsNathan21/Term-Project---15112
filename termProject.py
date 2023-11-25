from cmu_graphics import *
import random
import math

class Player():
    def __init__(self, health, damage):
        self.position = [800, 400]
        self.health = health
        self.damage = damage
        self.speed = 8
        self.gravity = 10
        self.jumping = False
        self.weapons = [weapon1, weapon2]
        self.equippedWeapon = weapon1
        self.firingWeapon1 = False
        self.firingWeapon2 = False
        self.weapon2Pos = []
        self.firingMousePosition = [None, None]
    def removeHealth(self, damageInflicted):
        self.health -= damageInflicted
    def reset(self, health):
        self.health = health
        self.position = [800, 400]
        self.firingWeapon1 = False
        self.firingWeapon2 = False
        self.weapon2Pos = []
        self.firingMousePosition = [None, None]
class Boss():
    def __init__(self, health, damage):
        self.health = health
        self.damage = damage 
        self.position = [random.randint(50, 1400), random.randint(50, 1400)]
        self.attack1Ready = True
        self.attack2Ready = False
        self.attack3Ready = False
        self.attack2Positions = []
        self.attack3Positions = []
        self.attack3EnragedPositions = []
        self.projectX, self.projectY = None, None
    def takeDamage(self, amount):
        self.health -= amount
    def reset(self, health):
        self.position = [random.randint(50, 1400), random.randint(50, 1400)]
        self.health = health
        self.attack1Ready = True
        self.attack2Ready = False
        self.attack3Ready = False
        self.attack2Positions = []
        self.attack3Positions = []
        self.attack3EnragedPositions = []
        self.projectX, self.projectY = None, None

class Weapon():
    def __init__(self, damage, name):
        self.damage = damage
        self.name = name
    def __hash__(self):
        pass
    def __repr__(self):
        return f'{self.name}'

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

level2Platforms = [leftBorder, topBorder, rightBorder, bottomBorder, [500, 600, 100, 10], [1300, 400, 200, 100]]

weapon1 = Weapon(1, 'laser')
weapon2 = Weapon(100, 'bulletboy')

player = Player(100, 10)

level1 = Level(level1Platforms)
level2 = Level(level2Platforms)
level3 = Level([])

boss1 = Boss(500, 10)
boss2, boss3 = Boss(1000, 20), Boss(1000, 20)
boss4 = Boss(3000, 30)

def onAppStart(app):
    app.width, app.height = 1600, 800
    app.stepsPerSecond = 60
    app.setMaxShapeCount(10000)
    app.counter = -1
    app.homeScreen = True
    app.level1Loaded, app.level1Completed = False, True
    app.level2Loaded, app.level2Completed = False, True
    app.level3Loaded, app.level2Completed = False, True
    app.deathScreen = False
    app.victoryScreen = False

def onMousePress(app, mouseX, mouseY):
    if app.homeScreen:
        if distance(mouseX, mouseY, 200, 500) < 100:
            app.homeScreen = False
            app.level1Loaded = True
        if distance(mouseX, mouseY, 500, 500) < 100 and app.level1Completed:
            app.homeScreen = False
            app.level2Loaded = True
        if distance(mouseX, mouseY, 1100, 500) < 100:
            player.equippedWeapon = weapon1
        if distance(mouseX, mouseY, 1400, 500) < 100:
            player.equippedWeapon = weapon2
    
    if app.deathScreen and distance(mouseX, mouseY, app.width/2, app.height/2 + 150) < 100:
        resetLevelParameters(app)
        boss1.reset(500)
        boss2.reset(1000)
        boss3.reset(1000)
        player.reset(100)
        print(boss1.health)
    if app.victoryScreen and distance(mouseX, mouseY, app.width/2, app.height/2 + 150) < 100:
        level1VictoryParametersReset(app)
        boss1.reset(500)
        boss2.reset(1000)
        boss3.reset(1000)
        player.reset(100)
    if player.equippedWeapon == weapon2 and (app.level1Loaded or app.level2Loaded or app.level3Loaded):
        player.firingWeapon2 = True
        player.firingMousePosition = [mouseX, mouseY]
        player.weapon2Pos.append(player.position + player.firingMousePosition + player.position)

def onMouseDrag(app, mouseX, mouseY):
    if app.level1Loaded or app.level2Loaded and player.equippedWeapon == weapon1:
        player.firingMousePosition= [mouseX, mouseY]
        player.firingWeapon1 = True

def onMouseRelease(app, mouseX, mouseY):
    if app.level1Loaded or app.level2Loaded or app.level3Loaded:
        if player.firingWeapon1:
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
        if player.firingWeapon1 and lineOfSightCheck(app, *player.position, *player.firingMousePosition):
            if player.equippedWeapon == weapon1:
                drawLine(*player.position, *player.firingMousePosition, fill = 'green')
            if distance(*player.firingMousePosition, *boss1.position) < 100:
                boss1.takeDamage(weapon1.damage)
        if player.firingWeapon2:
            for elem in player.weapon2Pos:
                drawCircle(elem[0], elem[1], 10, fill = 'black')
                dx = (elem[2] - elem[4]) / 70
                dy = (elem[3] - elem[5]) / 70
                makeProjectileMove(app, player.weapon2Pos.index(elem), dx, dy)

    if app.level2Loaded:
        drawLevel2(app)
        level2Attack(app)
        if player.firingWeapon1 and lineOfSightCheck(app, *player.position, *player.firingMousePosition):
            if player.equippedWeapon == weapon1:
                drawLine(*player.position, *player.firingMousePosition, fill = 'green')
            if distance(*player.firingMousePosition, *boss2.position) < 100:
                boss2.takeDamage(weapon1.damage)
            if distance(*player.firingMousePosition, *boss3.position) < 100:
                boss3.takeDamage(weapon1.damage)
        if player.firingWeapon2:
            for elem in player.weapon2Pos:
                drawCircle(elem[0], elem[1], 10, fill = 'black')
                dx = (elem[2] - elem[4]) / 70
                dy = (elem[3] - elem[5]) / 70
                makeProjectileMove(app, player.weapon2Pos.index(elem), dx, dy)

    if app.deathScreen:
        drawDeathScreen(app)
    if app.victoryScreen:
        drawVictoryScreen(app)

def onKeyPress(app, key):
    pass

def onKeyRelease(app, key):
    if key == 'w':
        player.jumping = False

def onKeyHold(app, keys):
    if app.level1Loaded or app.level2Loaded or app.level3Loaded:
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
        if distance(*player.position, *boss1.position) < 100:
            player.removeHealth(1)
        if player.health <= 0:
            app.level1Loaded = False
            app.deathScreen = True
        if boss1.health <= 0:
            app.level1Loaded = False
            app.victoryScreen = True
            app.level1Completed = True
        if boss1.attack2Ready:
            if app.counter % 30 == 0:
                boss1.attack2Positions.append(boss1.position + player.position + boss1.position)
        if boss1.attack3Ready:
            if app.counter % 5 == 0:
                boss1.attack2Positions.append(boss1.position + player.position + boss1.position)
    if app.level2Loaded:
        if app.counter == -1:
            boss2.attack2Positions = [*player.position, []]
            boss3.attack2Positions = [*player.position, []]
            boss2.attack3Positions = [*player.position, []]
            boss3.attack3Positions = [*player.position, []]
        app.counter += 1
        if app.counter == 1 and boss2.attack1Ready:
            boss2.position = [random.randint(100, 500), 100]
            boss3.position = [random.randint(900, 1400), 100]
        if app.counter == 180:
            app.counter = 0
        if boss2.attack2Ready and (app.counter % 20 == 0 or distance(*boss2.position, boss2.attack2Positions[0], boss2.attack2Positions[1]) < 5):
            boss2.attack2Positions[:2] = [player.position[0] + 100, player.position[1] + 100]
            boss3.attack2Positions[:2] = [player.position[0]- 100, player.position[1]- 100]
        if boss2.attack2Ready and app.counter == 0:
            x,y = boss2.position[0],boss2.position[1]
            boss2.attack2Positions[2] += [[x+25,y,5,0],[x-25,y,-5,0],[x,y+25,0,5],[x,y-25,0,-5],[x+25,y+25,5,5],
                                         [x+25,y-25,5,-5],[x-25,y-25,-5,-5],[x-25,y+25,-5,5]]
            x1,y1 = boss3.position[0],boss3.position[1]
            boss3.attack2Positions[2] += [[x1+25,y1,5,0],[x1-25,y1,-5,0],[x1,y1+25,0,5],[x1,y1-25,0,-5],[1+25,y1+25,5,5],
                                         [x1+25,y1-25,5,-5],[x1-25,y1-25,-5,-5],[x1-25,y1+25,-5,5]]
        if boss2.attack3Ready and app.counter % 30 == 0:
            boss2.attack3Positions[:2] = [player.position[0] + 100, player.position[1] + 100]
        if boss3.attack3Ready and app.counter % 30 == 0:
            boss3.attack3Positions[:2] = [player.position[0] + 100, player.position[1] + 100]
        if boss2.attack3Ready and app.counter % 60 == 0:
            boss2.attack3EnragedPositions = [*player.position, *boss2.position]
            x1,y1 = boss2.position[0],boss2.position[1]
            boss2.attack3Positions[2] += ([[x1+25,y1],[x1-25,y1],[x1,y1+25],[x1,y1-25],[x1+25,y1+25],
                                         [x1+25,y1-25],[x1-25,y1-25],[x1-25,y1+25]])
        if boss3.attack3Ready and app.counter % 60 == 0:
            boss3.attack3EnragedPositions = [*player.position, *boss3.position]
            x1,y1 = boss3.position[0],boss3.position[1]
            boss3.attack3Positions[2] += [[x1+25,y1],[x1-25,y1],[x1,y1+25],[x1,y1-25],[x1+25,y1+25],
                                         [x1+25,y1-25],[x1-25,y1-25],[x1-25,y1+25]]
        if player.health <= 0:
            app.level2Loaded = False
            app.deathScreen = True
        if boss2.health <=0 and boss3.health <= 0:
            app.level2Loaded = False
            app.victoryScreen = True
        makeMove(app, 0, player.gravity)
    if player.jumping:
        makeMove(app, 0, -19)

def drawLevel1(app):
    drawBoss1()
    drawEnviornment1()
    drawPlayer(app)

def drawLevel2(app):
    drawBoss2()
    drawBoss3()
    drawEnviornment2()
    drawPlayer(app)

def drawEnviornment2():
    for elem in level2.platforms:
        drawRect(*elem, fill = 'blue')

def drawBoss2():
    if boss2.health > 0:
        drawRect(30, 30, 1004, 10, fill = None, borderWidth = 2, border = 'black')
        drawRect(32, 32, boss2.health, 6, fill = 'red')
        drawCircle(*boss2.position, 50, fill = 'blue')

def drawBoss3():
    if boss3.health > 0:
        drawRect(30, 60, 1004, 10, fill = None, borderWidth = 2, border = 'black')
        drawRect(32, 62, boss3.health, 6, fill = 'red')
        drawCircle(*boss3.position, 50, fill = 'red')

def level2Attack(app):
    if boss2.health > 500 and boss3.health > 500:
        level2Attack1()
        boss1.attack1Ready = True
        if (boss2.position[0] < player.position[0] < boss3.position[0] and
            boss2.position[1] - 10 < player.position[1] < boss2.position[1] + 10):
            player.removeHealth(boss2.damage//10)
        if (distance(*player.position, *boss2.position) < 50 or 
            distance(*player.position, *boss3.position) < 50):
            player.removeHealth(boss2.damage//10)

    elif (boss2.health <= 500 or boss3.health <= 500) and (boss2.health > 0) and (boss3.health > 0):
        boss2.attack1Ready = False
        boss2.attack2Ready = True
        level2Attack2(app)
        if (distance(*player.position, *boss2.position) < 50 or 
            distance(*player.position, *boss3.position) < 50):
            player.removeHealth(boss2.damage//10)
    elif boss2.health <= 0 and boss3.health > 0:
        boss2.attack2Ready = False
        boss3.attack3Ready = True
        if (distance(*player.position, *boss3.position) < 50):
            player.removeHealth(boss3.damage)
        boss3Attack3(app)
    elif boss2.health >0 and boss3.health <=0:
        boss2.attack2Ready = False
        boss2.attack3Ready = True
        if (distance(*player.position, *boss2.position) < 50):
            player.removeHealth(boss2.damage)
        boss2Attack3(app)


def boss2Attack3(app):
    angle = angleTo(boss2.position[0], boss2.position[1], boss2.attack3Positions[0], boss2.attack3Positions[1])
    dy, dx = 5 * math.cos(angle), -5 * math.sin(angle)
    boss23Attack2Move(dx, dy, 0, 0)
    for elem in boss2.attack3Positions[2]:
        drawCircle(elem[0], elem[1], 10, fill = 'gray')
        dx2, dy2 = (boss2.attack3EnragedPositions[0] - boss2.attack3EnragedPositions[2]) / 20, (boss2.attack3EnragedPositions[1] - boss2.attack3EnragedPositions[3]) / 20
        boss2Attack3Move(boss2.attack3Positions[2].index(elem), dx2, dy2)

def boss3Attack3(app):
    angle = angleTo(boss3.position[0], boss3.position[1], boss3.attack3Positions[0], boss3.attack3Positions[1])
    dy, dx = 5 *math.cos(angle), -5 * math.sin(angle)
    boss23Attack2Move(0, 0, dx, dy)
    for elem in boss3.attack3Positions[2]:
        drawCircle(elem[0], elem[1], 10, fill = 'gray')
        dx2, dy2 = (boss3.attack3EnragedPositions[0] - boss3.attack3EnragedPositions[2]) / 20, (boss3.attack3EnragedPositions[1] - boss3.attack3EnragedPositions[3]) / 20
        boss3Attack3Move(boss3.attack3Positions[2].index(elem), dx2, dy2)

def boss2Attack3Move(index, dx, dy):
    boss2.attack3Positions[2][index][0] += dx
    boss2.attack3Positions[2][index][1] += dy
    for platform in level2.platforms:
        if rectanglesOverlap(*platform, boss2.attack3Positions[2][index][0], boss2.attack3Positions[2][index][1], 10, 10):
            boss2.attack3Positions[2].pop(index)
            return
    if distance(boss2.attack3Positions[2][index][0], boss2.attack3Positions[2][index][1], *player.position) < 50:
        player.removeHealth(boss2.damage)
        boss2.attack3Positions[2].pop(index)

def boss3Attack3Move(index, dx, dy):
    boss3.attack3Positions[2][index][0] += dx
    boss3.attack3Positions[2][index][1] += dy
    for platform in level2.platforms:
        if rectanglesOverlap(*platform, boss3.attack3Positions[2][index][0], boss3.attack3Positions[2][index][1], 10, 10):
            boss3.attack3Positions[2].pop(index)
            return
    if distance(boss3.attack3Positions[2][index][0], boss3.attack3Positions[2][index][1], *player.position) < 50:
        player.removeHealth(boss3.damage)
        boss3.attack3Positions[2].pop(index)

def level2Attack1():
    drawLine(*boss2.position, *boss3.position)
    dy = 3
    boss23Attack1Move(0, dy)

def boss23Attack1Move(dx, dy):
    boss2.position = [boss2.position[0] + dx, boss2.position[1] + dy]
    boss3.position = [boss3.position[0] + dx, boss3.position[1] + dy]


def level2Attack2(app):
    angle2 = angleTo(boss2.position[0], boss2.position[1], boss2.attack2Positions[0], boss2.attack2Positions[1])
    angle3 = angleTo(boss3.position[0], boss3.position[1], boss3.attack2Positions[0], boss3.attack2Positions[1])
    dy2, dx2 = 2 * math.cos(angle2), -2 * math.sin(angle2)
    dy3, dx3 = 2 * math.cos(angle3), -2 * math.sin(angle3)
    boss23Attack2Move(dx2, dy2, dx3, dy3)
    if len(boss2.attack2Positions) == 3:
        for elem in boss2.attack2Positions[2]:
            drawCircle(elem[0], elem[1], 10, fill = 'gray')
            dx, dy = elem[2], elem[3]
            boss2Attack2Move(app, boss2.attack2Positions[2].index(elem), dx, dy)
    if len(boss3.attack2Positions) == 3:
        for elem in boss3.attack2Positions[2]:
            drawCircle(elem[0], elem[1], 10, fill = 'gray')
            dx, dy = elem[2], elem[3]
            boss3Attack2Move(app, boss3.attack2Positions[2].index(elem), dx, dy)
    

def boss2Attack2Move(app, index, dx, dy):
    boss2.attack2Positions[2][index][0] += dx
    boss2.attack2Positions[2][index][1] += dy
    for platform in level2.platforms:
        if rectanglesOverlap(*platform, boss2.attack2Positions[2][index][0], boss2.attack2Positions[2][index][1], 10, 10):
            boss2.attack2Positions[2].pop(index)
            return
    if distance(boss2.attack2Positions[2][index][0], boss2.attack2Positions[2][index][1], *player.position) < 50:
        player.removeHealth(boss2.damage)
        boss2.attack2Positions[2].pop(index)

def boss3Attack2Move(app, index, dx, dy):
    boss3.attack2Positions[2][index][0] += dx
    boss3.attack2Positions[2][index][1] += dy
    for platform in level2.platforms:
        if rectanglesOverlap(*platform, boss3.attack2Positions[2][index][0], boss3.attack2Positions[2][index][1], 10, 10):
            boss3.attack2Positions[2].pop(index)
            return
    if distance(boss3.attack2Positions[2][index][0], boss3.attack2Positions[2][index][1], *player.position) < 50:
        player.removeHealth(boss2.damage)
        boss3.attack2Positions[2].pop(index)

def boss23Attack2Move(dx2, dy2, dx3, dy3):
    boss2.position = [boss2.position[0] + dx2, boss2.position[1] + dy2]
    boss3.position = [boss3.position[0] + dx3, boss3.position[1] + dy3]


def drawEnviornment2():
    for elem in level2.platforms:
        drawRect(*elem, fill = 'blue')

def drawPlayer(app):
    drawRect(*player.position, 50, 70, fill = 'hotpink', align = 'center')
    drawCircle(*player.position, 25, fill = None, border = 'black')
    drawRect(1400, 740, 104, 10, fill = None, borderWidth = 2, border = 'black')
    drawLabel('Player Health', 1452, 730, align='center')
    if player.health > 0:
        drawRect(1402, 742, player.health, 8, fill = 'green')

def drawEnviornment1():
    for elem in level1.platforms:
        drawRect(*elem, fill = 'blue')

def drawBoss1():
    if boss1.health > 0:
        drawRect(30, 30, 504, 10, fill = None, borderWidth = 2, border = 'black')
        drawRect(32, 32, boss1.health, 6, fill = 'red')
    if boss1.attack1Ready:
        drawCircle(*boss1.position, 100, fill = 'red')
        drawLabel('Attacking AHHHH', *boss1.position)
    elif not boss1.attack1Ready and boss1.health > 300:
        drawCircle(*boss1.position, 100, fill = 'green')
        drawLabel('Not Attacking', *boss1.position)
    if boss1.attack2Ready:
        drawCircle(*boss1.position, 100, fill = 'red')
        drawLabel('projectile attacks now', *boss1.position)
    if boss1.attack3Ready:
        drawCircle(*boss1.position, 100, fill = 'red')
        drawLabel('ENRAGED MODE', *boss1.position)

def bossMove(app, newX, newY):
    dx = newX - boss1.position[0]
    dy = newY - boss1.position[1]
    boss1.position = [dx + boss1.position[0], dy + boss1.position[1]]
    drawBoss1()

def projectBossNextSpot(app, newX, newY):
    drawCircle(newX, newY, 100, fill = None, border = 'black', borderWidth = 2)
    drawLabel('boss is about to move here', newX, newY)

def bossAttack(app):
    if boss1.health > 300:
        boss1Attack1(app)
    elif boss1.health > 100:
        boss1.attack2Ready = True
        boss1Attack2(app)
    else:
        boss1.attack3Ready = True
        boss1Attack3(app)

def lineOfSightCheck(app, object1X, object1Y, object2X, object2Y):
    dx = (object2X - object1X) // 25
    dy = (object2Y - object1Y) // 25
    rect1 = [object1X + dx, object1Y + dy, 10, 10]
    for i in range(25): #the amount of times before it will hit the player (same number as the // for dx and dy)
        drawRect(*rect1, fill = None)
        if app.level1Loaded:
            for platform in level1.platforms[4:]:
                if rectanglesOverlap(*platform, *rect1):
                    return False
            rect1 = [rect1[0] + dx, rect1[1] + dy, 10, 10]
        elif app.level2Loaded:
            for platform in level2.platforms[4:]:
                if rectanglesOverlap(*platform, *rect1):
                    return False
            rect1 = [rect1[0] + dx, rect1[1] + dy, 10, 10]
        elif app.level3Loaded:
            for platform in level3.platforms[4:]:
                if rectanglesOverlap(*platform, *rect1):
                    return False
            rect1 = [rect1[0] + dx, rect1[1] + dy, 10, 10]
    return True

def boss1Attack1(app):
    los = lineOfSightCheck(app, *boss1.position, *player.position)
    if boss1.attack1Ready and los:
        drawLine(*boss1.position, *player.position, lineWidth = 5)
        player.removeHealth(0.025)    

def boss1Attack2(app):
    for elem in boss1.attack2Positions:
        drawCircle(elem[0], elem[1], 10, fill = 'skyblue')
        dx = (elem[2] - elem[4]) / 30
        dy = (elem[3] - elem[5]) / 30
        makeBossProjectileMove(app, boss1.attack2Positions.index(elem), dx, dy)

def boss1Attack3(app):
    boss1Attack2(app)

def makeBossProjectileMove(app, index, dx, dy):
    boss1.attack2Positions[index][0] = boss1.attack2Positions[index][0] + dx
    boss1.attack2Positions[index][1] = boss1.attack2Positions[index][1] + dy
    if (0 > boss1.attack2Positions[index][0]-20 or boss1.attack2Positions[index][0]+20 > app.width or 
            0 > boss1.attack2Positions[index][1] 
            or boss1.attack2Positions[index][1]+20> app.height):
        boss1.attack2Positions.pop(index)
        return 
    if app.level1Loaded:
        for platform in level1.platforms:
            if rectanglesOverlap(*platform, boss1.attack2Positions[index][0], boss1.attack2Positions[index][1], 20, 20):
                boss1.attack2Positions.pop(index)
                return
    if distance(boss1.attack2Positions[index][0], boss1.attack2Positions[index][1], *player.position) < 60:
        player.removeHealth(10)
        boss1.attack2Positions.pop(index)

def makeProjectileMove(app, index, dx, dy):
    if len(player.weapon2Pos) > 7:
        player.weapon2Pos.pop(-1)
        return
    player.weapon2Pos[index][0] = player.weapon2Pos[index][0] + dx
    player.weapon2Pos[index][1] = player.weapon2Pos[index][1] + dy
    if (0 > player.weapon2Pos[index][0]-10 or player.weapon2Pos[index][0]+10 > app.width or 0 > player.weapon2Pos[index][1] 
            or player.weapon2Pos[index][1]+10> app.height):
        player.weapon2Pos.pop(index)
        return 
    if app.level1Loaded:
        for platform in level1.platforms:
            if rectanglesOverlap(*platform, player.weapon2Pos[index][0], player.weapon2Pos[index][1], 10, 10):
                player.weapon2Pos.pop(index)
                return
        if distance(player.weapon2Pos[index][0], player.weapon2Pos[index][1], *boss1.position) < 100:
            boss1.takeDamage(weapon2.damage)
            player.weapon2Pos.pop(index)
    if app.level2Loaded:
        for platform in level2.platforms:
            if rectanglesOverlap(*platform, player.weapon2Pos[index][0], player.weapon2Pos[index][1], 10, 10):
                player.weapon2Pos.pop(index)
                return
        if distance(player.weapon2Pos[index][0], player.weapon2Pos[index][1], *boss2.position) < 50:
            boss2.takeDamage(weapon2.damage)
            player.weapon2Pos.pop(index)
            return 
        if distance(player.weapon2Pos[index][0], player.weapon2Pos[index][1], *boss3.position) < 50:
            boss3.takeDamage(weapon2.damage)
            player.weapon2Pos.pop(index)
 

def makeMove(app, dx, dy):
    player.position = [player.position[0] + dx, player.position[1] + dy]
    if 0 > player.position[0]-25 or player.position[0]+25 > app.width or 0 > player.position[1] or player.position[1]+35> app.height:
        player.position = [player.position[0] - dx, player.position[1] - dy]
    if app.level1Loaded:
        for platform in level1.platforms:
            if rectanglesOverlap(*platform, player.position[0]-25, player.position[1], 45, 30):
                player.position = [player.position[0] - dx, player.position[1] - dy]
    elif app.level2Loaded:
        for platform in level2.platforms:
                if rectanglesOverlap(*platform, player.position[0]-25, player.position[1], 45, 30):
                    player.position = [player.position[0] - dx, player.position[1] - dy]

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
    drawLabel('level1', 200, 500, align='center')
    drawRect(400, 400, 200, 200, fill = None, borderWidth = 4, border = 'black')
    drawLabel('level2', 500, 500, align='center')
    drawRect(700, 400, 200, 200, fill = None, borderWidth = 4, border = 'black')
    drawLabel('level3', 800, 500, align='center')
    drawRect(1000, 400, 200, 200, fill = None, borderWidth = 4, border = 'black')
    drawLabel('weapon1', 1100, 500, align='center')
    drawRect(1300, 400, 200, 200, fill = None, borderWidth = 4, border = 'black')
    drawLabel('weapon2', 1400, 500, align='center')
   
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
    app.counter = -1
    app.jumping = False
    app.victoryScreen = False

def resetLevelParameters(app):
    app.level1Loaded = False
    app.deathScreen = False
    app.homeScreen = True
    app.jumping = False
    app.counter = -1


def main():
    runApp()
main()