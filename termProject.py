from cmu_graphics import *
import random
import math


####### INITIALIZING VALUES AND BORDERS
#######
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

def onAppStart(app):
    app.width, app.height = 1600, 800
    app.stepsPerSecond = 60
    app.setMaxShapeCount(10000)
    app.counter = -1
    app.homeScreen = True
    app.weaponSelectionScreen = False
    app.customLevelEditor = False
    app.customLevel = False
    app.level1Loaded, app.level1Completed = False, True
    app.level2Loaded, app.level2Completed = False, True
    app.level3Loaded, app.level2Completed = False, True
    app.deathScreen = False
    app.victoryScreen = False

####### DEFINING CLASSES 
#######
class Player():
    def __init__(self, health, damage):
        self.position = [800, 400]
        self.health = health
        self.damage = damage
        self.speed = 8
        self.gravity = 10
        self.jumping = False
        self.weapons = [weapon1, weapon2, weapon3, weapon4]
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
    def move(self, app, dx, dy):
        testPosition = [player.position[0] + dx, player.position[1] + dy]
        for platform in currentlyLoadedLevel(app)[0]:
            if rectanglesOverlap(*platform, testPosition[0] -25, testPosition[1] - 35, 50, 70):
                    return
        self.position = testPosition

class Boss():
    def __init__(self, health, damage, hitboxRadius):
        self.health = health
        self.originalHealth = health
        self.damage = damage 
        self.active = False
        self.radius = hitboxRadius
        self.position = [random.randint(50, 1400), random.randint(50, 600)]
        self.attack1Ready = True
        self.attack2Ready = False
        self.attack3Ready = False
        self.attack2Positions = []
        self.attack3Positions = [800, 400, []]
        self.attack3EnragedPositions = []
        self.projectX, self.projectY = None, None
    def __repr__(self):
        return f'{self.damage}'
    def takeDamage(self, amount):
        self.health -= amount
    def reset(self, health):
        self.health = health 
        self.position = [random.randint(50, 1400), random.randint(50, 600)]
        self.attack1Ready = True
        self.attack2Ready = False
        self.attack3Ready = False
        self.attack2Positions = []
        self.attack3Positions = [800, 400, []]
        self.attack3EnragedPositions = []
        self.projectX, self.projectY = None, None
    def teleport(self, x, y):
        self.position = [x, y]
    def touching(self):
        return distance(*player.position, *self.position) < 50
    def octagonalPositions(self, x, y):
        return [[x+25,y,5,0],[x-25,y,-5,0],[x,y+25,0,5],[x,y-25,0,-5],[x+25,y+25,5,5],
                [x+25,y-25,5,-5],[x-25,y-25,-5,-5],[x-25,y+25,-5,5]]
    def shotgunPositions(self, x, y):
        return [[x+25,y],[x-25,y],[x,y+25],[x,y-25],[x+25,y+25],
                [x+25,y-25],[x-25,y-25],[x-25,y+25]]
    def bossMove(self, dx, dy):
        self.position = [self.position[0] + dx, self.position[1] + dy]
    def attack3(self):
        dx, dy = ((self.attack3Positions[0] - self.position[0])/70, 
                (self.attack3Positions[1] - self.position[1])/70)
        if dx!=0:
            dx, dy = angleMaker(3, dx, dy)
            self.bossMove(dx, dy)
        if self.attack3EnragedPositions:
            dx2, dy2 = ((player.position[0] - self.position[0])/70,
                        (player.position[1] - self.position[1])/70)
            if dx2 != 0:
                dx2, dy2 = angleMaker(7, dx2, dy2)       
            for elem in self.attack3Positions[2]:
                drawCircle(elem[0], elem[1], 10, fill = 'gray')
                index = self.attack3Positions[2].index(elem)
                elem[0] += dx2
                elem[1] += dy2
                for platform in level2.platforms:
                    if rectanglesOverlap(*platform, elem[0], elem[1], 10, 10):
                        self.attack3Positions[2].pop(index)
                        return
                if distance(elem[0], elem[1], *player.position) < 50:
                    player.removeHealth(self.damage)
                    self.attack3Positions[2].pop(index)
    def shootProjectile(self, index, dx, dy):
        self.attack2Positions[index][0] += dx
        self.attack2Positions[index][1] += dy
        for platform in level2.platforms:
            if rectanglesOverlap(*platform, self.attack2Positions[index][0], 
                                 self.attack2Positions[index][1], 10, 10):
                self.attack2Positions.pop(index)
                return
        if distance(self.attack2Positions[index][0], 
                    self.attack2Positions[index][1], *player.position) < 50:
            player.removeHealth(self.damage)
            self.attack2Positions.pop(index)
    def shootProjectilesOutwards(self, index, dx, dy):
        self.attack2Positions[2][index][0] += dx
        self.attack2Positions[2][index][1] += dy
        for platform in level2.platforms:
            if rectanglesOverlap(*platform, 
                self.attack2Positions[2][index][0], self.attack2Positions[2][index][1], 10, 10):
                self.attack2Positions[2].pop(index)
                return
        if distance(self.attack2Positions[2][index][0], 
                self.attack2Positions[2][index][1], *player.position) < 50:
            player.removeHealth(self.damage)
            self.attack2Positions[2].pop(index)

