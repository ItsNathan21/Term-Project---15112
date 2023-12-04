from cmu_graphics import *
import random
import math
from PIL import Image
# from numpy import *

####### INITIALIZING VALUES AND BORDERS
#######
leftBorder = [0, 0, 20, 800]
topBorder = [0, 0, 1600, 20]
rightBorder = [1580, 0, 20, 800]
bottomBorder = [0, 780, 1600, 20]

level1Platforms = [leftBorder, topBorder, rightBorder, bottomBorder, [20, 400, 600, 50], 
                   [300, 250, 50, 400], [1300, 0, 50, 600], [1175, 400, 300, 20], [1275, 575, 100, 100]]
level2Platforms = [leftBorder, topBorder, rightBorder, bottomBorder, [0, 150, 400, 50], [0, 600, 400, 50],
                   [1200, 150, 400, 50], [1200, 600, 400, 50], [500, 500, 600, 25]]
leve3Platforms = [leftBorder, topBorder, rightBorder, [0, 150, 400, 50], [0, 600, 400, 50],
                   [1200, 150, 400, 50], [1200, 600, 400, 50], [500, 500, 600, 25]]

def onAppStart(app):
    def openImage(fileName):
        return Image.open(fileName)
    app.weapon2BulletImage = openImage("sprites/bullet1.png")
    app.weapon2BulletImageFlip = app.weapon2BulletImage.transpose(Image.FLIP_LEFT_RIGHT)
    app.boss1Tooth = openImage("sprites/boss1Attack1.png")
    app.deathScreenImage = openImage("sprites/gravestones.jpg")
    app.victoryScreenImage = openImage("sprites/victory.jpg")
    app.boss2Phase1 = openImage("sprites/boss2.png")
    app.boss3Phase1 = openImage("sprites/boss3.png")
    app.staff = openImage("sprites/staff.png")


    app.boss2Anim = openImage("sprites/boss2Animation.png")
    app.boss2Animation = []
    app.boss3Anim = openImage("sprites/boss3Animation.png")
    app.boss3Animation = []
    for i in range(4):
        sprite = CMUImage(app.boss2Anim.crop((320*i, 0, 320+320*i, 320)))
        app.boss2Animation.append(sprite)
        sprite1 = CMUImage(app.boss3Anim.crop((320*i, 0, 320+320*i, 320)))
        app.boss3Animation.append(sprite1)
    app.boss2AnimationCounter = 0
    app.boss3AnimationCounter = 0


    app.boss1Anim = openImage("sprites/boss1Animation.png")
    app.boss1AnimMirror = app.boss1Anim.transpose(Image.FLIP_LEFT_RIGHT)
    app.boss1Animation = []
    app.boss1AnimationMirror = []
    for i in range(2):
        sprite = CMUImage(app.boss1Anim.crop((275*i, 0, 275 + 275*i, 275)))
        sprite2 = CMUImage(app.boss1AnimMirror.crop((275*i, 0, 275 + 275*i, 275)))
        app.boss1Animation.append(sprite)
        app.boss1AnimationMirror.append(sprite2)
    app.boss1AnimationCounter = 0


    app.playerAnim = openImage("sprites/playerAnimation.png")
    app.playerAnimMir = app.playerAnim.transpose(Image.FLIP_LEFT_RIGHT)
    app.playerAnimation, app.playerAnimationMirror = [], []
    for i in range(3):
        sprite = CMUImage(app.playerAnim.crop((320*i, 0, 320+320*i, 320)))
        sprite1 = CMUImage(app.playerAnimMir.crop((320*i, 0, 320+320*i, 320)))
        app.playerAnimation.append(sprite)
        app.playerAnimationMirror.append(sprite1)
    app.playerAnimationCounter = 0


    app.typhoonAnim = openImage("sprites/typhoonAnimation.png")
    app.typhoonAnimation = []
    for i in range(5):
        sprite = CMUImage(app.typhoonAnim.crop((32*i, 0, 32 + 32*i, 32)))
        app.typhoonAnimation.append(sprite)
    app.typhoonAnimationCounter = 0
    app.typhoonBook = openImage("sprites/razorBook.png")

    
    app.weapon2BulletImage, app.weapon2BulletImageFlip = app.weapon2BulletImage.convert('RGBA'), app.weapon2BulletImageFlip.convert('RGBA')
    app.weapon2BulletImage = CMUImage(app.weapon2BulletImage)
    app.weapon2BulletImageFlip = CMUImage(app.weapon2BulletImageFlip)
    app.boss1Tooth = CMUImage(app.boss1Tooth)
    app.typhoonBook = CMUImage(app.typhoonBook)
    app.deathScreenImage = CMUImage(app.deathScreenImage)
    app.victoryScreenImage = CMUImage(app.victoryScreenImage)
    app.boss2Phase1 = CMUImage(app.boss2Phase1)
    app.boss3Phase1 = CMUImage(app.boss3Phase1)
    app.staff = CMUImage(app.staff)

    app.width, app.height = 1600, 800
    app.stepsPerSecond = 60
    app.colors, app.platColors = [], []
    app.cycleColors=['red','orange','green','blue','purple','yellow','lightgray']
    app.setMaxShapeCount(10000)
    app.counter = -1
    app.gravity = 0.0001
    app.homeScreen = True
    app.weaponSelectionScreen, app.armorSelectionScreen = False, False
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
        self.facingLeft = False
        self.gravity = 10
        self.jumping = False
        self.weapons = [weapon1, weapon2, weapon3, weapon4]
        self.equippedWeapon = weapon1
        self.equippedArmor = None
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
        self.attack1Positions =[]
        self.attack2Positions = [0,0,[]]
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
        return [[x+25,y,x+300,y-20,0,8],[x-25,y,x-300,y-20,0,-8],[x,y+25,x,y-300,0,0],
                [x,y-25,x,y+300,0,0],[x+25,y+25,x+300,y-50,0,8],
                [x+25,y-25,x+300,y,0,8],[x-25,y-50,x-300,y,0,-8],[x-25,y+25,x+300,y+20,0,-8]]
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
                drawCircle(elem[0], elem[1], 10, fill = 'gray', border='black')
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
    def shootProjectile(self, app, index, dx, dy):
        self.attack2Positions[2][index][0] += dx
        self.attack2Positions[2][index][1] += dy

        for platform in currentlyLoadedLevel(app)[0]:
            if rectanglesOverlap(*platform, self.attack2Positions[2][index][0], 
                                 self.attack2Positions[2][index][1], 10, 10):
                self.attack2Positions[2].pop(index)
                return
        if distance(self.attack2Positions[2][index][0], 
                    self.attack2Positions[2][index][1], *player.position) < 30:
            player.removeHealth(self.damage)
            self.attack2Positions[2].pop(index)
            return
    def shootProjectilesOutwards(self, app, index, dx, dy):
        self.attack2Positions[2][index][0] += dx
        self.attack2Positions[2][index][1] += dy
        for platform in currentlyLoadedLevel(app)[0]:
            if rectanglesOverlap(*platform, 
                self.attack2Positions[2][index][0], self.attack2Positions[2][index][1], 10, 10):
                self.attack2Positions[2].pop(index)
                return
        if distance(self.attack2Positions[2][index][0], 
                self.attack2Positions[2][index][1], *player.position) < 50:
            player.removeHealth(self.damage)
            self.attack2Positions[2].pop(index)
            return
    def randomBG(self, app, index):
        if self.attack1Positions[index][2] < 20 or len(self.attack1Positions) > 20:
            self.attack1Positions.pop(index)
        point = [*self.attack1Positions[index][:2]]
        leng = self.attack1Positions[index][2]
        drawRect(point[0]-leng,point[1]-leng,leng,leng,border='black',
                 opacity=5,fill=app.cycleColors[self.attack1Positions[index][3]])
        self.attack1Positions[index][2]-=1
        
        

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
        self.projectilePositions[index][1] += 2
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
        if app.level3Loaded:
            if self.projectilePositions[index][1] > 800:
                self.projectilePositions.pop(index)
                return
    def reset(self):
        self.firing = False
        self.mousePosition = []
        self.projectilePositions = []
    def parabolicMove(self, app, index):
        dx = self.projectilePositions[index][5]
        if (self.projectilePositions[index][3] < (self.projectilePositions[index][1] - 20) and 
            self.projectilePositions[index][4] == 0):
            m = max(self.projectilePositions[index][3],self.projectilePositions[index][1])
            s = min(self.projectilePositions[index][3],self.projectilePositions[index][1])
            dy = (s-m)/30
        else:
            self.projectilePositions[index][4] = 1
            m = max(self.projectilePositions[index][3],self.projectilePositions[index][1])
            s = min(self.projectilePositions[index][3],self.projectilePositions[index][1])
            dy = (m-s)/30
        self.projectilePositions[index] = [self.projectilePositions[index][0] + dx, 
                                           self.projectilePositions[index][1] + dy,
                                           *self.projectilePositions[index][2:]]       
        for platform in currentlyLoadedLevel(app)[0]:
            if rectanglesOverlap(*platform, self.projectilePositions[index][0], 
                            self.projectilePositions[index][1], 10, 10) or (
                            self.projectilePositions[index][1]  > 800):
                self.projectilePositions.pop(index)
                return 
        for boss in currentlyLoadedLevel(app)[1:]:
            if distance(self.projectilePositions[index][0], 
                        self.projectilePositions[index][1], *boss.position) < boss.radius:
                self.projectilePositions.pop(index)
                boss.takeDamage(self.damage)
                return
            
        
        
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
        self.colors = []
    def addPlatform(self, platform):
        self.platforms.append(platform)

