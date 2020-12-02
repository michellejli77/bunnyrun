# NEW VERSION
import copy
import random
from cmu_112_graphics import *
# game mode
class crossyMode(Mode):
    def appStarted(mode):
        # character
        mode.oldsprite = mode.loadImage('images/molang.png')
        imageWidth, imageHeight = mode.oldsprite.size
        mode.sprite = mode.scaleImage(mode.oldsprite, .5)
        # mii character info
        mode.miiX = mode.width/2
        mode.miiY = mode.height*8/10
        mode.isJumping = False
        mode.isWalking = False
        mode.miiVel = 7.5
        mode.miiMass = 1
        mode.hasMoved = False
        # platforms
        mode.resetPlatforms()
        mode.nextPlat = None
        # road and cars
        # https://lh3.googleusercontent.com/proxy/kaw3Loo5EIMb9IzvJpvV24P3f_Ozy09cSDCtyqvNRpRDcFrRlmGyx-yZyWPMgjp57TNHMHh8NPE9LoQ7uR2qTthL
        mode.redcar1 = mode.loadImage('images/redcar.png')
        mode.redcar = mode.scaleImage(mode.redcar1, .3/1.5)
        mode.bcar2 = mode.loadImage('images/bcar.png')
        mode.bcar1 = mode.bcar2.transpose(Image.FLIP_LEFT_RIGHT)
        mode.bcar = mode.scaleImage(mode.bcar1, .2/1.5)
        mode.gcar1 = mode.loadImage('images/gcar.png')
        mode.gcar = mode.scaleImage(mode.gcar1, .15/1.5)
        mode.cars = [mode.redcar, mode.bcar, mode.gcar]
        # background pictures
        mode.backgroundPics()
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
        mode.name = None
        mode.highScores = {'Michelle': 100}
    
    def backgroundPics(mode):
        # https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pngitem.com%2Fmiddle%2FhTbmTb_life-clipart-colorful-tree-transparent-background-tree-clipart%2F&psig=AOvVaw13JaeiR3H6uoCgNc0NZDWT&ust=1606890271306000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCNjHjveSrO0CFQAAAAAdAAAAABAa
        mode.tree1 = mode.loadImage('images/tree.png')
        mode.tree = mode.scaleImage(mode.tree1, .1)
    
    def resetPlatforms(mode):
        platOptions = [['grass', []], 'ice', 'sand', ['road', []], ['river', []], 'lava']
        mode.platforms = [['grass', []]] + [['grass', []]] + [['grass', []]] + [None]*8
        mode.chooseTrees()
        index = 3
        while index < len(mode.platforms):
            num = random.randint(0, 5)
            mode.platforms[index] = copy.copy(platOptions[num])
            if index < 10 and mode.platforms[index] == 'ice':
                mode.platforms[index + 1] = 'ice'
                index += 1
            index +=1 
        mode.generateLogs()
        mode.platY = 0
        mode.totalTime = 60
        mode.endTime = None

    def keyPressed(mode, event):
        if event.key == 'Space' or event.key == 'Up':
            mode.hasMoved = True
        if mode.isJumping == False and mode.isWalking == False:
            if event.key == "Space":
                mode.isJumping = True
            elif event.key == "Up":
                mode.isWalking = True
    
    def timerFired(mode):
        if mode.totalTime == 0:
            mode.isFinished = True
            mode.endTime = mode.totalTime
        if mode.isJumping:
            mode.platY += 75.5/8
            mode.generatePlatform()
            mode.jump()
        if mode.isWalking:
            mode.platY += 75.5/8
            mode.generatePlatform()
            mode.walk()
        if mode.hasMoved:
            mode.timerFiredTime -= 1
            if mode.timerFiredTime % 30 == 0:
                mode.totalTime -= 1
        if mode.isFinished:
            mode.name = mode.getUserInput('Enter name to save score: ')
            while (mode.name == ''):
                # name input taken from 
                # http://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#subclassingApp
                mode.message = 'No name entered'
                mode.showMessage('No name entered')
                mode.name = mode.getUserInput('Enter name: ')
            mode.highScores[mode.name] = mode.totalTime
            mode.appStarted()
            mode.app.setActiveMode(mode.app.lbMode)
        # move the river
        mode.moveLog()
        # move the cars
        mode.moveCars()  
    
    def mousePressed(mode, event):
        print(event.x, event.y)
        if (mode.bx1 <= event.x <= mode.bx2 and mode.by1 <= event.y <= mode.by2):
            mode.app.setActiveMode(mode.app.splashMode)
        if (mode.rx1 <= event.x <= mode.rx2 and mode.ry1 <= event.y <= mode.ry2):
            mode.appStarted()
    
    def generatePlatform(mode):
        platOptions = [['grass', []], 'ice', 'sand', ['road', []], ['river', []], 'lava']
        if mode.platY % (mode.height/10) == 0:
            mode.platY = 0
            mode.platforms.pop(0)
            num = random.randint(0, 5)
            if mode.nextPlat != None:
                num = 1
                mode.nextPlat = None
                mode.platforms.append(platOptions[num])
            elif platOptions[num] == 'ice':
                mode.nextPlat = 'ice'
                mode.platforms.append(platOptions[num])
            elif platOptions[num] != 'lava':
                mode.platforms.append(platOptions[num])
            elif platOptions[num] == 'lava' and mode.platforms[-1] != 'lava':
                mode.platforms.append(platOptions[num])
            else:
                mode.platforms.append(platOptions[0])

    # make bunny walk
    def walk(mode):
        if mode.platY % (75.5/2) == 0:
            mode.sprite = mode.sprite.transpose(Image.FLIP_LEFT_RIGHT)
        if mode.platY % 75.5 == 0:
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
        if mode.miiVel == .5:
            mode.sprite = mode.sprite.transpose(Image.FLIP_LEFT_RIGHT)
        if mode.miiVel == -8.5:
            mode.isJumping = False
            mode.miiVel = 7.5
            mode.miiMass = 1
                    
    def chooseTrees(mode):
        for platform in mode.platforms:
            if platform != None and platform[0] == 'grass' and platform[1] == []:
                numTrees = random.randint(1, 5)
                mode.treeLocations = [None]*16
                for tree in range(numTrees):
                    locations = random.randint(0, 5)
                    locations2 = random.randint(10, 15)
                    side = random.randint(0, 1)
                    if side == 0:
                        mode.treeLocations[locations] = True
                    else:
                        mode.treeLocations[locations2] = True
                platform[1] = mode.treeLocations
    
    def drawGrass(mode, canvas, y, platform, index1):
        mode.chooseTrees()
        canvas.create_rectangle(0, y - mode.height/10, mode.width, y, 
                            fill = '#9fe04f', width = 0)
        if mode.platforms[index1 - 1][0] != 'grass':
            canvas.create_rectangle(0, y - 10, mode.width, y, 
                                fill = '#6b5e48', width = 0)
        # draw trees on grass
        for index in range(len(platform[1])):
            if platform[1][index] == True:
                canvas.create_image(mode.width * index / 16.3 + 16.3, y - 60, 
                                    image=ImageTk.PhotoImage(mode.tree)) 
    
    def drawIce(mode, canvas, y, index1):
        canvas.create_rectangle(0, y - mode.height/10, mode.width, y, fill = 'light blue', outline = 'light blue')
        for x1 in range(0, mode.width, 30):
            for y1 in range(int(y - mode.height/10), int(y), 30):
                canvas.create_polygon(x1, y1, x1 + 2, y1, x1 + 20, y1 + 20, x1 + 20, y1 + 18, fill = 'white')
        if mode.platforms[index1 - 1] != 'ice':
            canvas.create_rectangle(0, y - 10, mode.width, y, 
                                fill = '#5bc0eb', width = 0)
    
    def drawSand(mode, canvas, y):
        canvas.create_rectangle(0, y - mode.height/10, mode.width, y, fill = 'tan', outline = 'tan')
    
    def makeCars(mode):
        for platform in mode.platforms:
            if platform != None and platform[0] == 'road' and platform[1] == []:
                platform[1] = [None]*7
                x = -200
                for index in range(len(platform[1])):
                    carDist = random.randint(2, 4)
                    x += carDist * 100
                    carColor = random.randint(0,2)
                    platform[1][index] = [x, mode.cars[carColor]]
    
    def moveCars(mode):
        for platform in mode.platforms:
            if platform[0] == 'road':
                for index in range(len(platform[1])):
                    platform[1][index][0] -= 4
                    if platform[1][index][0] < -50:
                        platform[1].pop(0)
                        carColor = random.randint(0,2)
                        platform[1].append([2200, mode.cars[carColor]]) 
    
    def drawRoad(mode, canvas, y, platform):
        mode.makeCars()
        canvas.create_rectangle(0, y - mode.height/10, mode.width, y, fill = 'gray', outline = 'gray')
        y1 = (y - mode.height/10 + y)/2
        # draw logs in grass
        for car in platform[1]:
            canvas.create_image(car[0], y1 - 20, image=ImageTk.PhotoImage(car[1]))
    
    def generateLogs(mode):
        for platform in mode.platforms:
            if platform != None and platform[0] == 'river' and platform[1] == []:
                platform[1] = [None]*15
                x = -500 
                for index in range(len(platform[1])):
                    logDist = random.randint(3, 5)
                    x += logDist * 100
                    platform[1][index] = [x, x + 200]
    
    def moveLog(mode):
        for platform in mode.platforms:
            if platform[0] == 'river':
                for index in range(len(platform[1])):
                    for x in range(2):
                        platform[1][index][x] += 2
                    if platform[1][index][0] > mode.width:
                        platform[1].pop()
                        platform[1].insert(0, [-500, -300]) 
    
    def drawRiver(mode, canvas, y, platform):
        mode.generateLogs()
        canvas.create_rectangle(0, y - mode.height/10, mode.width, y, fill = '#4bb9de', outline = '#4bb9de')
        y1 = (y - mode.height/10 + y)/2
        # draw logs in grass
        for log in platform[1]:
            x1, x2 = log
            canvas.create_rectangle(x1, y1 - 20, x2, y1 + 20, fill = 'brown', outline = 'brown')  
    
    def drawLava(mode, canvas, y, index):
        canvas.create_rectangle(0, y - mode.height/10, mode.width, y, fill = 'red', outline = 'red')

    def drawPlatforms(mode, canvas):
        y = 0
        index = 0
        for index in range(len(mode.platforms)):
            platform = list(reversed(mode.platforms))[index]
            if platform == 'ice':
                crossyMode.drawIce(mode, canvas, y + mode.platY, len(mode.platforms) - index - 1)
            elif platform == 'sand':
                crossyMode.drawSand(mode, canvas, y + mode.platY)
            elif platform == 'road':
                crossyMode.drawRoad(mode, canvas, y + mode.platY)
            elif platform == 'lava':
                crossyMode.drawLava(mode, canvas, y + mode.platY, index)
            elif platform[0] == 'road':
                crossyMode.drawRoad(mode, canvas, y + mode.platY, platform)
            elif platform[0] == 'river':
                crossyMode.drawRiver(mode, canvas, y + mode.platY, platform)
            elif platform[0] == 'grass':
                crossyMode.drawGrass(mode, canvas, y + mode.platY, platform, len(mode.platforms) - index - 1)
            y += mode.height/10
    
    def drawTimer(mode, canvas):
        tx1, ty1 = mode.width - 200, 20
        tx2, ty2 = mode.width - 20, 80
        canvas.create_rectangle(tx1, ty1, tx2, ty2, fill = 'pink')
        canvas.create_text((tx1 + tx2)/2 + 20, (ty1 + ty2)/2, text = f'{mode.totalTime}',
                                font = 'Arial 30 bold')
        canvas.create_image((tx1 + tx2)/2 - 40, (ty1 + ty2)/2,
                             image=ImageTk.PhotoImage(mode.timerImage1))

    def redrawAll(mode, canvas):
        # platform
        crossyMode.drawPlatforms(mode, canvas)
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