class Weapon():
    def __init__(self, damage, name):
        self.damage = damage
        self.name = name
        self.firing = False
        self.mousePosition = []
        self.projectilePositions = []
    def __hash__(self):
        pass
    def __repr__(self):
        return f'{self.name}'
    def projectileMove(self, app, index, dx, dy):
        self.projectilePositions[index][0] += dx
        self.projectilePositions[index][1] += dy
        for platform in currentlyLoadedLevel(app)[0]:
            if rectanglesOverlap(*platform, self.projectilePositions[index][0], 
                            self.projectilePositions[index][1], 10, 10):
                self.projectilePositions.pop(index)
                return 
        for boss in currentlyLoadedLevel(app)[1:]:
            if distance(self.projectilePositions[index][0], 
                        self.projectilePositions[index][1], *boss.position) < boss.radius:
                self.projectilePositions.pop(index)
                boss.takeDamage(self.damage)
                return
    def reset(self):
        self.firing = False
        self.mousePosition = []
        self.projectilePositions = []

class Armor():
    def __init__(self, shields):
        self.shield = shields
    def __hash__(self):
        pass

class Level():
    def __init__(self, platforms):
        self.platforms = platforms
        self.makingPlatform = False
        self.platformOutlinePosition = []
        self.bosses = []
    def addPlatform(self, platform):
        self.platforms.append(platform)

weapon1 = Weapon(1, 'laser')
weapon2 = Weapon(100, 'bulletboy')
weapon3 = Weapon(5, 'Razoablade Typhoon')
weapon4 = Weapon(50, 'blood rain')

player = Player(100, 10)

level1 = Level(level1Platforms)
level2 = Level(level2Platforms)
level3 = Level([])
customLevel = Level([leftBorder, topBorder, rightBorder, bottomBorder])


boss1 = Boss(500, 10, 100)
boss2, boss3 = Boss(1000, 20, 50), Boss(1000, 20, 50)
boss4 = Boss(3000, 30, 300)

bosses = [boss1, boss2, boss3, boss4]
weapons = [weapon1, weapon2, weapon3, weapon4]

####### ALL MISCLELLANEOUS FUNCTIONS
#######
def currentlyLoadedLevel(app):
    if app.level1Loaded:
        return [level1.platforms, boss1]
    elif app.level2Loaded:
        return [level2.platforms, boss2, boss3]
    elif app.level3Loaded:
        return [level3.platforms, boss4]
    return [customLevel.platforms, *customLevel.bosses]
def anyLevelLoaded(app):
    return app.level1Loaded or app.level2Loaded or app.level3Loaded or app.customLevel

def angleMaker(scalar, dx, dy):
    f = 1 if dx > 0 else -1
    a = math.atan(dy/dx)
    dx, dy = f * scalar * math.cos(a), f * scalar * math.sin(a)
    return dx, dy

def rectanglesOverlap(left1, top1, width1, height1,
                      left2, top2, width2, height2):
    bottom1 = top1 + height1
    bottom2 = top2 + height2
    right1 = left1 + width1
    right2 = left2 + width2
    return (bottom1 >= top2 and bottom2 >= top1 and right1 >= left2 and right2 >= left1 )

def lineOfSightCheck(app, object1X, object1Y, object2X, object2Y):
    dx = (object2X - object1X) / 25
    dy = (object2Y - object1Y) / 25
    rect1 = [object1X + dx, object1Y + dy, 10, 10]
    for i in range(25):
        drawRect(*rect1, fill = None)
        for platform in currentlyLoadedLevel(app)[0]:
            if rectanglesOverlap(*platform, *rect1):
                    return False
        rect1 = [rect1[0] + dx, rect1[1] + dy, 10, 10]
    return True