weapon1 = Weapon(1, 'laser')
weapon2 = Weapon(100, 'bulletboy')
weapon3 = Weapon(5, 'Razoablade Typhoon')
weapon4 = Weapon(50, 'lightning')
weapon5 = Weapon(50, 'teslaCoil')

player = Player(100, 10)

level1 = Level(level1Platforms)
level2 = Level(level2Platforms)
level3 = Level(leve3Platforms)
customLevel = Level([leftBorder, topBorder, rightBorder, bottomBorder])


boss1 = Boss(500, 10, 100)
boss2, boss3 = Boss(1000, 20, 50), Boss(1000, 20, 50)
boss4 = Boss(3000, 30, 300)

bosses = [boss1, boss2, boss3, boss4]
weapons = [weapon1, weapon2, weapon3, weapon4]

lightArmor = Armor(300)
mediumArmor = Armor(500)
heavyArmor = Armor(700)

armor=[lightArmor, mediumArmor,heavyArmor]

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

def lineOfSightCheck(app, object1X, object1Y, object2X, object2Y, amount):
    dx = (object2X - object1X) / amount
    dy = (object2Y - object1Y) / amount
    rect1 = [object1X + dx, object1Y + dy, 10, 10]
    for i in range(amount):
        drawRect(*rect1, fill = None)
        for platform in currentlyLoadedLevel(app)[0]:
            if rectanglesOverlap(*platform, *rect1):
                    return False
        rect1 = [rect1[0] + dx, rect1[1] + dy, 10, 10]
    return True

