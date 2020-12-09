# this class has info on the 'how to play' screen
from cmu_112_graphics import *

class howToPlay(Mode):
    def appStarted(mode):
        # back button
        mode.bx1, mode.by1 = 20, 20
        mode.bx2, mode.by2 = 120, 50
        mode.pic1 = mode.loadImage('images/instructions.png')
        mode.pic = mode.scaleImage(mode.pic1, .8)
    
    def mousePressed(mode, event):
        if (mode.bx1 <= event.x <= mode.bx2 and mode.by1 <= event.y <= mode.by2):
            mode.app.setActiveMode(mode.app.splashMode)
    
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2 + 30, image=ImageTk.PhotoImage(mode.pic))
        # back button
        canvas.create_rectangle(mode.bx1, mode.by1, mode.bx2, mode.by2, fill = 'pink')
        canvas.create_text((mode.bx1 + mode.bx2)/2, (mode.by1 + mode.by2)/2, 
                text = 'back', font = 'System 15 bold')