def weaponShootingMechanics(app, bossList):
    if weapon1.firing and lineOfSightCheck(app, *player.position, *weapon1.mousePosition):
        drawLine(*player.position, *weapon1.mousePosition, fill = 'green')
        for elem in bossList:
            if distance(*weapon1.mousePosition, *elem.position) < 100:
                elem.takeDamage(weapon1.damage)
    if weapon2.firing:
        for elem in weapon2.projectilePositions:
            drawCircle(elem[0], elem[1], 10, fill = 'black')
            dx, dy = elem[2], elem[3]
            weapon2.projectileMove(app, weapon2.projectilePositions.index(elem), dx, dy)
    if player.equippedWeapon == weapon3:
        for elem in weapon3.projectilePositions:
            if elem[4] < 60:
                dx, dy = elem[2], elem[3]
                drawCircle(elem[0], elem[1], 10, fill = 'black')
                weapon3.projectileMove(app, weapon3.projectilePositions.index(elem), dx, dy)
                elem[4] += 1
            else:
                if len(bossList) > 1:
                    distancefromBoss0 = distance(elem[0], elem[1], *bossList[0].position)
                    distancefromBoss1 = distance(elem[0], elem[1], *bossList[1].position)
                    if distancefromBoss0 < distancefromBoss1:
                        dx, dy = ((bossList[0].position[0] - elem[0])/70,
                                  (bossList[0].position[1] - elem[1])/70)
                    else:
                        dx, dy = ((bossList[1].position[0] - elem[0]) / 70,
                                  (bossList[1].position[1] - elem[1]) / 70)
                else:
                    dx, dy = ((bossList[0].position[0] - elem[0])/70,
                              (bossList[0].position[1] - elem[1]) / 70)
                if dx!=0:
                    dx, dy = angleMaker(7, dx, dy)
                    drawCircle(elem[0], elem[1], 10, fill = 'black')
                    weapon3.projectileMove(app, weapon3.projectilePositions.index(elem), dx, dy)
    if player.equippedWeapon == weapon4:
        for elem in weapon4.projectilePositions:
            drawLine(elem[0], elem[1], elem[0], elem[1] + 20)
            weapon4.projectileMove(app, weapon4.projectilePositions.index(elem), 0, 5)

####### ALL APP FUNCTIONS
########