def weaponShootingMechanics(app, bossList):
    if weapon1.firing and lineOfSightCheck(app, *player.position, *weapon1.mousePosition, 35):
        drawPolygon(*player.position, weapon1.mousePosition[0]-5, weapon1.mousePosition[1],
                    weapon1.mousePosition[0]+5,weapon1.mousePosition[1])
        for elem in bossList:
            if distance(*weapon1.mousePosition, *elem.position) < 100:
                elem.takeDamage(weapon1.damage)
    if weapon2.firing:
        for elem in weapon2.projectilePositions:
            print(elem[0],elem[1],'elem')
            drawCircle(elem[0], elem[1], 10, fill='gray')
            weapon2.parabolicMove(app, weapon2.projectilePositions.index(elem))
    if player.equippedWeapon == weapon3:
        for elem in weapon3.projectilePositions:
            drawImage(app.typhoonAnimation[app.typhoonAnimationCounter], elem[0], elem[1], align='center', 
                      width=90, height = 70)
            if elem[4] < 60:
                dx, dy = elem[2], elem[3]
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
                    weapon3.projectileMove(app, weapon3.projectilePositions.index(elem), dx, dy)

    if player.equippedWeapon == weapon4:
        for list in weapon4.projectilePositions:
            for i in range(len(list)-2):
                firstPoint, secondPoint = list[i], list[i+1]
                drawPolygon(firstPoint[0]-5, firstPoint[1], firstPoint[0]+5, firstPoint[1], 
                            *secondPoint, fill='white', border='blue')
            updateLightningPositions(app, weapon4.projectilePositions.index(list))


def updateLightningPositions(app, index):
    list = weapon4.projectilePositions[index]
    start, end, previous = list[0], list[-1], list[-2]
    center = [(previous[0]+list[-3][0])/2, (previous[1]+list[-3][1])/2]
    if previous == end or not lineOfSightCheck(app, *previous, *list[-3], 1):
        weapon4.projectilePositions.pop(index)
        return
    if distance(*previous, *end) < 50:
        list = list[:-1] + [end] + list[-1:]
        weapon4.projectilePositions[index]=list
        return
    nextX = random.randint(start[0]-20, start[0]+40)
    nextY = random.randint(previous[1], previous[1]+40)
    list = list[:-1] + [[nextX, nextY]] + list[-1:]
    for boss in currentlyLoadedLevel(app)[1:]:
        if distance(*center, *boss.position) < boss.radius:
            boss.takeDamage(weapon4.damage)
            weapon4.projectilePositions.pop(index)
            return
    weapon4.projectilePositions[index] = list    
 

####### ALL APP FUNCTIONS
########

