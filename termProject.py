from cmu_graphics import *


# git add .
# git commit -m
# git push

def onAppStart(app):
    app.width, app.height = 1800, 900
    app.playerPosition = (None, None)
    app.stepsPerSecond = 60

def redrawAll(app):
    drawRect(50, 50, 50, 50)


def main():
    runApp()
main()