def onMousePress(app, mouseX, mouseY):
    if app.customLevelEditor:
        for i in range(4):
            if distance(mouseX, mouseY, 1450, i * 150 + 150) < 50:
                if i == 0 and boss1 not in customLevel.bosses:
                    customLevel.bosses.append(boss1)
                elif i == 1 and boss2 not in customLevel.bosses:
                    customLevel.bosses.append(boss2), customLevel.bosses.append(boss3)
                elif i == 2 and boss4 not in customLevel.bosses:
                    customLevel.bosses.append(boss4)
                elif i == 3:
                    print('AHHH')
                    customLevel.platforms = [leftBorder, topBorder, rightBorder, bottomBorder]
                return
        if distance(mouseX,mouseY, 200, 700) < 50:
            app.customLevelEditor = False
            app.homeScreen = True
        if not customLevel.makingPlatform:
            customLevel.platformOutlinePosition = [mouseX, mouseY, 1, 1]
        if not customLevel.makingPlatform:
            for platform in customLevel.platforms[4:]:
                    if rectanglesOverlap(*platform, mouseX + 2, mouseY, 5, 5):
                        customLevel.platforms.pop(customLevel.platforms.index(platform))
                        return
        if customLevel.makingPlatform:
            customLevel.addPlatform(customLevel.platformOutlinePosition)
        customLevel.makingPlatform = not customLevel.makingPlatform

    if app.homeScreen:
        if distance(mouseX, mouseY, 200, 500) < 100:
            app.homeScreen = False
            boss1.active = True
            for boss in bosses[1:]:
                boss.active = False
            app.level1Loaded = True
            app.level1Loaded = True
        if distance(mouseX, mouseY, 500, 500) < 100 and app.level1Completed:
            app.homeScreen = False
            boss1.active = False
            boss4.active = False
            app.level2Loaded = True
            boss2.active = True
            boss3.active = True
        if distance(mouseX, mouseY, 1100, 500) < 100:
            app.weaponSelectionScreen = True
            app.homeScreen = False
        if distance(mouseX,mouseY, 1400, 500) < 100:
            app.customLevelEditor = True
            app.homeScreen = False
        if distance(mouseX, mouseY, 1400, 200) < 100:
            app.customLevel = True
            app.homeScreen = False
            for boss in customLevel.bosses:
                boss.active = True
    if app.deathScreen and distance(mouseX, mouseY, app.width/2, app.height/2 + 150) < 100:
        lossParametersReset(app)
        for weapon in weapons:
            weapon.reset()
        for boss in bosses:
            boss.reset(boss.originalHealth)
        player.reset(100)
    if app.victoryScreen and distance(mouseX, mouseY, app.width/2, app.height/2 + 150) < 100:
        victoryParametersReset(app)
        for weapon in weapons:
            weapon.reset()
        for boss in bosses:
            boss.reset(boss.originalHealth)
        player.reset(100)
    if app.weaponSelectionScreen:
        for i in range(4):
            if distance(mouseX, mouseY, 350, i * 200 + 100) < 100:
                player.equippedWeapon = weapons[i]
        if distance(mouseX, mouseY, 900, 600) < 100:
            app.weaponSelectionScreen = False
            app.homeScreen = True
    if player.equippedWeapon == weapon2 and anyLevelLoaded(app):
        weapon2.firing = True
        weapon2.mousePosition = [mouseX, mouseY]
        if len(weapon2.projectilePositions) < 10:
            dx, dy = ((weapon2.mousePosition[0] - player.position[0])/70, 
                      (weapon2.mousePosition[1] - player.position[1])/70)
            if dx != 0:
                dx, dy = angleMaker(8, dx, dy)
                weapon2.projectilePositions.append([*player.position, dx, dy])
    if (player.equippedWeapon == weapon3 and anyLevelLoaded(app) and 
            len(weapon3.projectilePositions) < 16):
        x, y = player.position[0], player.position[1]
        weapon3.projectilePositions += [[x+25,y,3,0,0],[x-25,y,-3,0,0],
                                        [x,y+25,0,3,0],[x,y-25,0,-3,0]]
    if player.equippedWeapon == weapon4 and anyLevelLoaded(app):
        weapon4.projectilePositions += [[mouseX, random.randint(20, 40)], 
            [mouseX - 30, random.randint(20, 40)], [mouseX + 30, random.randint(20, 40)]]
        
def onMouseMove(app, mouseX, mouseY):
    if app.customLevelEditor and customLevel.makingPlatform:
        if (mouseX > customLevel.platformOutlinePosition[0] and
            mouseX -customLevel.platformOutlinePosition[0] > 0 and
            mouseY -customLevel.platformOutlinePosition[1] > 0):
            customLevel.platformOutlinePosition[2:] = [mouseX -customLevel.platformOutlinePosition[0],
                                                    mouseY -customLevel.platformOutlinePosition[1] ]

def onMouseDrag(app, mouseX, mouseY):
    if anyLevelLoaded(app) and player.equippedWeapon == weapon1:
        weapon1.mousePosition = [mouseX, mouseY]
        weapon1.firing = True

def onMouseRelease(app, mouseX, mouseY):
    if anyLevelLoaded(app):
        if weapon1.firing:
            weapon1.firing = False