def onMousePress(app, mouseX, mouseY):
    if app.homeScreen:
        for i in range(3):
            if rectanglesOverlap(mouseX, mouseY, 5, 5, 100, 200 + 200*i, 400, 75):
                app.homeScreen=False
                if i == 0:
                    app.level1Loaded=True
                    boss1.active = True
                elif i == 1:
                    app.level2Loaded=True
                    boss2.active = True
                    boss3.active=True
                elif i == 2:
                    app.level3Loaded=True
                    boss4.active = True
        for i in range(2):
            if rectanglesOverlap(mouseX, mouseY, 5, 5, 1100, 460 + 150*i, 400, 75):
                app.homeScreen = False
                if i == 0:
                    app.customLevelEditor = True
                elif i == 1:
                    app.customLevel = True
                    for boss in customLevel.bosses:
                        boss.active = True
        for i in range(2):
            if rectanglesOverlap(mouseX, mouseY, 5, 5, 600 + 250*i, 200, 200, 200):
                app.homeScreen = False
                if i == 0:
                    app.weaponSelectionScreen = True
                elif i == 1:
                    app.armorSelectionScreen = True

    if app.customLevelEditor:
        for i in range(4):
            if distance(mouseX, mouseY, 1450, i * 150 + 200) < 50:
                if i == 0 and boss1 not in customLevel.bosses:
                    customLevel.bosses.append(boss1)
                elif i == 1 and boss2 not in customLevel.bosses:
                    customLevel.bosses.append(boss2), customLevel.bosses.append(boss3)
                elif i == 2 and boss4 not in customLevel.bosses:
                    customLevel.bosses.append(boss4)
                elif i == 3:
                    customLevel.platforms = [leftBorder, topBorder, rightBorder, bottomBorder]
                return
        for i in range(2):
            if distance(mouseX, mouseY, 250,625+100*i)<38:
                if i == 0:
                    app.colors=[]
                    app.platColors=[]
                    return
                else:
                    app.homeScreen = True
                    app.customLevelEditor = False
                    return
        colors = ['red', 'yellow', 'green', 'blue', 'purple', 'black', 'white']
        for i in range(7):
            if distance(mouseX,mouseY,75,225+100*i) < 25:
                if colors[i] not in app.colors:
                    app.colors.append(colors[i])
                    return
                else:
                    app.colors.pop(app.colors.index(colors[i]))
                    return  
        for i in range(7):
            if distance(mouseX,mouseY,175,225+100*i)<25:
                if colors[i] not in app.platColors:
                    app.platColors.append(colors[i])
                    return
                else:
                    app.platColors.pop(app.platColors.index(colors[i]))
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
    
    if app.deathScreen and distance(mouseX, mouseY, 1250, 350) < 100:
        lossParametersReset(app)
        for weapon in weapons:
            weapon.reset()
        for boss in bosses:
            boss.reset(boss.originalHealth)
        if player.equippedArmor:
            player.reset(500 + player.equippedArmor.shield)
        else:
            player.reset(500)
    
    if app.victoryScreen and distance(mouseX, mouseY, app.width/2, 300) < 100:
        victoryParametersReset(app)
        for weapon in weapons:
            weapon.reset()
        for boss in bosses:
            boss.reset(boss.originalHealth)
        if player.equippedArmor:
            player.reset(500 + player.equippedArmor.shield)
        else:
            player.reset(500)

    if app.weaponSelectionScreen:
        for i in range(4):
            if rectanglesOverlap(mouseX, mouseY, 5,5, 350, 50+200*i, 300, 100):
                player.equippedWeapon = weapons[i]
        if rectanglesOverlap(mouseX, mouseY, 5, 5, 50, 200, 200, 200):
            app.homeScreen = True
            app.weaponSelectionScreen = False
    
    if app.armorSelectionScreen:
        for i in range(3):
            if rectanglesOverlap(mouseX, mouseY, 5,5, 350, 50+200*i, 300, 100):
                if armor[i] != player.equippedArmor:
                    player.reset(500)
                    player.equippedArmor = armor[i]
                    player.health+=player.equippedArmor.shield
        if rectanglesOverlap(mouseX, mouseY, 5, 5, 50, 200, 200, 200):
            app.homeScreen = True
            app.armorSelectionScreen = False

    if player.equippedWeapon == weapon2 and anyLevelLoaded(app):
        weapon2.firing = True
        dx = (mouseX - player.position[0])/50
        end = mouseY if mouseY < player.position[1] else player.position[1] -20
        weapon2.projectilePositions.append([player.position[0], player.position[1], mouseX, end, 0, dx])
   
    
    if (player.equippedWeapon == weapon3 and anyLevelLoaded(app) and 
            len(weapon3.projectilePositions) < 10):
        x, y = player.position[0], player.position[1]
        weapon3.projectilePositions += [[x+25,y,3,0,0],[x-25,y,-3,0,0],
                                        [x,y+25,0,3,0],[x,y-25,0,-3,0]]
        
    if player.equippedWeapon == weapon4 and anyLevelLoaded(app):
        if mouseY > 50:
            startingPoint = [mouseX, 21]
            firstPoint = [random.randint(mouseX-50, mouseX+50), random.randint(50, 100)]
            endPoint = [mouseX, mouseY]
            list = [startingPoint, firstPoint, endPoint]
            weapon4.projectilePositions.append(list)
        
    if player.equippedWeapon == weapon5:
        centerPoint = [[mouseX, mouseY]]
        starterPoints = [[mouseX +50, mouseY],[mouseX-50, mouseY],[mouseX,mouseY+50],
                         [mouseX,mouseY-50]]
        weapon5.projectilePositions = centerPoint + starterPoints


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
        level2Attack(app)
        weaponShootingMechanics(app, [boss2, boss3])
        if boss2.attack1Ready and 0 < app.counter < 60:
            drawCircle(boss2.projectX, 100, boss2.radius, fill = None, border = 'black')
            drawCircle(boss3.projectX, 100, boss3.radius, fill = None, border = 'black')
   
   
   
    if app.level3Loaded:
        drawLevel3(app)
        level3Attack(app)
        weaponShootingMechanics(app, [boss4])
        drawBoss4(app)


    if app.customLevel:
        drawCustomLevel(app)
        weaponShootingMechanics(app, customLevel.bosses)
        if boss1 in customLevel.bosses and boss1.active:
            boss1Attack(app)
            drawBoss1(app)
            if app.counter == 179:
                boss1.teleport(boss1.projectX, boss1.projectY)
            elif 100 < app.counter < 180:
                projectBossNextSpot(app, boss1.projectX, boss1.projectY)
        if boss2 in customLevel.bosses and (boss2.active or boss3.active):
            if boss2.attack1Ready and 0 < app.counter < 60:
                drawCircle(boss2.projectX, 100, boss2.radius, fill = None, border = 'black')
                drawCircle(boss3.projectX, 100, boss3.radius, fill = None, border = 'black')
            level2Attack(app)
            drawBoss2(app)
            drawBoss3(app)


    if app.weaponSelectionScreen:
        drawWeaponSelectionScreen(app)

    
    if app.armorSelectionScreen:
        drawArmorSelectionScreen(app)
   
   
    if app.customLevelEditor:
        drawLevelEditor(app)
        if customLevel.makingPlatform:
            drawRect(*customLevel.platformOutlinePosition, fill = None, border='blue', dashes=True)


    if app.deathScreen:
        drawDeathScreen(app)
    if app.victoryScreen:
        drawVictoryScreen(app)

def onStep(app):
    if boss1.active:
        if app.counter == -1:
            boss1.attack2Positions = [800,400,[]]
        
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
                dx = -8 if boss1.position[0] > player.position[0] else 8
                boss1.attack2Positions[2].append([*boss1.position,*player.position,0,dx])
        if boss1.attack3Ready:
            if app.counter % 5 == 0:
                dx = -8 if boss1.position[0] > player.position[0] else 8
                boss1.attack2Positions[2].append([*boss1.position,*player.position,0,dx])
    if boss2.active or boss3.active:
        if app.counter == -1:
            boss2.attack2Positions=[800,400,[]]
            boss3.attack2Positions=[800,400,[]]
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
                
    if app.level3Loaded:
        scroll(app)
        if app.counter % 60 == 0 and app.counter != 0:
            addPlatform(app)
        if player.position[1] > 800 and app.counter %5==0:
            player.removeHealth(1)
            
        
    
    if app.customLevel:
        if player.health <= 0:
            app.customLevel = False
            app.deathScreen = True
        count = 0
        for boss in customLevel.bosses:
            if boss.health > 0:
                count += 1
            else:
                boss.active = False
        if count == 0:
            app.customLevel = False
            app.victoryScreen = True
    if player.jumping:
        player.move(app, 0, -19)
    if anyLevelLoaded(app):
        if app.counter % 2 == 0 and player.equippedWeapon == weapon3:
            app.typhoonAnimationCounter = (app.typhoonAnimationCounter + 1) % 5
        if app.counter % 10 == 0 and boss1.active:
            app.boss1AnimationCounter = (app.boss1AnimationCounter +1) % 2
        if (boss2.attack2Ready or boss2.attack3Ready or boss3.attack3Ready) and app.counter % 5 == 0:
            app.boss2AnimationCounter = (app.boss2AnimationCounter + 1) % 4
            app.boss3AnimationCounter = (app.boss3AnimationCounter + 1) % 4
        if player.jumping and app.counter % 7 ==0 :
            app.playerAnimationCounter = (app.playerAnimationCounter + 1) % 3
        player.move(app, 0, player.gravity)
        app.counter += 1
        if app.counter == 180:
            app.counter = 0

