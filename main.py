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
        if (mode.bx1 <= event.x <= mode.bx2 and mode.by1 <= event.y <= mode.by2):
            mode.app.setActiveMode(mode.app.gameMode)

class gameMode(Mode):
    def appStarted(mode):
        # character
        mode.oldsprite = mode.loadImage('images/molang.png')
        mode.sprite = mode.scaleImage(mode.oldsprite, 1)
        # mii character info
        mode.miiX = mode.width/2
        mode.miiY = mode.height*2/3
        mode.isJumping = False
        mode.isWalking = False
        mode.miiVel = 7.5
        mode.miiMass = 1
        # background
        mode.bgImage = mode.loadImage('images/background.gif')
        bgW, bgH = mode.bgImage.size
        bgScale = mode.height/bgH
        mode.bgImage1 = mode.scaleImage(mode.bgImage, bgScale)
        # platforms
        mode.platforms = [('ground', 400, 'light green'), ('ground', 50, 'white'),('ground', 100, 'pink')]
        mode.platcoords = []
        mode.platY = 0
        # obstacles
        mode.obstacles = None
        # back button
        mode.bx1, mode.by1 = 20, 20
        mode.bx2, mode.by2 = 120, 50
        # restart button
        mode.rx1, mode.ry1 = 140, 20
        mode.rx2, mode.ry2 = 240, 50

    def keyPressed(mode, event):
        if mode.isJumping == False:
            if event.key == "Space":
                mode.isJumping = True
            elif event.key == "Up":
                mode.isWalking = True
                mode.platY += 10

    def timerFired(mode):
        if mode.isJumping:
            mode.jump()
        if mode.isWalking:
            mode.walk()
    
    def walk(mode):
        mode.sprite = mode.sprite.transpose(Image.FLIP_LEFT_RIGHT)
        mode.isWalking = False

    def jump(mode):
        # physics calculation taken from https://www.geeksforgeeks.org/python-making-an-object-jump-in-pygame/
        F = (1/2) * mode.miiMass * (mode.miiVel**2) 
        mode.miiY -= F 
        mode.miiVel = mode.miiVel - 1 
        if mode.miiVel < 0:
            mode.miiMass = -1
        if mode.miiVel == -8.5:
            mode.isJumping = False
            mode.miiVel = 7.5
            mode.miiMass = 1
    
    def mousePressed(mode, event):
        print(event.x, event.y)
        if (mode.bx1 <= event.x <= mode.bx2 and mode.by1 <= event.y <= mode.by2):
            mode.app.setActiveMode(mode.app.splashMode)
        if (mode.rx1 <= event.x <= mode.rx2 and mode.ry1 <= event.y <= mode.ry2):
            mode.appStarted()
    
    def drawPlatform(mode, canvas):
        curY = 0
        width = 800
        for platform in mode.platforms:
            if platform[0] == 'ground':
                x1, y1 = mode.width/2 - width, mode.height - curY + mode.platY  # bottom left
                x2, y2 = mode.width/2 + width, mode.height - curY + mode.platY  # bottom right
                x3, y3 = mode.width/2 + width/3, mode.height - platform[1] - curY + mode.platY  # top right
                x4, y4 = mode.width/2 - width/3, mode.height - platform[1] - curY + mode.platY  # top left
                canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, fill = platform[2])
            curY += platform[1]
            width = width/3

    def redrawAll(mode, canvas):
        # background
        canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.bgImage1))
        # back button
        canvas.create_rectangle(mode.bx1, mode.by1, mode.bx2, mode.by2, fill = 'pink')
        canvas.create_text((mode.bx1 + mode.bx2)/2, (mode.by1 + mode.by2)/2, text = 'BACK')
        # restart button 
        canvas.create_rectangle(mode.rx1, mode.ry1, mode.rx2, mode.ry2, fill = 'pink')
        canvas.create_text((mode.rx1 + mode.rx2)/2, (mode.ry1 + mode.ry2)/2, text = 'RESET')
        # platform
        mode.drawPlatform(canvas)
        # draw character
        canvas.create_image(mode.miiX, mode.miiY, image=ImageTk.PhotoImage(mode.sprite))

# from http://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#subclassingModalApp
class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashMode = splashMode()
        app.gameMode = gameMode()
        app.setActiveMode(app.splashMode)
        app.timerDelay = 50

MyModalApp(width=1234, height=755)