def redrawAll(app):
    if app.homeScreen:
        drawHomeScreen(app)
    if app.level1Loaded:
        drawLevel1(app)
        boss1Attack(app)
        if app.counter == 179:
            boss1.teleport(boss1.projectX, boss1.projectY)
        elif 100 < app.counter < 180:
            projectBossNextSpot(app, boss1.projectX, boss1.projectY)
        weaponShootingMechanics(app, [boss1])
    if app.level2Loaded:
        drawLevel2(app)
        level2Attack()
        weaponShootingMechanics(app, [boss2, boss3])
        if boss2.attack1Ready and 0 < app.counter < 60:
            drawCircle(boss2.projectX, 100, boss2.radius, fill = None, border = 'black')
            drawCircle(boss3.projectX, 100, boss3.radius, fill = None, border = 'black')
    if app.weaponSelectionScreen:
        for i in range(4):
            drawRect(300, i * 200 + 50, 100, 100, fill = None, border = 'black')
            drawLabel('click here to choose weapon',300, i * 200 + 100, fill=None, border='black')
        drawWeaponDescriptions(app)
        drawRect(900, 600, 100, 100, align='center')
    if app.customLevelEditor:
        drawLevelEditor(app)
        if customLevel.makingPlatform:
            drawRect(*customLevel.platformOutlinePosition, fill = None, border='blue')
    if app.customLevel:
        weaponShootingMechanics(app, customLevel.bosses)
        drawCustomLevel(app)
        if boss1 in customLevel.bosses and boss1.active:
            boss1Attack(app)
            drawBoss1()
            if app.counter == 179:
                boss1.teleport(boss1.projectX, boss1.projectY)
            elif 100 < app.counter < 180:
                projectBossNextSpot(app, boss1.projectX, boss1.projectY)
        if boss2 in customLevel.bosses and boss2.active:
            if boss2.attack1Ready and 0 < app.counter < 60:
                drawCircle(boss2.projectX, 100, boss2.radius, fill = None, border = 'black')
                drawCircle(boss3.projectX, 100, boss3.radius, fill = None, border = 'black')
            level2Attack()
            drawBoss2()
            drawBoss3()
    if app.deathScreen:
        drawDeathScreen(app)
    if app.victoryScreen:
        drawVictoryScreen(app)

def onStep(app):
    if boss1.active:
        if app.counter == 0:
            boss1.projectX = random.randint(70, app.width - 70)
            boss1.projectY = random.randint(70 , app.height - 70)
        if app.counter == 180:
            boss1.attack1Ready = not boss1.attack1Ready
        if distance(*player.position, *boss1.position) < 100:
            player.removeHealth(1)
        if app.level1Loaded:
            if player.health <= 0:
                app.level1Loaded = False
                boss1.active = False
                app.deathScreen = True
            if boss1.health <= 0:
                app.level1Loaded = False
                app.victoryScreen = True
                boss1.active = False
                app.level1Completed = True
        if boss1.attack2Ready:
            if app.counter % 30 == 0:
                boss1.attack2Positions.append(boss1.position + player.position + boss1.position)
        if boss1.attack3Ready:
            if app.counter % 5 == 0:
                boss1.attack2Positions.append(boss1.position + player.position + boss1.position)
    if boss2.active or boss3.active:
        if app.counter == -1:
            boss2.attack2Positions = [800, 400, []]
            boss3.attack2Positions = [800, 400, []]
            boss2.position, boss3.position = [300, 100], [900, 100]
        if app.counter == 0 and boss2.attack1Ready:
            boss2.projectX, boss3.projectX = random.randint(100, 500), random.randint(900, 1400)
        if app.counter == 60 and boss2.attack1Ready:
            boss2.position = [boss2.projectX, 100]
            boss3.position = [boss3.projectX, 100]
        if boss2.attack2Ready:
            boss2.attack2Positions[:2] = [player.position[0] + 100, player.position[1] + 100]
            boss3.attack2Positions[:2] = [player.position[0]- 100, player.position[1]- 100]
        if boss2.attack2Ready and app.counter % 60 == 0:
            x,y = boss2.position[0],boss2.position[1]
            boss2.attack2Positions[2] += boss2.octagonalPositions(x, y)
            x1,y1 = boss3.position[0],boss3.position[1]
            boss3.attack2Positions[2] += boss3.octagonalPositions(x1, y1)
        if boss2.attack3Ready:
            boss2.attack3Positions[:2] = [player.position[0], player.position[1]]
        if boss3.attack3Ready:
            boss3.attack3Positions[:2] = [player.position[0], player.position[1]]
        if boss2.attack3Ready and app.counter % 60 == 0:
            boss2.attack3EnragedPositions = [*player.position, *boss2.position]
            x,y = boss2.position[0],boss2.position[1]
            boss2.attack3Positions[2] += boss2.shotgunPositions(x, y)
        if boss3.attack3Ready and app.counter % 60 == 0:
            boss3.attack3EnragedPositions = [*player.position, *boss3.position]
            x,y = boss3.position[0],boss3.position[1]
            boss3.attack3Positions[2] += boss2.shotgunPositions(x, y)
        if app.level2Loaded:
            if player.health <= 0:
                app.level2Loaded = False
                app.deathScreen = True
                boss2.active = False
            if boss2.health <=0 and boss3.health <= 0:
                app.level2Loaded = False
                app.victoryScreen = True
                boss2.active = False
    if app.customLevel:
        if player.health <= 0:
            app.customLevel = False
            app.deathScreen = True
        count = 0
        for boss in customLevel.bosses:
            if boss.health >= 0:
                count += 1
            else:
                boss.active = False
        if count == 0:
            app.customLevel = False
            app.victoryScreen = True
    if player.jumping:
        player.move(app, 0, -19)
    if anyLevelLoaded(app):
        player.move(app, 0, player.gravity)
        app.counter += 1
        if app.counter == 180:
            app.counter = 0