def scroll(app):
    for i in range(3,len(level3.platforms)):
        level3.platforms[i][0]-=10
    for platform in level3.platforms:
        if platform[0] + platform[2] <= 0:
            level3.platforms.pop(level3.platforms.index(platform))
        
def addPlatform(app):
    width=random.randint(200,300)
    top=random.randint(100,700)
    level3.platforms += [[1600,top,width,20]]

def onKeyPress(app, key):
    pass

def onKeyRelease(app, key):
    if key == 'w':
        player.jumping = False

def onKeyHold(app, keys):
    if anyLevelLoaded(app):
        if 'd' in keys and 'a' not in keys:
            player.facingLeft = False
            player.move(app, player.speed, 0)
        if 'a' in keys and 'd' not in keys:
            player.facingLeft = True
            player.move(app, -player.speed, 0)
        if 'w' in keys:
            player.jumping = True

##### ALL LEVEL 1 STUFF
#####

def drawLevel1(app):
    drawPlatform(app)
    drawPlayer(app)
    drawBoss1(app)

def drawPlatform(app):
    if app.level1Loaded:
        if boss1.attack1Ready:
            drawRect(0, 0, app.width, app.height, fill=gradient('blue', 'lightblue', 'white', start='bottom'))
        elif boss1.attack2Ready or boss1.attack3Ready:
            drawRect(0, 0, app.width, app.height, fill=gradient('red', 'brown', 'black', start='bottom'))
        for platform in level1.platforms[:4]:
            drawRect(*platform, fill = None, border='black', borderWidth = 5)
            drawRect(platform[0]+2.5, platform[1]+2.5, platform[2]-5, platform[3]-5, fill='gray')
        for platform in level1.platforms[4:]:
            drawRect(*platform, fill = None, border='black', borderWidth = 5)
            drawRect(platform[0]+2.5, platform[1]+2.5, platform[2]-5, platform[3]-5, fill='gray')
            drawLine(platform[0]+2, platform[1]+2, platform[0] + platform[2]/2, platform[1] + platform[3]-2)
            drawLine(platform[0] + platform[2]/2, platform[1] + platform[3]-2, 
                     platform[0] + platform[2]-2, platform[1]+2)
    elif app.level2Loaded:
        if boss2.attack1Ready and boss3.attack1Ready:
            drawRect(0, 0, app.width, app.height, fill=gradient('lightgreen', 'lightblue', 'white', start='left'))
        elif boss2.attack2Ready:
            drawRect(0, 0, app.width, app.height, fill=gradient('orange', 'white', 'gray', start='left'))
        elif boss2.attack3Ready or boss3.attack3Ready:
            drawRect(0, 0, app.width, app.height, fill=gradient('red', 'black', 'red', start='left'))

        for platform in level2.platforms:
            drawRect(*platform, fill = None, border = 'black', borderWidth = 5)
            drawRect(platform[0] + 2.5, platform[1] + 2.5, platform[2]-5, platform[3]-5, fill = 'hotpink')
    elif app.level3Loaded:
        for platform in level3.platforms:
            drawRect(*platform,fill='blue')

def drawBoss1(app):
    if boss1.health > 0:
        drawRect(30, 30, 504, 10, fill = None, borderWidth = 2, border = 'black')
        drawRect(32, 32, boss1.health, 6, fill = 'red')
    dx, dy = (player.position[0] - boss1.position[0])/70, (player.position[1] - boss1.position[1])/70
    if dx != 0:
        angle = 50 * math.atan(dy/dx)
        if boss1.attack1Ready and dx > 0:
            drawImage(app.boss1Animation[0], *boss1.position, width=200, height=200, 
                      align='center', rotateAngle = angle)
        elif boss1.attack1Ready and dx <0:
            drawImage(app.boss1AnimationMirror[1], *boss1.position, width=200, 
                      height=200, align='center', rotateAngle = angle)
        elif boss1.attack2Ready or boss1.attack3Ready:
            if dx > 0:
                drawImage(app.boss1Animation[app.boss1AnimationCounter], *boss1.position,
                           width=200, height=200, align='center', rotateAngle = angle)
            elif dx < 0:
                drawImage(app.boss1AnimationMirror[app.boss1AnimationCounter], *boss1.position, 
                          width=200, height=200, align='center', rotateAngle = angle)

def projectBossNextSpot(app, newX, newY):
    drawImage(app.boss1Animation[app.boss1AnimationCounter], newX-20, newY+10, width=200, 
              height=200, align='center', opacity = 30)

def boss1Attack(app):
    if boss1.health > 300:
        boss1.attack2Ready = False
        boss1Attack1(app)
    elif boss1.health > 100:
        boss1.attack1Ready = False
        boss1.attack2Ready = True
        boss1Attack2(app)
    else:
        boss1.attack2Ready = False
        boss1.attack3Ready = True
        boss1Attack3(app)

