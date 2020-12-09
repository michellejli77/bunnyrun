from cmu_112_graphics import *
import time
import pygame
from twoPlayer import *
from onePlayer import *
from leaderboard import *
from howtoplay import *

# splash screen
class splashMode(Mode):
    def appStarted(mode):
        pygame.init()
        # how-to button dimensions
        mode.hx1, mode.hy1 = mode.width/2 - 500, mode.height*2/3 - 150
        mode.hx2, mode.hy2 = mode.width/2 - 100, mode.height*2/3
        # one player button
        mode.ox1, mode.oy1 = mode.width/2 - 500, mode.height*2/3 + 50
        mode.ox2, mode.oy2 = mode.width/2 - 100, mode.height*2/3 + 200
        # two player button
        mode.bx1, mode.by1 = mode.width/2 + 500, mode.height*2/3 + 50
        mode.bx2, mode.by2 = mode.width/2 + 100, mode.height*2/3 + 200
        # leaderboard button dimensions
        mode.lx1, mode.ly1 = mode.width/2 + 500, mode.height*2/3 - 150
        mode.lx2, mode.ly2 = mode.width/2 + 100, mode.height*2/3 
        # background
        # https://i.pinimg.com/originals/62/b9/38/62b938023bec355c2384a3714bc76e1d.jpg
        mode.bgImage = mode.loadImage('images/background.png')
        bgW, bgH = mode.bgImage.size
        bgScale = mode.height/bgH
        mode.bgImage1 = mode.scaleImage(mode.bgImage, bgScale)
        # buttons (made with canva)
        mode.howto1 = mode.loadImage('images/howto.jpg')
        mode.howto = mode.scaleImage(mode.howto1, .2)
        mode.lb1 = mode.loadImage('images/lb.jpg')
        mode.lb = mode.scaleImage(mode.lb1, .2)
        mode.op1 = mode.loadImage('images/oneplayer.jpg')
        mode.op = mode.scaleImage(mode.op1, .2)
        mode.tp1 = mode.loadImage('images/twoplayer.jpg')
        mode.tp = mode.scaleImage(mode.tp1, .2)

    def redrawAll(mode, canvas):
        # bkg
        canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.bgImage1))
        # two player button
        canvas.create_rectangle(mode.bx1, mode.by1, mode.bx2, mode.by2, fill = 'pink')
        canvas.create_text((mode.bx1 + mode.bx2)/2, (mode.by1 + mode.by2)/2, text = 'two player',
                            font = 'System 50 bold')
        canvas.create_image((mode.bx1 + mode.bx2)/2, (mode.by1 + mode.by2)/2, image=ImageTk.PhotoImage(mode.tp))
        # one player button
        canvas.create_rectangle(mode.ox1, mode.oy1, mode.ox2, mode.oy2, fill = 'pink')
        canvas.create_text((mode.ox1 + mode.ox2)/2, (mode.oy1 + mode.oy2)/2, text = 'one player',
                            font = 'System 50 bold')
        canvas.create_image((mode.ox1 + mode.ox2)/2, (mode.oy1 + mode.oy2)/2, image=ImageTk.PhotoImage(mode.op))
        # how to button
        canvas.create_rectangle(mode.hx1, mode.hy1, mode.hx2, mode.hy2, fill = 'pink')
        canvas.create_text((mode.hx1 + mode.hx2)/2, (mode.hy1 + mode.hy2)/2, text = 'how to play',
                            font = 'System 50 bold')
        canvas.create_image((mode.hx1 + mode.hx2)/2, (mode.hy1 + mode.hy2)/2, image=ImageTk.PhotoImage(mode.howto))
        # leaderboard button
        canvas.create_rectangle(mode.lx1, mode.ly1, mode.lx2, mode.ly2, fill = 'pink')
        canvas.create_text((mode.lx1 + mode.lx2)/2, (mode.ly1 + mode.ly2)/2, text = 'leaderboard',
                            font = 'System 50 bold')
        canvas.create_image((mode.lx1 + mode.lx2)/2, (mode.ly1 + mode.ly2)/2, image=ImageTk.PhotoImage(mode.lb))
    
    def mousePressed(mode, event):
        if (mode.bx2 <= event.x <= mode.bx1 and mode.by1 <= event.y <= mode.by2):
            pygame.mixer.music.unpause()
            mode.app.setActiveMode(mode.app.twoPlayer)
        if (mode.lx1 >= event.x >= mode.lx2 and mode.ly1 <= event.y <= mode.ly2):
            mode.app.setActiveMode(mode.app.lbMode)
        if (mode.ox2 >= event.x >= mode.ox1 and mode.oy1 <= event.y <= mode.oy2):
            pygame.mixer.music.unpause()
            mode.app.setActiveMode(mode.app.onePlayer)
        if (mode.hx2 >= event.x >= mode.hx1 and mode.hy1 <= event.y <= mode.hy2):
            mode.app.setActiveMode(mode.app.howTo)

# learned from http://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#subclassingModalApp
class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashMode = splashMode()
        app.twoPlayer = twoPlayer()
        app.onePlayer = onePlayer()
        app.howTo = howToPlay()
        app.lbMode = lbMode()
        app.setActiveMode(app.splashMode)
        app.timerDelay = 20 

MyModalApp(width=1234, height=755)
 