def onKeyPress(app, key):
    pass

def onKeyRelease(app, key):
    if key == 'w':
        player.jumping = False

def onKeyHold(app, keys):
    if anyLevelLoaded(app):
        if 'd' in keys and 'a' not in keys:
            player.move(app, player.speed, 0)
        if 'a' in keys and 'd' not in keys:
            player.move(app, -player.speed, 0)
        if 'w' in keys:
            player.jumping = True

##### ALL LEVEL 1 STUFF
#####

def drawLevel1(app):
    drawBoss1()
    drawEnviornment1()
    drawPlayer(app)

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

def projectBossNextSpot(app, newX, newY):
    drawCircle(newX, newY, 100, fill = None, border = 'black', borderWidth = 2)
    drawLabel('boss is about to move here', newX, newY)

def boss1Attack(app):
    if boss1.health > 300:
        boss1Attack1(app)
    elif boss1.health > 100:
        boss1.attack2Ready = True
        boss1Attack2(app)
    else:
        boss1.attack3Ready = True
        boss1Attack3(app)

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
        boss1.shootProjectile(boss1.attack2Positions.index(elem), dx, dy)

def boss1Attack3(app):
    boss1Attack2(app)


##### ALL LEVEL 2 STUFF
#####
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

def level2Attack():
    if boss2.health > 500 and boss3.health > 500:
        boss1.attack1Ready = True
        level2Attack1()
        if (boss2.position[0] < player.position[0] < boss3.position[0] and
            boss2.position[1] - 10 < player.position[1] < boss2.position[1] + 10):
            player.removeHealth(boss2.damage//10)
        if boss2.touching() or boss3.touching():
            player.removeHealth(boss2.damage)
    elif (boss2.health <= 500 or boss3.health <= 500) and (boss2.health > 0) and (boss3.health > 0):
        boss2.attack1Ready = False
        boss2.attack2Ready = True
        if boss2.touching() or boss3.touching():
            player.removeHealth(boss2.damage)
        level2Attack2()
    elif boss2.health <= 0 and boss3.health > 0:
        boss2.attack2Ready = False
        boss3.attack3Ready = True
        if boss3.touching():
            player.removeHealth(boss3.damage)
        boss3.attack3()
    elif boss2.health >0 and boss3.health <=0:
        boss2.attack2Ready = False
        boss2.attack3Ready = True
        if boss2.touching():
            player.removeHealth(boss2.damage)
        boss2.attack3()

def level2Attack1():
    drawLine(*boss2.position, *boss3.position)
    dy = 3
    boss2.bossMove(0, dy)
    boss3.bossMove(0, dy)

def level2Attack2():
    dx, dy = (boss2.attack2Positions[0] - boss2.position[0])/70, (boss2.attack2Positions[1] - boss2.position[1])/70
    dx2, dy2 = (boss3.attack2Positions[0] - boss3.position[0])/70, (boss3.attack2Positions[1] - boss3.position[1])/70
    dx, dy = angleMaker(2, dx, dy)
    dx2, dy2 = angleMaker(2, dx2, dy2)
    boss2.bossMove(dx, dy)
    boss3.bossMove(dx2, dy2)
    for elem in boss2.attack2Positions[2]:
        drawCircle(elem[0], elem[1], 10, fill = 'gray')
        dx, dy = elem[2], elem[3]
        boss2.shootProjectilesOutwards(boss2.attack2Positions[2].index(elem), dx, dy)
    for elem in boss3.attack2Positions[2]:
        drawCircle(elem[0], elem[1], 10, fill = 'gray')
        dx, dy = elem[2], elem[3]
        boss3.shootProjectilesOutwards(boss3.attack2Positions[2].index(elem), dx, dy)

def drawCustomLevel(app):
    for platform in customLevel.platforms:
        drawRect(*platform, fill = 'blue')
    drawPlayer(app)

##### MISC DRAWINGS & RESETS
#####
def drawPlayer(app):
    drawRect(*player.position, 50, 70, fill = 'hotpink', align = 'center')
    drawCircle(*player.position, 25, fill = None, border = 'black')
    drawRect(1400, 740, 104, 10, fill = None, borderWidth = 2, border = 'black')
    drawLabel('Player Health', 1452, 730, align='center')
    if player.health > 0:
        drawRect(1402, 742, player.health, 8, fill = 'green')

def drawHomeScreen(app):
    drawLabel('Welcome to Boss Fight 112', app.width/2, 100, align = 'center', size = 20)
    drawRect(100, 400, 200, 200, fill = None, borderWidth = 4, border = 'black')
    drawLabel('level1', 200, 500, align='center')
    drawRect(400, 400, 200, 200, fill = None, borderWidth = 4, border = 'black')
    drawLabel('level2', 500, 500, align='center')
    drawRect(700, 400, 200, 200, fill = None, borderWidth = 4, border = 'black')
    drawLabel('level3', 800, 500, align='center')
    drawRect(1000, 400, 200, 200, fill = None, borderWidth = 4, border = 'black')
    drawLabel('Weapon Selection Screen', 1100, 500, align='center')
    drawRect(1300, 400, 200, 200, fill = None, borderWidth = 4, border = 'black')
    drawLabel('Custom Level Editor', 1400, 500, align='center')
    drawRect(1300, 100, 200, 200, fill=None, borderWidth=4, border='black')
    drawLabel('Play Custom Level', 1400, 200)
   
def drawDeathScreen(app):
    drawLabel('You died bruh', app.width/2, app.height/2, align = 'center', size = 25)
    drawLabel('lol lmao', app.width/2, app.height/2 + 50, align = 'center', size = 25)
    drawRect(app.width/2, app.height/2 + 150, 100, 100, align  = 'center', fill = None, border = 'black')

def drawVictoryScreen(app):
    drawLabel('You won bruh', app.width/2, app.height/2, align = 'center', size = 25)
    drawLabel('lol lmao good work', app.width/2, app.height/2 + 50, align = 'center', size = 25)
    drawRect(app.width/2, app.height/2 + 150, 100, 100, align  = 'center', fill = None, border = 'black')

def drawWeaponDescriptions(app):
    drawLabel('Lazer Pointer, Click the screen to shoot a laser at that position', 600, 100, align = 'center')
    drawLabel('Damage Per Second = 60', 600, 120, align = 'center')
    drawLabel('Basic Bullet Gun, click to shoot a projectile in that direction', 600, 300, align = 'center')
    drawLabel(f'Damage Per Pellet = {weapon2.damage}', 600, 320, align = 'center')
    drawLabel('Razorblade Typhoon, click to shoot tracking projectiles in a volley around you', 620, 
              500, align = 'center')
    drawLabel(f'Damage Per Pellet = {weapon3.damage}', 600, 520, align = 'center')
    drawLabel('Blood rain, click to summon projectiles from the air', 600, 700, align ='center')
    drawLabel(f'Damage Per Pellet = {weapon4.damage}', 600, 720, align='center')

def drawLevelEditor(app):
    drawRect(200, 700, 50, 50, align='center', fill = None, border='black')
    drawLabel('CUSTOM LEVELS! CLICK TO MAKE PLATFORMS AND CHOOSE BOSSES', 800, 100, align='center', size = 15)
    drawLabel('Return', 200, 700, align='center')
    drawLabel('Click to Enable Boss1', 1450, 150, align = 'center')
    drawLabel('Click To Enable Boss2&3', 1450, 300, align='center')
    drawLabel('Click To Enable Boss4', 1450, 450, align='center')
    drawLabel('Clear All', 1450, 600, align='center')
    for platform in customLevel.platforms:
        drawRect(*platform, fill = 'blue')
    for i in range(4):
        drawRect(1400, i * 150 + 100, 100, 100, fill=None, border='black')

def victoryParametersReset(app):
    app.homeScreen = True
    app.counter = -1
    app.jumping = False
    app.victoryScreen = False

def lossParametersReset(app):
    app.deathScreen = False
    app.homeScreen = True
    app.jumping = False
    app.counter = -1


def main():
    runApp()
main()