def boss1Attack1(app):
    if boss1.attack1Ready and lineOfSightCheck(app, *boss1.position, *player.position, 35):
        drawPolygon(*boss1.position, player.position[0], player.position[1] - 10, 
                    player.position[0], player.position[1] + 10)
        drawPolygon(*boss1.position, player.position[0], player.position[1] -5, 
                    player.position[0], player.position[1] + 5, fill='red')
        player.removeHealth(0.025)    

def boss1Attack2(app):
    print(boss1.attack2Positions)
    for elem in boss1.attack2Positions[2]:
        drawCircle(elem[0], elem[1],10,fill='gray',border='black')
        dx = elem[5]
        m = max(elem[3],elem[1])
        s = min(elem[3],elem[1])
        if elem[3] < elem[1] -10 and elem[4] == 0:
            dy = (s-m)/30
        else:
            elem[4]=1
            dy=(m-s)/30
        boss1.shootProjectile(app, boss1.attack2Positions[2].index(elem), dx, dy) 

def boss1Attack3(app):
    boss1Attack2(app)


##### ALL LEVEL 2 STUFF
#####
def drawLevel2(app):
    drawPlatform(app)
    drawBoss2(app)
    drawBoss3(app)
    drawPlayer(app)

def drawBoss2(app):
    if boss2.attack1Ready: 
        drawImage(app.boss2Phase1, boss2.position[0], boss2.position[1], 
                  width=300, height=300, align='center')
    elif boss2.attack2Ready or boss2.attack3Ready:
        drawImage(app.boss2Animation[app.boss2AnimationCounter], *boss2.position, 
                  width=300, height=300, align='center')
    if boss2.health > 0:
        drawRect(30, 30, 1004, 15, fill = None, borderWidth = 2, border = 'black')
        drawRect(32, 32, boss2.health, 11, fill = 'red')
        drawLabel('Boss 2 Health', 1060, 35, size=20, align='left')


def drawBoss3(app):
    if boss3.attack1Ready: 
        drawImage(app.boss3Phase1, boss3.position[0], boss3.position[1], 
                  width=300, height=300, align='center')
    elif boss3.attack2Ready or boss3.attack3Ready:
        drawImage(app.boss3Animation[app.boss3AnimationCounter], *boss3.position, 
                  width=300, height=300, align='center')
    if boss3.health > 0:
        drawRect(30, 60, 1004, 15, fill = None, borderWidth = 2, border = 'black')
        drawRect(32, 62, boss3.health, 11, fill = 'red')
        drawLabel('Boss 3 Health', 1060, 65, size =20, align='left')


