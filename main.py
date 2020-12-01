from cmu_112_graphics import *
from cmu_112_graphics import *
import time
from game import *
from crossy import *
from leaderboard import *

# splash screen
class splashMode(Mode):
    def appStarted(mode):
        # start button dimensions
        mode.bx1, mode.by1 = mode.width/2 - 500, mode.height*2/3 - 100
        mode.bx2, mode.by2 = mode.width/2 - 100, mode.height*2/3 + 100
        # leaderboard button dimensions
        mode.lx1, mode.ly1 = mode.width/2 + 500, mode.height*2/3 - 100
        mode.lx2, mode.ly2 = mode.width/2 + 100, mode.height*2/3 + 100
        # old version button dimensions
        mode.ox1, mode.oy1 = mode.width/2 - 200, mode.height*2/3 + 120
        mode.ox2, mode.oy2 = mode.width/2 + 200, mode.height*2/3 + 220
        # background
        mode.bgImage = mode.loadImage('images/background.gif')
        bgW, bgH = mode.bgImage.size
        bgScale = mode.height/bgH
        mode.bgImage1 = mode.scaleImage(mode.bgImage, bgScale)

    def redrawAll(mode, canvas):
        # bkg clouds
        canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.bgImage1))
        canvas.create_text(mode.width/2, mode.height/4, text = 'wii fit obstacle course',
                            font = 'System 100 bold')
        # start button
        canvas.create_rectangle(mode.bx1, mode.by1, mode.bx2, mode.by2, fill = 'pink')
        canvas.create_text((mode.bx1 + mode.bx2)/2, (mode.by1 + mode.by2)/2, text = 'start',
                            font = 'System 50 bold')
        # leaderboard button
        canvas.create_rectangle(mode.lx1, mode.ly1, mode.lx2, mode.ly2, fill = 'pink')
        canvas.create_text((mode.lx1 + mode.lx2)/2, (mode.ly1 + mode.ly2)/2, text = 'leaderboard',
                            font = 'System 50 bold')
        # old ver button
        canvas.create_rectangle(mode.ox1, mode.oy1, mode.ox2, mode.oy2, fill = 'pink')
        canvas.create_text((mode.ox1 + mode.ox2)/2, (mode.oy1 + mode.oy2)/2, text = 'old ver',
                            font = 'System 50 bold')
    
    def mousePressed(mode, event):
        if (mode.bx1 <= event.x <= mode.bx2 and mode.by1 <= event.y <= mode.by2):
            mode.app.setActiveMode(mode.app.crossyMode)
        if (mode.lx1 >= event.x >= mode.lx2 and mode.ly1 <= event.y <= mode.ly2):
            mode.app.setActiveMode(mode.app.lbMode)
        if (mode.ox1 >= event.x >= mode.ox2 and mode.oy1 <= event.y <= mode.oy2):
            mode.app.setActiveMode(mode.app.gameMode)

# from http://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#subclassingModalApp
class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashMode = splashMode()
        app.gameMode = gameMode()
        app.crossyMode = crossyMode()
        app.lbMode = lbMode()
        app.setActiveMode(app.splashMode)
        app.timerDelay = 20

MyModalApp(width=1234, height=755)
