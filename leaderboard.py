from cmu_112_graphics import *
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
        canvas.create_text(mode.width/2, 20, text = 'LEADERBOARD', font = 'Arial 30 bold')
        y = 60
        for name in mode.highScores:
            canvas.create_text(mode.width/2 - 100, y, text = f'{name}', font = 'Arial 15 bold')
            canvas.create_text(mode.width/2 + 100, y, text = f'{mode.highScores[name]}', font = 'Arial 15 bold')
            y += 40
