# this class/file contains all the informatino for one player bunny run
import time
import copy
import random
from cmu_112_graphics import *
from operator import itemgetter
from twoPlayer import *
import pygame

# game mode
class onePlayer(twoPlayer):
    # https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html
    def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    # You do not need to understand how this function works.
        import decimal
        rounding = decimal.ROUND_HALF_UP
        return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

    # https://www.cs.cmu.edu/~112/notes/notes-graphics.html
    def rgbString(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

    def appStarted(mode):
        pygame.init()
        mode.play()
        # character
        mode.oldsprite = mode.loadImage('images/molang.png')
        imageWidth, imageHeight = mode.oldsprite.size
        mode.sprite = mode.scaleImage(mode.oldsprite, (mode.height/10)/imageWidth*1.3)
        # mii character info
        mode.miiX = mode.width/2
        mode.miiY = mode.height*8/10
        mode.bunnyX = 0
        mode.isJumping = False
        mode.isWalking = False
        mode.isBackward = False
        mode.wentBackward = False
        mode.goRight = False
        mode.goLeft = False
        mode.miiVel = 7.5
        mode.miiMass = 1
        mode.hasMoved = False
        mode.facingRight = False
        mode.jumpsLeft = 3
        mode.onLog = False
        mode.miiSpeed = 75.5/8
        # platforms
        mode.platCoins = []
        mode.resetPlatforms()
        mode.nextPlat = None
        # coins
        # https://i.pinimg.com/600x315/96/b7/55/96b75530dd0e65612e905bf52ef80c9d.jpg
        mode.coin1 = mode.loadImage('images/carrot.png')
        mode.coin = mode.scaleImage(mode.coin1,.3)
        mode.totalCoins = 0
        # road and cars
        # https://lh3.googleusercontent.com/proxy/kaw3Loo5EIMb9IzvJpvV24P3f_Ozy09cSDCtyqvNRpRDcFrRlmGyx-yZyWPMgjp57TNHMHh8NPE9LoQ7uR2qTthL
        mode.redcar1 = mode.loadImage('images/redcar.png')
        mode.redcar = mode.scaleImage(mode.redcar1, .32/1.5)
        mode.bcar2 = mode.loadImage('images/bcar.png')
        mode.bcar1 = mode.bcar2.transpose(Image.FLIP_LEFT_RIGHT)
        mode.bcar = mode.scaleImage(mode.bcar1, .2/1.5)
        mode.gcar1 = mode.loadImage('images/gcar.png')
        mode.gcar = mode.scaleImage(mode.gcar1, .15/1.5)
        mode.cars = [mode.redcar, mode.bcar, mode.gcar]
        mode.carWidth, mode.carHeight = mode.bcar.size
        # background pictures
        mode.backgroundPics()
        # back button
        mode.bx1, mode.by1 = 20, 20
        mode.bx2, mode.by2 = 120, 50
        # restart button
        mode.rx1, mode.ry1 = 140, 20
        mode.rx2, mode.ry2 = 240, 50
        # game position
        mode.isFinished = False
        mode.fellInLava = False
        mode.fellInWater = False
        mode.hitByCar = False
        mode.EfellInWater = False
        mode.EwentOffScreen = False
        mode.EhitByCar = False
        mode.wentOffScreen = False
        mode.miiLost = False
        # scores
        mode.score = 0
        mode.name = None
        mode.highScores = []
        # access leaderboard file and get scores
        leaderboard = open('leaderboard.txt', 'r')
        scores = leaderboard.readlines()
        for score in scores:
            comma = score.find(',')
            name = score[:comma]
            pscore = score[comma + 1:]
            pscore = pscore.strip()
            if pscore != '':
                mode.highScores.append([name, int(pscore)])
        # from https://stackoverflow.com/questions/18563680/sorting-2d-list-python
        mode.highScores.sort(key=itemgetter(1), reverse=True)
        # friction
        mode.frictionCoeff = {'ice': .03, 'sand': .4, 'grass': .35}
        # time
        mode.timerFiredTime = 0
        mode.seconds = 0
    
    # learned how to use from https://stackoverflow.com/questions/38966257/how-to-play-sounds-on-python-with-tkinter/53670523
    def play(mode):
        # https://www.youtube.com/watch?v=4uu5ojNeY-8
        pygame.mixer.music.load("music/cute2.mp3") 
        pygame.mixer.music.play(-1) 
        pygame.mixer.music.set_volume(.5)
    
    # idea from https://stackoverflow.com/questions/42393916/how-can-i-play-multiple-sounds-at-the-same-time-in-pygame
    def bounceNoise(mode):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('music/jump.mp3'))
        pygame.mixer.Channel(1).set_volume(.1)
    
    def backgroundPics(mode):
        # https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pngitem.com%2Fmiddle%2FhTbmTb_life-clipart-colorful-tree-transparent-background-tree-clipart%2F&psig=AOvVaw13JaeiR3H6uoCgNc0NZDWT&ust=1606890271306000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCNjHjveSrO0CFQAAAAAdAAAAABAa
        mode.tree1 = mode.loadImage('images/tree.png')
        mode.tree = mode.scaleImage(mode.tree1, .1)
    
    def resetPlatforms(mode):
        platOptions = [['grass', []], 'ice', 'sand', ['road', []], ['river', []], ['lava', None]]
        mode.platforms =  [['grass', []]] + [['grass', []]] + [['grass', []]] + \
                            [['grass', []]] + [None]*8
        mode.chooseTrees()
        for index in range(len(mode.platforms)):
            coinLocation = random.randint(0, 12)
            mode.platCoins += [coinLocation]
            if index % 2 == 0:
                mode.platCoins[index] = None
        index = 4
        while index < len(mode.platforms):
            num = random.randint(0, 5)
            mode.platforms[index] = copy.copy(platOptions[num])
            if index < 10 and mode.platforms[index] == 'ice':
                mode.platforms[index + 1] = 'ice'
                index += 1
            if mode.platforms[index][0] == 'lava' and mode.platforms[index - 1][0] == 'lava':
                mode.resetPlatforms()
            index += 1 
        mode.generateLogs()
        mode.platY = 0
        mode.totalTime = 60
        mode.endTime = None

    def keyPressed(mode, event):
        if (event.key == 'Space' or event.key == 'Up' or event.key == 'Down'):
            mode.hasMoved = True
        if mode.isJumping == False and mode.isWalking == False:
            if event.key == "Space" and mode.jumpsLeft != 0:
                mode.wentBackward = False
                mode.jumpsLeft -= 1
                mode.isJumping = True
            if event.key == "Up":
                if mode.onLog:
                    mode.onLog = False
                mode.wentBackward = False
                mode.isWalking = True
            if event.key == 'Down':
                if mode.wentBackward == False:
                    if mode.onLog:
                        mode.onLog = False
                    mode.wentBackward = True
                    mode.isBackward = True
            if event.key == 'Right' and not(mode.onLog):
                mode.goRight = True
                if not(mode.facingRight):
                    mode.sprite = mode.sprite.transpose(Image.FLIP_LEFT_RIGHT)
            if event.key == 'Left' and not(mode.onLog):
                mode.goLeft = True
                if mode.facingRight:
                    mode.sprite = mode.sprite.transpose(Image.FLIP_LEFT_RIGHT)
    
    def timerFired(mode):
        mode.timerFiredTime += 1
        if mode.timerFiredTime % 20 == 0:
            mode.seconds += 1
        mode.calculateForce()
        mode.bunnyX = (mode.miiX - mode.width/2) / 75.5
        mode.checkFinish()
        mode.moveOnLog()
        if (mode.fellInLava or mode.fellInWater or mode.hitByCar 
            or mode.wentOffScreen or mode.EfellInWater or mode.EhitByCar
            or mode.EwentOffScreen):
            mode.isFinished = True
        elif mode.isJumping:
            mode.platY += 75.5/8
            mode.generatePlatform()
            mode.jump()
        elif mode.isWalking:
            mode.platY += mode.miiSpeed
            if mode.miiSpeed != 75.5/8:
                if 72 < mode.platY < 75.5:
                    mode.platY = 75.5
                    mode.isWalking = False
            if mode.onLog:
                mode.onLog = False
            mode.generatePlatform()
            mode.walk()
        elif mode.isBackward:
            mode.platY -= mode.miiSpeed
            if mode.miiSpeed != 75.5/8:
                if -75.5 < mode.platY < -72:
                    mode.platY = -75.5
                    mode.isWalking = False
            if mode.onLog:
                mode.onLog = False
            mode.walkBackward()
        if mode.goRight and not(mode.onLog):
            mode.miiX += 75.5/8
            mode.moveRight()
        if mode.goLeft:
            mode.miiX -= 75.5/8
            mode.moveLeft()
        if mode.isFinished:
            mode.name = mode.getUserInput('Enter name to save score: ')
            while (mode.name == ''):
                # name input taken from 
                # http://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#subclassingApp
                mode.message = 'No name entered'
                mode.showMessage('No name entered')
                mode.name = mode.getUserInput('Enter name: ')
            leaderboard = open('leaderboard.txt', 'a')
            if mode.name != None:
                leaderboard.write(f'{mode.name},{mode.score}\n')
            mode.appStarted()
            mode.app.setActiveMode(mode.app.lbMode)
        # move the river
        mode.moveLog()
        # move the cars
        mode.moveCars()  
    
    def mousePressed(mode, event):
        if (mode.bx1 <= event.x <= mode.bx2 and mode.by1 <= event.y <= mode.by2):
            pygame.mixer.music.pause()
            mode.app.setActiveMode(mode.app.splashMode)
        if (mode.rx1 <= event.x <= mode.rx2 and mode.ry1 <= event.y <= mode.ry2):
            mode.appStarted()
    
    def generatePlatform(mode):
        if mode.score % 50 == 0 and mode.score > 0:
            mode.jumpsLeft += 1
        platOptions = [['grass', []], 'ice', 'sand', ['road', []], 
                        ['river', []], ['lava', None]]
        if (mode.platY % (mode.height/10) == 0 or
                 (mode.miiSpeed != 75.5/8 and mode.platY > 72)):
            coinLocation = random.randint(0, 12)
            coinBool = random.randint(0,1)
            if coinBool == 1:
                mode.platCoins += [coinLocation]
            else:
                mode.platCoins += [None]
            mode.score += 1
            mode.platY = 0
            if mode.wentBackward == False:
                mode.platforms.pop(0)
                mode.platCoins.pop(0)
            num = random.randint(0, 5)
            if mode.nextPlat != None:
                num = 1
                mode.nextPlat = None
                mode.platforms.append(platOptions[num])
            elif platOptions[num] == 'ice':
                mode.nextPlat = 'ice'
                mode.platforms.append(platOptions[num])
            elif platOptions[num] == 'sand' or platOptions[num][0] != 'lava':
                mode.platforms.append(platOptions[num])
            elif platOptions[num][0] == 'lava' and mode.platforms[-1][0] != 'lava':
                mode.platforms.append(platOptions[num])
            else:
                mode.platforms.append(platOptions[0])
    
    # find speed which object moves based on platform friction
    def calculateForce(mode):
        # kinetic friction equation:
        # friction force = friction coeff * normal force
        # no force: velocity = 75.5/8 pixels per 1 timer fired
        platform = mode.platforms[3]
        if platform == 'ice' or platform == 'sand' or platform[0] == 'grass':
            if platform[0] == 'grass':
                platform = 'grass'
            gravity = 9.8
            normalForce = abs(mode.miiMass) * 9.8
            kineticFrictionCoeff = mode.frictionCoeff[platform]
            frictionForce = kineticFrictionCoeff * normalForce
            force = abs(mode.miiMass) * 75.5/8/1
            acceleration = (force - frictionForce)/abs(mode.miiMass)
            mode.miiSpeed = acceleration * 1
        else:
            mode.miiSpeed = 75.5/8
    
    # check collect coins
    def checkCoin(mode):
        coins = mode.platCoins[2]
        if coins != None:
            lower = mode.width/2 - (6.5 - coins)*mode.height/10 - mode.height/20 - 10
            upper = mode.width/2 - (6.5 - coins)*mode.height/10 - mode.height/20 + 10
            if (mode.platCoins[2] == (onePlayer.roundHalfUp(mode.bunnyX)) + 7
                or lower <= mode.miiX <= upper):
                mode.totalCoins += 1
                mode.platCoins[2] = None
                if mode.totalCoins % 10 == 0:
                    mode.jumpsLeft += 1

    # check if the player lost
    def checkFinish(mode):
        bunnyX = 7 + mode.bunnyX
        platform = mode.platforms[2]
        if platform == 'ice' or platform == 'sand' or platform == 'grass':
            pass
        elif (platform[0] == 'lava' and mode.isJumping == False 
                and platform[1] != bunnyX and mode.onLog == False):
            mode.fellInLava = True
        elif (platform[0] == 'river' and mode.isJumping == False and mode.onLog == False
            and mode.isWalking == False):
            for log in platform[1]:
                if (log[0] <= mode.miiX <= log[1]):
                    return
            mode.fellInWater = True
        elif platform[0] == 'road' and mode.isJumping == False:
            for car in platform[1]:
                if (car[0] - mode.carWidth/2) <= mode.miiX <= (car[0] + mode.carWidth/2):
                    mode.hitByCar = True
        # check if players went off the screen
        if (mode.miiX < 20) or (mode.miiX > mode.width + 20):
            mode.wentOffScreen = True
                
    # make bunny walk
    def walk(mode):
        if mode.platY % (75.5/2) == 0:
            mode.sprite = mode.sprite.transpose(Image.FLIP_LEFT_RIGHT)
            mode.facingRight = not(mode.facingRight)
        dist = abs((mode.miiX) - mode.width/2) % 75.5
        if dist != 0 and not(mode.onLog):
            if (mode.miiX) - mode.width/2 > 0:
                if dist < 75.5/2:
                    mode.miiX -= dist
                else:
                    mode.miiX += (75.5 - dist)
            else:
                if dist < 75.5/2:
                    mode.miiX += dist
                else:
                    mode.miiX -= (75.5 - dist)
        if mode.platY % 75.5 == 0:
            mode.checkCoin()
            mode.bounceNoise()
            mode.isWalking = False
            if mode.onLog:
                mode.onLog = False
    
    # make bunny walk backward
    def walkBackward(mode):
        if mode.platY % (75.5/2) == 0:
            mode.sprite = mode.sprite.transpose(Image.FLIP_LEFT_RIGHT)
            mode.facingRight = not(mode.facingRight)
        if mode.platY % 75.5 == 0:
            mode.checkCoin()
            mode.bounceNoise()
            mode.isBackward = False
            mode.platY = 0
            mode.platforms.insert(0, ['grass', []])
            mode.platforms.pop()
            mode.platCoins.insert(0, None)
            mode.platCoins.pop()
            
    def moveRight(mode):
        dist = abs((mode.miiX) - mode.width/2) % 75.5
        if  0 < ((mode.miiX) - mode.width/2) < 3.5:
            mode.miiX = mode.width/2
        if 72 < dist < 75.5 and not(mode.onLog):
            if ((mode.miiX) - mode.width/2) > 0:
                mode.miiX += (75.5 - dist)
            else:
                mode.miiX -= (75.5 - dist)  
        if (mode.miiX - mode.width/2) % 75.5 == 0:
            mode.checkCoin()
            mode.bounceNoise()
            mode.facingRight = True
            mode.goRight = False 
    
    def moveLeft(mode):
        dist = abs((mode.miiX) - mode.width/2) % 75.5
        if  -3.5 < ((mode.miiX) - mode.width/2) < 0:
            mode.miiX = mode.width/2
        if 72 < dist < 75.5 and not(mode.onLog):
            if ((mode.miiX) - mode.width/2) > 0:
                mode.miiX += (75.5 - dist)
            else:
                mode.miiX -= (75.5 - dist)      
        if (mode.miiX - mode.width/2) % 75.5 == 0:
            mode.checkCoin()
            mode.bounceNoise()
            mode.facingRight = False
            mode.goLeft = False 

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
            mode.facingRight = not(mode.facingRight)
        if mode.miiVel == -8.5:
            mode.isJumping = False
            mode.miiVel = 7.5
            mode.miiMass = 1
            mode.checkCoin()
            mode.bounceNoise()
            dist = abs((mode.miiX) - mode.width/2) % 75.5
            if dist != 0:
                if (mode.miiX) - mode.width/2 > 0:
                    if dist < 75.5/2:
                        mode.miiX -= dist
                    else:
                        mode.miiX += (75.5 - dist)
                else:
                    if dist < 75.5/2:
                        mode.miiX += dist
                    else:
                        mode.miiX -= (75.5 - dist)
            if mode.onLog:
                mode.onLog = False
    
    # move character if standing on log
    def moveOnLog(mode):
        platform = mode.platforms[2]
        if platform[0] == 'river':
            for log in platform[1]:
                if (log[0] <= mode.miiX <= log[1]):
                    mode.miiX += 2
                    mode.onLog = True
                    
    def chooseTrees(mode):
        for platform in mode.platforms:
            if platform != None and platform[0] == 'grass' and platform[1] == []:
                numTrees = random.randint(1, 5)
                mode.treeLocations = [None]*17
                for tree in range(numTrees):
                    locations = random.randint(0, 5)
                    locations2 = random.randint(10, 16)
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
    
    def drawSand(mode, canvas, y, index1):
        canvas.create_rectangle(0, y - mode.height/10, mode.width, y, fill = 'tan', outline = 'tan')
        if mode.platforms[index1 - 1] != 'sand':
            canvas.create_rectangle(0, y - 10, mode.width, y, fill = '#a89560', width = 0)
    
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
        canvas.create_rectangle(0, y - mode.height/10, mode.width, y - mode.height/10 + 5, 
                                fill = 'black', outline = 'black')
        # draw cars on road
        for car in platform[1]:
            canvas.create_image(car[0], y1 - 20, image=ImageTk.PhotoImage(car[1]))
        canvas.create_rectangle(0, y - 5, mode.width, y, fill = 'black', outline = 'black')
    
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
        canvas.create_rectangle(0, y - mode.height/10, mode.width, y, fill = '#5394e6', outline = '#5394e6')
        y1 = (y - mode.height/10 + y)/2
        # draw logs in grass
        for log in platform[1]:
            x1, x2 = log
            canvas.create_rectangle(x1, y1 - 20, x2, y1 + 20, fill = 'brown', outline = 'brown')  

    def drawLava(mode, canvas, y, platform):
        r = 255
        g = 5
        for block in range(int(y - mode.height/10), int(y), int(mode.height/10/16)):
            color = onePlayer.rgbString(r, g, 0)
            canvas.create_rectangle(0, block, mode.width, block + mode.height/10/16, 
                                    fill = color, outline = color)
            g += 13
        # draw random bridge
        if platform[1] == None:
            platform[1] = random.randint(2, 11)
        bx, by = mode.width/2 - (7 - platform[1])*mode.height/10 - mode.height/20, y - mode.height/10
        bx2, by2 = mode.width/2 - (6 - platform[1])*mode.height/10 - mode.height/20, y
        canvas.create_rectangle(bx, by, bx2, by2, fill = 'brown', width = 0)
        for y in range(int(by), int(by2), 5):
            canvas.create_line(bx, y, bx2, y)
        
    def drawPlatforms(mode, canvas):
        y = 0
        index = 0
        for index in range(len(mode.platforms)):
            platform = list(reversed(mode.platforms))[index]
            if platform == 'ice':
                mode.drawIce(canvas, y + mode.platY, len(mode.platforms) - index - 1)
            elif platform == 'sand':
                mode.drawSand(canvas, y + mode.platY, len(mode.platforms) - index - 1)
            elif platform == 'road':
                mode.drawRoad(canvas, y + mode.platY)
            elif platform[0] == 'lava':
                mode.drawLava(canvas, y + mode.platY, platform)
            elif platform[0] == 'road':
                mode.drawRoad(canvas, y + mode.platY, platform)
            elif platform[0] == 'river':
                mode.drawRiver(canvas, y + mode.platY, platform)
            elif platform[0] == 'grass':
                mode.drawGrass(canvas, y + mode.platY, platform, len(mode.platforms) - index - 1)
            y += mode.height/10
    
    def drawCoins(mode, canvas):
        y = 0
        for index in range(len(mode.platforms)):
            coins = list(reversed(mode.platCoins))
            if coins[index] != None:
                coinX = mode.width/2 - (6.5 - coins[index])*mode.height/10 - mode.height/20
                coinY = (y + y - mode.height/10)/2 - 15
                canvas.create_image(coinX, coinY + mode.platY, image=ImageTk.PhotoImage(mode.coin))
            y += mode.height/10
    
    def drawScore(mode, canvas):
        sx1, sy1 = mode.width - 200, 20
        sx2, sy2 = mode.width - 20, 80
        canvas.create_rectangle(sx1, sy1, sx2, sy2, fill = 'pink')
        canvas.create_text((sx1 + sx2)/2, (sy1 + sy2)/2, text = f'score: {mode.score}',
                                font = 'Arial 20 bold')

    def drawJumpsRemaining(mode, canvas):
        jx1, jy1 = mode.width - 400, 20
        jx2, jy2 = mode.width - 220, 80
        canvas.create_rectangle(jx1, jy1, jx2, jy2, fill = 'pink')
        canvas.create_text((jx1 + jx2)/2, (jy1 + jy2)/2, text = f'jumps left: {mode.jumpsLeft}',
                                font = 'Arial 20 bold')
    
    def drawCoinsRemaining(mode, canvas):
        jx1, jy1 = mode.width - 540, 20
        jx2, jy2 = mode.width - 420, 80
        canvas.create_rectangle(jx1, jy1, jx2, jy2, fill = 'pink')
        canvas.create_text((jx1 + jx2)/2, (jy1 + jy2)/2, text = f'carrots: {mode.totalCoins}',
                                font = 'Arial 20 bold')

    
    def endGame(mode, canvas):
        if mode.isFinished:
            canvas.create_rectangle(mode.width/2 - 400, mode.height/2 - 80, 
                        mode.width/2 + 400, mode.height/2 + 80,
                        fill = '#fcfc9d')
            if mode.fellInLava:
                canvas.create_text(mode.width/2, mode.height/2, text = 'good bunny fell in lava :(',
                        font = 'Arial 30 bold')
            elif mode.fellInWater:
                canvas.create_text(mode.width/2, mode.height/2, text = 'good bunny drowned :(',
                        font = 'Arial 30 bold')
            elif mode.hitByCar:
                canvas.create_text(mode.width/2, mode.height/2, text = 'good bunny got hit by a car :(',
                        font = 'Arial 30 bold')
            elif mode.wentOffScreen:
                canvas.create_text(mode.width/2, mode.height/2, text = 'good bunny disappeared into the void',
                        font = 'Arial 30 bold')

    def redrawAll(mode, canvas):
        # platform 
        mode.drawPlatforms(canvas)
        # draw coins
        mode.drawCoins(canvas)
        # draw character
        canvas.create_image(mode.miiX, mode.miiY, image=ImageTk.PhotoImage(mode.sprite))
        # back button
        canvas.create_rectangle(mode.bx1, mode.by1, mode.bx2, mode.by2, fill = 'pink')
        canvas.create_text((mode.bx1 + mode.bx2)/2, (mode.by1 + mode.by2)/2, 
                text = 'back', font = 'System 15 bold')
        # restart button 
        canvas.create_rectangle(mode.rx1, mode.ry1, mode.rx2, mode.ry2, fill = 'pink')
        canvas.create_text((mode.rx1 + mode.rx2)/2, (mode.ry1 + mode.ry2)/2, 
                text = 'reset', font = 'System 15 bold')
        # draw score
        mode.drawScore(canvas)
        # draw coins remaining
        mode.drawCoinsRemaining(canvas)
        # jumps remaining
        mode.drawJumpsRemaining(canvas)
        # instructions
        if mode.hasMoved == False:
            canvas.create_rectangle(mode.width/2 - 400, mode.height/2 - 80, 
                        mode.width/2 + 400, mode.height/2 + 40,
                        fill = '#fcfc9d')
            canvas.create_text(mode.width/2, mode.height/2 - 40, 
                        text = "- collect carrots to get more jumps! 10 carrots = 1 jump",
                            font = 'Arial 30 bold')
            canvas.create_text(mode.width/2, mode.height/2, 
                        text = "- bunny is now affected by friction of surfaces",
                            font = 'Arial 30 bold')
            # canvas.create_text(mode.width/2, mode.height/2 + 40, 
            #             text = "don't let evil bunny get away!",
            #                 font = 'Arial 30 bold')
        # if bunny loses
        mode.endGame(canvas)