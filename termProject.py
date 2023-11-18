from cmu_graphics import *


# git add .
# git commit -m
# git push
def distance(x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2) ** 0.5
def lineDistance(line1, line2):
    return line2 - line1

def onAppStart(app):
    app.width, app.height = 1800, 900
    app.playerPosition = [app.width/2, app.height/2]
    app.jumping = False
    app.level1Platforms = [[0, 900, 1800, 10],[100, 200, 100, 20]]

def redrawAll(app):
    drawPlatforms(app)
    drawRect(*app.playerPosition, 100, 100, fill ='hotpink', align = 'center')

def drawPlatforms(app):
    for elem in app.level1Platforms:
        drawRect(*elem, fill = 'gray')
def onStep(app):
    enactGravity(app, app.playerPosition)
    if app.jumping:
        app.playerPosition[1] -= 20

def enactGravity(app, position):
    # if app.playerPosition[1] + 50 < app.height:
    #     app.playerPosition[1] += 10
    for platform in app.level1Platforms:
        if lineDistance(app.playerPosition[1] + 50, platform[1]) > 0:
            app.playerPosition[1] += 10

def onKeyHold(app, keys):
    if 'right' in keys:
        movePlayerRight(app)
    if 'left' in keys:
        movePlayerLeft(app)
    if 'space' in keys:
        app.jumping = True

def onKeyPress(app, key):
    if key == 'space':
        playerJump(app)

def onKeyRelease(app, key):
    if key == 'space':
        app.jumping = False

def playerJump(app):
    app.jumping = True

def movePlayerRight(app):
    app.playerPosition[0] += 15

def movePlayerLeft(app):
    app.playerPosition[0] -= 15



def main():
    runApp()
main()