def level2Attack(app):
    if boss2.health > 500 and boss3.health > 500:
        boss2.attack1Ready = True
        boss3.attack1Ready = True
        level2Attack1()
        if (boss2.position[0] < player.position[0] < boss3.position[0] and
            boss2.position[1] - 10 < player.position[1] < boss2.position[1] + 10):
            player.removeHealth(boss2.damage//10)
        if boss2.touching() or boss3.touching():
            player.removeHealth(boss2.damage)
    elif (boss2.health <= 500 or boss3.health <= 500) and (boss2.health > 0) and (boss3.health > 0):
        boss2.attack1Ready = False
        boss3.attack1Ready = False
        boss2.attack2Ready = True
        boss3.attack2Ready = True
        if boss2.touching() or boss3.touching():
            player.removeHealth(boss2.damage)
        level2Attack2(app)
    elif boss2.health <= 0 and boss3.health > 0:
        boss2.attack2Ready = False
        boss3.attack2Ready = False
        boss3.attack3Ready = True
        if boss3.touching():
            player.removeHealth(boss3.damage)
        boss3.attack3()
    elif boss2.health >0 and boss3.health <=0:
        boss2.attack2Ready = False
        boss3.attack2Ready = False
        boss2.attack3Ready = True
        if boss2.touching():
            player.removeHealth(boss2.damage)
        boss2.attack3()

def level2Attack1():
    drawLine(*boss2.position, *boss3.position)
    dy = 3
    boss2.bossMove(0, dy)
    boss3.bossMove(0, dy)

def level2Attack2(app):
    dx, dy = (boss2.attack2Positions[0] - boss2.position[0])/70, (boss2.attack2Positions[1] - boss2.position[1])/70
    dx2, dy2 = (boss3.attack2Positions[0] - boss3.position[0])/70, (boss3.attack2Positions[1] - boss3.position[1])/70
    dx, dy = angleMaker(2, dx, dy)
    dx2, dy2 = angleMaker(2, dx2, dy2)
    boss2.bossMove(dx, dy)
    boss3.bossMove(dx2, dy2)
    for elem in boss2.attack2Positions[2]:
        drawCircle(elem[0], elem[1], 10, fill='gray', border='black')
        dx = elem[5]
        m = max(elem[3],elem[1])
        s = min(elem[3],elem[1])
        if elem[3] < elem[1] -10 and elem[4] == 0:
            dy = (s-m)/30
        else:
            elem[4]=1
            dy=(m-s)/30
        boss2.shootProjectilesOutwards(app, boss2.attack2Positions[2].index(elem), dx, dy)    
    for elem in boss3.attack2Positions[2]:
        drawCircle(elem[0], elem[1], 10, fill='gray', border='black')
        dx = elem[5]
        m = max(elem[3],elem[1])
        s = min(elem[3],elem[1])
        if elem[3] < elem[1] -10 and elem[4] == 0:
            dy = (s-m)/30
        else:
            elem[4]=1
            dy=(m-s)/30
        boss3.shootProjectilesOutwards(app, boss3.attack2Positions[2].index(elem), dx, dy)

def drawCustomLevel(app):
    if len(app.colors) >=2:
        drawRect(0, 0, app.width, app.height, fill=gradient(*app.colors, start='left-top'))
    elif len(app.colors) ==1:
        drawRect(0, 0, app.width, app.height, fill=app.colors[0])
    if len(app.platColors) >= 2:
        for platform in customLevel.platforms:
            drawRect(*platform, fill=gradient(*app.platColors, start='left'))
    elif len(app.platColors) == 1:
        for platform in customLevel.platforms:
            drawRect(*platform, fill=app.platColors[0])
    else:
        for platform in customLevel.platforms:
            drawRect(*platform, fill='orange')
    drawPlayer(app)

##### LEVEL 3 STUFF

def drawLevel3(app):
    drawPlatform(app)
    background(app)
    drawBoss4(app)
    drawPlayer(app)

def drawBoss4(app):
    boss4.position = [1600, 800]
    drawRect(1400, 0, 200, 800, fill='pink')
    if boss4.health > 0:
        drawRect(30, 60, 1004, 15, fill = None, borderWidth = 2, border = 'black')
        drawRect(32, 62, boss4.health//3, 11, fill = 'red')
        drawLabel('Boss 4 Health', 1060, 65, size =20, align='left')

def level3Attack(app):
    if boss4.health > 2000:
        boss4.attack1Ready=True
        level3Attack1(app)
    elif 2000 > boss4.health > 1000:
        level3Attack2(app)
    else:
        level3Attack3(app)
        
def background(app):
    colour = random.randint(0,6)
    center = [random.randint(0, 1600), random.randint(0, 800),300,colour] 
    boss4.attack1Positions.append(center)
    for elem in boss4.attack1Positions:
        boss4.randomBG(app, boss4.attack1Positions.index(elem))

def level3Attack1(app):
    pass

def level3Attack2(app):
    pass

def level3Attack3(app):
    pass


##### MISC DRAWINGS & RESETS
#####
def drawPlayer(app):
    if player.jumping:
        if player.facingLeft:
            drawImage(app.playerAnimationMirror[app.playerAnimationCounter], player.position[0], player.position[1] - 10,
                    width = 140, height = 140, align='center')
        else:
            drawImage(app.playerAnimation[app.playerAnimationCounter], player.position[0], player.position[1] - 10,
                    width = 140, height = 140, align='center')
    else:
        if player.facingLeft:
            drawImage(app.playerAnimationMirror[2], player.position[0], player.position[1] - 10,
                    width = 140, height = 140, align='center')
        else:
            drawImage(app.playerAnimation[0], player.position[0], player.position[1] - 10,
                    width = 140, height = 140, align='center')
    if player.equippedWeapon == weapon3 and player.facingLeft:
        drawImage(app.typhoonBook, player.position[0]-20, player.position[1] - 10,
                    width = 60, height = 60, align='center')
    elif player.equippedWeapon == weapon3 and not player.facingLeft:
        drawImage(app.typhoonBook, player.position[0]+20, player.position[1] - 10,
                    width = 60, height = 60, align='center')
    if player.health > 0:
        drawRect(96, 721, player.health+8, 28, fill='gold', border='black')
        drawRect(100, 725, player.health, 20, fill='green')
        drawLabel(f'Player Health:{int(player.health)}', 180, 700, size=20, fill='white')
    if app.level3Loaded and playerBumpedByPlatform(app):
        if player.position[0] > 30:
            player.move(app, -10, 0)
        else:
            player.removeHealth(10)
        
def playerBumpedByPlatform(app):
    for platform in level3.platforms[3:]:
        if (platform[0]-50<player.position[0]<platform[0]) and (platform[1]-50 < player.position[1] < platform[1]+50):
            return True
    return False

    


def drawHomeScreen(app):
    drawRect(0, 0, app.width, app.height, fill=gradient('black', 'black', start='left'))
    drawRect(0, 0, app.width, app.height, fill=gradient('red', 'gray', 'black', start='bottom'), opacity=30)
    drawLabel('BOSS FIGHT 112', app.width/2-5, 97.5, align='center', size = 100, font='sacramento', 
              italic=True,bold=True, fill='white', border='black')
    drawLabel('BOSS FIGHT 112', app.width/2, 100, align='center', size = 100, 
              italic=True,bold=True, fill=gradient('red', 'salmon', 'orange', start='left-top'), border='black')
    for i in range(3):
        drawRect(296, 246 + 200*i, 400, 75, border='black', align='center', 
                 fill='gray')
        drawRect(300, 250 + 200*i, 400, 75, border='black', align='center', 
                 fill=gradient('blue', 'white', start='right'), borderWidth=4)
        drawLabel(f'Click to Play Level {i+1}', 300, 250+200*i, font='cursive'
                  , fill='black', size=30)
    for i in range(2):
        drawRect(1296, 496 + 150*i, 400, 75, border='black', align='center',
                 fill='gray', borderWidth=2)
        drawRect(1300, 500 + 150*i, 400, 75, border='black', align='center', 
                 fill=gradient('blue', 'white', 'blue', start='left'))
        label = 'Click To Create Level' if i == 0 else 'Click To Play Custom Level'
        drawLabel(label,1300, 500 + 150*i, fill='black'
                  , size=30)
        drawRect(696 + 250*i, 296, 200, 200, fill='gray', 
                 border='black', align='center')
        drawRect(700 + 250*i, 300, 200, 200, fill=gradient('blue', 'white', start='right'), 
                 border='black', align='center')
        text = 'Weapon Selection Screen' if i == 0 else 'Armor Selection Screen'
        drawLabel(text, 700 +250*i, 300, size = 15)
    if player.equippedWeapon == weapon2:
        drawImage(app.weapon2BulletImage, app.width/2, 400, width=200, height=200)
    elif player.equippedWeapon == weapon3:
        drawImage(app.typhoonBook, app.width/2, 400, width=200, height=200)
    elif player.equippedWeapon == weapon4:
        drawImage(app.staff, app.width/2, 400, width=200, height=200)
        
    drawImage(app.playerAnimation[0], 800, 600, width=400, height=400, align='center')
    drawImage(app.boss1AnimationMirror[0], 1400, 200, width=250, height=250, align='center', rotateAngle=-20)
    drawImage(app.boss2Phase1, 100, 100, width=300, height=300, align='center', rotateAngle=20)
    drawImage(app.boss3Phase1, 1520, 700, width=250, height=250, align='center', rotateAngle=20)
    
   
def drawDeathScreen(app):
    drawImage(app.deathScreenImage, 0, 0)
    drawRect(1196, 296, 100, 100, fill='white')
    drawRect(1200, 300, 100, 100, fill = 'gray', border='black')
    drawLabel('Return', 1250, 350)

def drawVictoryScreen(app):
    drawImage(app.victoryScreenImage, 0, 0, width=1600)
    drawLabel('Victory!', app.width/2-5, 95, size=100, bold=True, 
              fill='white', border='black')
    drawLabel('Victory!', app.width/2, 100, size=100, bold=True, 
              fill=gradient('blue', 'limeGreen', 'green', start='left-top'), border='black')
    drawRect(app.width/2, 300, 100, 100, align='center', fill='lightgray')
    drawLabel('Return', app.width/2, 300, size=20)

def drawWeaponSelectionScreen(app):
    drawRect(0,0, app.width, app.height, 
             fill=gradient('purple', 'magenta', 'darkblue', start='left-top'))
    drawRect(150, 300, 200, 200, fill='gray', border='black', align='center')
    drawLabel('Return', 150, 300, size=20)
    text1 = 'Lazer Pointer, Click the Click the screen to shoot a laser at that position'
    text2 = 'Basic Bullet Gun, click to shoot a projectile in that direction'
    text3 = 'Razorblade Typhoon, click to shoot tracking projectiles in a volley around you'
    text4 = 'Lightning rod, click to summon projectiles from the air'
    texts = [text1, text2, text3, text4]
    for i in range(4):
        color = gradient('red', 'white', start='right-top') if weapons[i] != player.equippedWeapon else 'green'
        drawRect(350, 50 + 200*i, 300, 100, 
                 fill=color)
        drawLabel(texts[i], 700, 100 + 200*i, size=20 , align='left')
    drawPolygon(350,100,645,55,645,145,fill='black')
    drawImage(app.typhoonBook, 500, 510, width=175, height=175, align='center')
    drawImage(app.weapon2BulletImage, 500, 325, width=175, height=175, align='center')
    drawImage(app.staff, 500, 700, width=200, height=200, rotateAngle=90, align='center')

def drawArmorSelectionScreen(app):
    drawRect(0,0, app.width, app.height, 
             fill=gradient('red', 'pink', 'red', start='left-top'))
    drawRect(150, 300, 200, 200, fill='gray', border='black', align='center')
    drawLabel('Return', 150, 300, size=20)
    text1='Light Armor, some health and movement benefits'
    text2='Medium Armor, increased health benefits but no movement help'
    text3='Heavy Armor, extreme health increase but movement hinderance'
    texts=[text1, text2, text3]
    for i in range(3):
        color = gradient('blue', 'green', start='right-top') if armor[i] != player.speed else 'green'
        drawRect(350, 50 + 200*i, 300, 100, 
                 fill=color, border='black')
        drawLabel(texts[i], 700, 100 + 200*i, size=20 , align='left')

def drawLevelEditor(app):
    fil = 'white' if len(app.colors) >= 2 else 'black'
    if len(app.colors) >= 2:
        drawRect(0, 0, app.width, app.height, fill=gradient(*app.colors, start='left-top'))
    elif len(app.colors) == 1:
        drawRect(0, 0, app.width, app.height, fill = app.colors[0])
    if len(app.platColors) >=2:
        for platform in customLevel.platforms:
            drawRect(*platform, fill = gradient(*app.platColors, start='left'))
    elif len(app.platColors) == 1:
        for platform in customLevel.platforms:
            drawRect(*platform, fill=app.platColors[0])
    else:
        for platform in customLevel.platforms:
            drawRect(*platform, fill='orange')
    colors = ['red', 'yellow', 'green', 'blue', 'purple', 'black', 'white']
    for i in range(7):
        drawRect(50, 200 + 100*i, 50, 50, fill=colors[i], border='black')
        drawRect(150, 200 + 100*i, 50, 50, fill=colors[i], border='black')
    words=['Clear Theme', 'Save']
    for i in range(2):
        drawRect(250, 625+100*i, 75, 75, align='center', fill=None, border=fil)
        drawLabel(words[i], 250, 625+100*i, align='center', fill=fil)
    for i in range(4):
        drawRect(1400, i * 150 + 150, 100, 100, fill=None, border=fil)
        if i < 3:
            drawLabel(f'Enable Boss {i+1}', 1450, i*150+200, align='center', fill=fil)
        elif i == 3:
            drawLabel('Clear All', 1450, i*150+200, align='center', fill=fil)
    drawLabel('CUSTOM LEVEL! CLICK TO MAKE PLATFORMS AND CHOOSE BOSSES', 798, 88, 
              align='center', size = 40, bold=True, italic=True, fill='gray', border='black')
    drawLabel('CUSTOM LEVEL! CLICK TO MAKE PLATFORMS AND CHOOSE BOSSES', 800, 90, 
              align='center', size = 40, bold=True, italic=True, 
              fill=gradient('red', 'yellow', 'green', 'blue', start='left'))
    drawLabel('Background      Platform', 120, 175, align='center', 
              fill=fil, size=15)


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