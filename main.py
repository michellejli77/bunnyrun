from cmu_112_graphics import *
import time

# splash screen
class splashMode(Mode):
    def appStarted(mode):
        # start button dimensions
        mode.bx1, mode.by1 = mode.width/2 - 500, mode.height*2/3 - 100
        mode.bx2, mode.by2 = mode.width/2 - 100, mode.height*2/3 + 100
        # leaderboard button dimensions
        mode.lx1, mode.ly1 = mode.width/2 + 500, mode.height*2/3 - 100
        mode.lx2, mode.ly2 = mode.width/2 + 100, mode.height*2/3 + 100
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
    
    def mousePressed(mode, event):
        if (mode.bx1 <= event.x <= mode.bx2 and mode.by1 <= event.y <= mode.by2):
            mode.app.setActiveMode(mode.app.gameMode)
        if (mode.lx1 >= event.x >= mode.lx2 and mode.ly1 <= event.y <= mode.ly2):
            mode.app.setActiveMode(mode.app.lbMode)

# game mode
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
        mode.isFalling = False
        mode.miiVel = 7.5
        mode.miiMass = 1
        mode.hasMoved = False
        # background
        mode.bgImage = mode.loadImage('images/background.gif')
        bgW, bgH = mode.bgImage.size
        bgScale = mode.height/bgH
        mode.bgImage1 = mode.scaleImage(mode.bgImage, bgScale)
        # platforms
        mode.platforms = [('start', 200, 'black'), ('ground', 400, 'light green'), 
                          ('ground', 50, 'white'), ('ground', 100, 'pink'), 
                          ('gap', 100, None), ('ground', 300, 'light green'), 
                          ('ground', 100, 'pink'), ('gap', 100, None), 
                          ('finish', 200, 'black')
                          ]
        mode.platcoords = [None] * len(mode.platforms)
        mode.platY = 0
        # obstacles
        mode.obstacles = None
        # back button
        mode.bx1, mode.by1 = 20, 20
        mode.bx2, mode.by2 = 120, 50
        # restart button
        mode.rx1, mode.ry1 = 140, 20
        mode.rx2, mode.ry2 = 240, 50
        # timer
        mode.timerImage = mode.loadImage('images/clock.png')
        mode.timerImage1 = mode.scaleImage(mode.timerImage, .1)
        mode.timerFiredTime = 0
        mode.totalTime = 60 # 60 s
        # game position
        mode.isFinished = False
        # scores
        # name input taken from 
        # http://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#subclassingApp
        mode.name = mode.getUserInput('Enter name: ')
        while (mode.name == ''):
            mode.message = 'No name entered'
            mode.showMessage('No name entered')
            mode.name = mode.getUserInput('Enter name: ')
        mode.highScores = dict()

    def keyPressed(mode, event):
        if event.key == 'Space' or event.key == 'Up':
            mode.hasMoved = True
        if mode.isJumping == False:
            if event.key == "Space":
                mode.isJumping = True
            elif event.key == "Up":
                mode.isWalking = True
                mode.platY += 10

    def timerFired(mode):
        if mode.isJumping:
            mode.jump()
            mode.platY += 10
        if mode.isWalking:
            mode.walk() 
        if mode.hasMoved:
            mode.timerFiredTime -= 1
            if mode.timerFiredTime % 20 == 0:
                mode.totalTime -= 1
        if mode.isFinished:
            mode.highScores[mode.name] = mode.totalTime
    
    # check if bunny on ground
    def onGround(mode):
        pass
    
    # make bunny walk
    def walk(mode):
        mode.sprite = mode.sprite.transpose(Image.FLIP_LEFT_RIGHT)
        mode.isWalking = False

    # make bunny jump
    def jump(mode):
        # physics calculation taken from 
        # https://www.geeksforgeeks.org/python-making-an-object-jump-in-pygame/
        F = (1/2) * mode.miiMass * (mode.miiVel**2) 
        mode.miiY -= F 
        mode.miiVel = mode.miiVel - 1 
        if mode.miiVel < 0:
            mode.miiMass = -1
        if mode.miiVel == -.5:
            mode.sprite = mode.sprite.transpose(Image.FLIP_LEFT_RIGHT)
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
    
    # draw obstacle
    def drawObstacle(mode, canvas):
        pass

    # draw platform
    def drawPlatform(mode, canvas):
        curY = 0
        width = 800
        for index in range(len(mode.platforms)):
            platform = mode.platforms[index]
            if platform[0] != 'gap':
                x1, y1 = mode.width/2 - width - mode.platY, mode.height - curY + mode.platY  # bottom left
                x2, y2 = mode.width/2 + width + mode.platY, mode.height - curY + mode.platY  # bottom right
                x3, y3 = mode.width/2 + width/3 + mode.platY, mode.height - platform[1] - curY + mode.platY  # top right
                x4, y4 = mode.width/2 - width/3 - mode.platY, mode.height - platform[1] - curY + mode.platY  # top left
                canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, fill = platform[2])
                mode.platcoords[index] = (x1, y1, x2, y2, x3, y3, x4, y4)
            if platform[0] == 'start':
                canvas.create_text((x1 + x2)/2, (y1 + y3)/2, 
                                    text = 'START', font = 'Arial 30 bold', fill = 'white')
            if platform[0] == 'finish':
                canvas.create_text((x1 + x2)/2, (y1 + y3)/2, 
                                    text = 'FINISH', font = 'Arial 30 bold', fill = 'white')
            curY += platform[1]
            width = width/3
    
    def drawTimer(mode, canvas):
        tx1, ty1 = mode.width - 200, 20
        tx2, ty2 = mode.width - 20, 80
        canvas.create_rectangle(tx1, ty1, tx2, ty2, fill = 'pink')
        canvas.create_text((tx1 + tx2)/2 + 20, (ty1 + ty2)/2, text = f'{mode.totalTime}',
                                font = 'Arial 30 bold')
        canvas.create_image((tx1 + tx2)/2 - 40, (ty1 + ty2)/2,
                             image=ImageTk.PhotoImage(mode.timerImage1))

    def redrawAll(mode, canvas):
        # background
        canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.bgImage1))
        # platform
        mode.drawPlatform(canvas)
        # draw character
        canvas.create_image(mode.miiX, mode.miiY, image=ImageTk.PhotoImage(mode.sprite))
        # back button
        canvas.create_rectangle(mode.bx1, mode.by1, mode.bx2, mode.by2, fill = 'pink')
        canvas.create_text((mode.bx1 + mode.bx2)/2, (mode.by1 + mode.by2)/2, text = 'BACK')
        # restart button 
        canvas.create_rectangle(mode.rx1, mode.ry1, mode.rx2, mode.ry2, fill = 'pink')
        canvas.create_text((mode.rx1 + mode.rx2)/2, (mode.ry1 + mode.ry2)/2, text = 'RESET')
        # draw timer
        mode.drawTimer(canvas)

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

MyModalApp(width=1234, height=755)
