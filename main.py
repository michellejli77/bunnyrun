from cmu_112_graphics import *

class splashMode(Mode):
    def appStarted(mode):
        # start button dimensions
        mode.bx1, mode.by1 = mode.width/2 - 200, mode.height*2/3 - 100
        mode.bx2, mode.by2 = mode.width/2 + 200, mode.height*2/3 + 100
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
        canvas.create_rectangle(mode.bx1, mode.by1, mode.bx2, mode.by2, fill = 'pink')
        canvas.create_text((mode.bx1 + mode.bx2)/2, (mode.by1 + mode.by2)/2, text = 'START',
                            font = 'System 100 bold')
    
    def mousePressed(mode, event):
        if (event.x >= mode.bx1 and event.x <= mode.bx2 and event.y >= mode.by1
            and event.y <= mode.by2):
            mode.app.setActiveMode(mode.app.gameMode)

class gameMode(Mode):
    def appStarted(mode):
        # mii character location
        mode.miiX = mode.width/2
        mode.miiY = mode.height*3/4
        # background
        mode.background = 0
        # game settings
        mode.splash = True
        mode.gameStarted = False
        # back button
        mode.bx1, mode.by1 = 20, 20
        mode.bx2, mode.by2 = 120, 50

    def keyPressed(mode, event):
        if mode.gameStarted:
            if event.key == "Space":
                mode.miiY += 50
            elif event.key == "Up":
                mode.background -= 10
    
    def mousePressed(mode, event):
        if (event.x >= mode.bx1 and event.x <= mode.bx2 and event.y >= mode.by1
            and event.y <= mode.by2):
            mode.app.setActiveMode(mode.app.splashMode)

    def redrawAll(mode, canvas):
        # start button
        canvas.create_rectangle(mode.bx1, mode.by1, mode.bx2, mode.by2, fill = 'pink')
        canvas.create_text((mode.bx1 + mode.bx2)/2, (mode.by1 + mode.by2)/2, text = 'BACK')

# from http://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#subclassingModalApp
class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashMode = splashMode()
        app.gameMode = gameMode()
        app.setActiveMode(app.splashMode)
        # app.timerDelay = 50

MyModalApp(width=1234, height=755)
