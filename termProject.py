from cmu_graphics import *


# git add .
# git commit -m
# git push

def onAppStart(app):
    app.width, app.height = 1800, 900
    app.playerPosition = [app.width/2, app.height/2]

def redrawAll(app):
    drawRect(*app.playerPosition, 100, 100, fill ='hotpink', align = 'center')

def onStep(app):
    enactGravity(app, app.playerPosition)

def enactGravity(app, position):
    if app.playerPosition[1] + 50 < app.height:
        app.playerPosition[1] += 10




def main():
    runApp()
main()