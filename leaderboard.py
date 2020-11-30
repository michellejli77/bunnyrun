from game import *

# leaderboard mode
class lbMode(gameMode):
    def appStarted(mode):
        super().appStarted()
        # back button
        mode.bx1, mode.by1 = 20, 20
        mode.bx2, mode.by2 = 120, 50
    
    def mousePressed(mode, event):
        print(event.x, event.y)
        if (mode.bx1 <= event.x <= mode.bx2 and mode.by1 <= event.y <= mode.by2):
            mode.app.setActiveMode(mode.app.splashMode)
    
    def redrawAll(mode, canvas):
        # back button
        canvas.create_rectangle(mode.bx1, mode.by1, mode.bx2, mode.by2, fill = 'pink')
        canvas.create_text((mode.bx1 + mode.bx2)/2, (mode.by1 + mode.by2)/2, text = 'BACK')

# from http://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#subclassingModalApp
class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashMode = splashMode()
        app.gameMode = gameMode()
        app.lbMode = lbMode()
        app.setActiveMode(app.splashMode)
        app.timerDelay = 20