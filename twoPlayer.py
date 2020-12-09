# this class/file contains all the informatino for two player bunny run
import time
import copy
import random
from cmu_112_graphics import *
from operator import itemgetter
import pygame

# game mode
class twoPlayer(Mode):
    # https://www.cs.cmu.edu/~112/notes/notes-graphics.html
    def rgbString(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

    def appStarted(mode):
        pygame.init()
        mode.play()
        # character
        # https://www.google.com/url?sa=i&url=http%3A%2F%2Frebloggy.com%2Fpost%2Fgif-cute-walk-spin-molang%2F129723665143&psig=AOvVaw2bRtEkaJtpMKZeWF6gVyNL&ust=1607627493768000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCMj3iqDNwe0CFQAAAAAdAAAAABAJ
        mode.oldsprite = mode.loadImage('images/molang.png')
        imageWidth, imageHeight = mode.oldsprite.size
        mode.sprite = mode.scaleImage(mode.oldsprite, (mode.height/10)/imageWidth*1.3)
        # edited using molang.png
        mode.evilBunny1 = mode.loadImage('images/evilBunny.png')
        mode.evilBunny = mode.scaleImage(mode.evilBunny1, (mode.height/10)/imageWidth*1.3)
        # mii character info
        mode.miiX = mode.width/2 + mode.height/10
        mode.miiY = mode.height*8/10
        mode.bunnyX = 1
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
        # evil bunny info
        mode.evilX = mode.width/2 - mode.height/10
        mode.evilY = mode.height*8/10
        mode.EWalking = False
        mode.EBackward = False
        mode.EwentBackward = False
        mode.EgoRight = False
        mode.EgoLeft = False
        mode.EVel = 7.5
        mode.EMass = 1
        mode.EhasMoved = False
        mode.EfacingRight = False
        mode.EonLog = False
        mode.EonRoad = False
        mode.evilAI = False
        mode.moveX = False
        mode.EwentOffScreen = False
        # platforms
        mode.resetPlatforms()
        mode.nextPlat = None
        # road and cars - other cars edited from same source
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
        # evil computer controlled button
        mode.ex1, mode.ey1 = 20, mode.height - 70
        mode.ex2, mode.ey2 = 150, mode.height - 20
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
        # https://www.youtube.com/watch?v=qrgUzN7pE9Y
        pygame.mixer.music.load("music/cute1.mp3") 
        pygame.mixer.music.play(-1) 
        pygame.mixer.music.set_volume(.5)
    
    # idea from https://stackoverflow.com/questions/42393916/how-can-i-play-multiple-sounds-at-the-same-time-in-pygame
    def bounceNoise(mode):
        # https://www.youtube.com/watch?v=jfSbP8MBU5Q
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
        if mode.EWalking == False:
            if event.key == "w" or event.key == "W":
                mode.EwentBackward = False
                if mode.EonLog:
                    mode.EonLog = False
                mode.EWalking = True
            if event.key == "s" or event.key == "S":
                if mode.EwentBackward == 0:
                    if mode.EonLog:
                        mode.EonLog = False
                    mode.EwentBackward = True
                    mode.EBackward = True
            if (event.key == "d" or event.key == "D") and not(mode.EonLog):
                mode.EgoRight = True
                if not(mode.EfacingRight):
                    mode.evilBunny = mode.evilBunny.transpose(Image.FLIP_LEFT_RIGHT)
                    mode.EfacingRight = not(mode.EfacingRight)
            if (event.key == "a" or event.key == "A") and not(mode.EonLog):
                mode.EgoLeft = True
                if mode.EfacingRight:
                    mode.evilBunny = mode.evilBunny.transpose(Image.FLIP_LEFT_RIGHT)
                    mode.EfacingRight = not(mode.EfacingRight)
    
    def timerFired(mode):
        mode.timerFiredTime += 1
        if mode.timerFiredTime % 20 == 0:
            mode.seconds += 1
        mode.evilAlgorithm()
        mode.calculateForce()
        mode.bunnyX = (mode.miiX - mode.width/2) / 75.5
        mode.checkFinish()
        mode.moveOnLog()
        if (mode.fellInLava or mode.fellInWater or mode.hitByCar 
            or mode.wentOffScreen or mode.EfellInWater or mode.EhitByCar
            or mode.EwentOffScreen or mode.miiLost):
            mode.isFinished = True
        elif mode.isJumping:
            mode.platY += 75.5/8
            mode.evilY += 75.5/8 
            mode.generatePlatform()
            mode.jump()
        elif mode.isWalking:
            mode.evilY += 75.5/8
            mode.platY += 75.5/8
            if mode.miiSpeed != 75.5/8:
                if 72 < mode.platY < 75.5:
                    mode.evilY += (75.5 - mode.evilY % 75.5)
                    mode.platY = 75.5
                    mode.isWalking = False
            if mode.onLog:
                mode.onLog = False
            mode.generatePlatform()
            mode.walk()
        elif mode.isBackward:
            mode.evilY -= mode.miiSpeed
            mode.platY -= mode.miiSpeed
            if mode.miiSpeed != 75.5/8:
                if -75.5 < mode.platY < -72:
                    mode.evilY -= (mode.evilY % 75.5)
                    mode.platY = -75.5
                    mode.isWalking = False
            if mode.onLog:
                mode.onLog = False
            mode.walkBackward()
        if mode.EWalking and not(mode.isWalking):
            mode.evilY -= 75.5/8
            if mode.miiSpeed != 75.5/8:
                if 72 < (mode.evilY % 75.5) < 75.5:
                    mode.evilY += (75.5 - mode.evilY % 75.5)
            if mode.EonLog:
                mode.EonLog = False
            mode.Ewalk()
        elif mode.EBackward:
            mode.evilY += 75.5/8
            if mode.EonLog:
                mode.EonLog = False
            mode.EwalkBackward()
        if mode.goRight and not(mode.onLog):
            mode.miiX += 75.5/8
            mode.moveRight()
        if mode.goLeft and not(mode.onLog):
            mode.miiX -= 75.5/8
            mode.moveLeft()
        if mode.EgoRight:
            mode.evilX += 75.5/8
            mode.EmoveRight()
        if mode.EgoLeft:
            mode.evilX -= 75.5/8
            mode.EmoveLeft()
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
        if (mode.ex1 <= event.x <= mode.ex2 and mode.ey1 <= event.y <= mode.ey2):
            mode.evilAI = not(mode.evilAI)
    
    def generatePlatform(mode):
        if mode.score % 50 == 0 and mode.score > 0:
            mode.jumpsLeft += 1
        platOptions = [['grass', []], 'ice', 'sand', ['road', []], 
                        ['river', []], ['lava', None]]
        if (mode.platY % (mode.height/10) == 0 or
                 (mode.miiSpeed != 75.5/8 and mode.platY > 72)):
            mode.score += 1
            mode.platY = 0
            if mode.wentBackward == False:
                mode.platforms.pop(0)
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
        # check for evil bunny
        location = (mode.height*9/10 - mode.evilY)/75.5 + 1
        if location % 1 == 0 and 0 <= location < len(mode.platforms):
            evilPlatform = mode.platforms[int(location)]
            if evilPlatform == 'ice' or evilPlatform == 'sand' or evilPlatform == 'grass':
                pass
            elif evilPlatform[0] == 'river' and mode.EonLog == False and mode.isWalking == False:
                for log in evilPlatform[1]:
                    if (log[0] <= mode.evilX <= log[1]):
                        return
                mode.EfellInWater = True
            elif evilPlatform[0] == 'road':
                for car in evilPlatform[1]:
                    if (car[0] - mode.carWidth/2) <= mode.evilX <= (car[0] + mode.carWidth/2):
                        mode.EhitByCar = True
        # check if players went off the screen
        if (mode.miiX < 20) or (mode.miiX > mode.width + 20):
            mode.wentOffScreen = True
        if (mode.evilX < 20) or (mode.evilX > mode.width + 20):
            mode.EwentOffScreen = True
        if mode.evilY < -20:
            mode.miiLost = True
                
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
            mode.bounceNoise()
            mode.isBackward = False
            mode.platY = 0
            mode.platforms.insert(0, ['grass', []])
            mode.platforms.pop()
            
    def moveRight(mode):
        dist = abs((mode.miiX) - mode.width/2) % 75.5
        if 0 < ((mode.miiX) - mode.width/2) < 3.5:
            mode.miiX = mode.width/2
        if 72 < dist < 75.5:
            if ((mode.miiX) - mode.width/2) > 0:
                mode.miiX += (75.5 - dist)
            else:
                mode.miiX -= (75.5 - dist)  
        if (mode.miiX - mode.width/2) % 75.5 == 0:
            mode.bounceNoise()
            mode.facingRight = True
            mode.goRight = False 
    
    def moveLeft(mode):
        dist = abs((mode.miiX) - mode.width/2) % 75.5
        if  -3.5 < ((mode.miiX) - mode.width/2) < 0:
            mode.miiX = mode.width/2
        if 72 < dist < 75.5:
            if ((mode.miiX) - mode.width/2) > 0:
                mode.miiX += (75.5 - dist)
            else:
                mode.miiX -= (75.5 - dist)      
        if (mode.miiX - mode.width/2) % 75.5 == 0:
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
            mode.bounceNoise()
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
            if mode.onLog:
                mode.onLog = False
    
    def Ewalk(mode):
        if mode.evilY % (75.5/2) == 0:
            mode.evilBunny = mode.evilBunny.transpose(Image.FLIP_LEFT_RIGHT)
            mode.EfacingRight = not(mode.EfacingRight)
        dist = abs((mode.evilX) - mode.width/2) % 75.5
        if (mode.evilX) - mode.width/2 > 0:
                if dist < 75.5/2:
                    mode.evilX -= dist
                else:
                    mode.evilX += (75.5 - dist)
        else:
            if dist < 75.5/2:
                mode.evilX += dist
            else:
                mode.evilX -= (75.5 - dist)
        if mode.evilY % 75.5 == 0:
            mode.bounceNoise()
            mode.EWalking = False
            if mode.EonLog:
                mode.EonLog = False      
    
    # make evil bunny walk backward
    def EwalkBackward(mode):
        if mode.evilY % (75.5/2) == 0:
            mode.evilBunny = mode.evilBunny.transpose(Image.FLIP_LEFT_RIGHT)
            mode.EfacingRight = not(mode.EfacingRight)
        if mode.evilY % 75.5 == 0:
            mode.bounceNoise()
            mode.EBackward = False
            
    def EmoveRight(mode):
        if (mode.evilX - mode.width/2) % 75.5 == 0:
            mode.EgoRight = False 
            mode.bounceNoise()
    
    def EmoveLeft(mode):
        if (mode.evilX - mode.width/2) % 75.5 == 0:
            mode.bounceNoise()
            mode.EgoLeft = False 
    
    # move character if standing on log
    def moveOnLog(mode):
        platform = mode.platforms[2]
        if platform[0] == 'river':
            for log in platform[1]:
                if (log[0] <= mode.miiX <= log[1]):
                    mode.miiX += 2
                    mode.onLog = True
        # check if evil bunny is on a log
        location = (mode.height*9/10 - mode.evilY)/75.5 + 1
        if location % 1 == 0 and 0 <= int(location) < len(mode.platforms):
            evilPlatform = mode.platforms[int(location)]
            if evilPlatform[0] == 'river':
                for log in evilPlatform[1]:
                    if (log[0] <= mode.evilX <= log[1]):
                        mode.EonLog = True
        if mode.EonLog:
            mode.evilX += 2
                    
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
            color = twoPlayer.rgbString(r, g, 0)
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
    
    def drawScore(mode, canvas):
        sx1, sy1 = mode.width - 200, 20
        sx2, sy2 = mode.width - 20, 80
        canvas.create_rectangle(sx1, sy1, sx2, sy2, fill = 'pink')
        canvas.create_text((sx1 + sx2)/2, (sy1 + sy2)/2, text = f'score: {mode.score}',
                                font = 'Arial 20 bold')
    
    def drawEvilButton(mode, canvas):
        ex1, ey1 = mode.ex1, mode.ey1
        ex2, ey2 = mode.ex2, mode.ey2
        canvas.create_rectangle(ex1, ey1, ex2, ey2, fill = 'pink')
        if mode.evilAI:
            canvas.create_text((ex1 + ex2)/2, (ey1 + ey2)/2, text = 'evil AI: ON',
                                font = 'Arial 20 bold')
        else:
            canvas.create_text((ex1 + ex2)/2, (ey1 + ey2)/2, text = 'evil AI: OFF',
                                font = 'Arial 20 bold')

    def drawJumpsRemaining(mode, canvas):
        jx1, jy1 = mode.width - 400, 20
        jx2, jy2 = mode.width - 220, 80
        canvas.create_rectangle(jx1, jy1, jx2, jy2, fill = 'pink')
        canvas.create_text((jx1 + jx2)/2, (jy1 + jy2)/2, text = f'jumps left: {mode.jumpsLeft}',
                                font = 'Arial 20 bold')
    
    def endGame(mode, canvas):
        if mode.isFinished:
            canvas.create_rectangle(mode.width/2 - 400, mode.height/2 - 80, 
                        mode.width/2 + 400, mode.height/2 + 80,
                        fill = '#fcfc9d')
            if mode.fellInLava:
                canvas.create_text(mode.width/2, mode.height/2, text = 'angel bunny fell in lava :(',
                        font = 'Arial 30 bold')
            elif mode.fellInWater:
                canvas.create_text(mode.width/2, mode.height/2, text = 'angel bunny drowned :(',
                        font = 'Arial 30 bold')
            elif mode.hitByCar:
                canvas.create_text(mode.width/2, mode.height/2, text = 'angel bunny got hit by a car :(',
                        font = 'Arial 30 bold')
            elif mode.wentOffScreen:
                canvas.create_text(mode.width/2, mode.height/2, text = 'angel bunny disappeared into the void',
                        font = 'Arial 30 bold')
            elif mode.EfellInWater:
                canvas.create_text(mode.width/2, mode.height/2, text = 'evil bunny drowned :)',
                        font = 'Arial 30 bold')
            elif mode.EhitByCar:
                canvas.create_text(mode.width/2, mode.height/2, text = 'evil bunny got hit by a car :)',
                        font = 'Arial 30 bold')
            elif mode.miiLost:
                canvas.create_text(mode.width/2, mode.height/2, text = 'evil bunny ran away!',
                        font = 'Arial 30 bold')
            elif mode.EwentOffScreen:
                canvas.create_text(mode.width/2, mode.height/2, text = 'evil bunny disappeared into the void',
                        font = 'Arial 30 bold')

    def redrawAll(mode, canvas):
        # platform 
        mode.drawPlatforms(canvas)
        # draw character
        canvas.create_image(mode.miiX, mode.miiY, image=ImageTk.PhotoImage(mode.sprite))
        canvas.create_image(mode.evilX, mode.evilY, image=ImageTk.PhotoImage(mode.evilBunny))
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
        # jumps remaining
        mode.drawJumpsRemaining(canvas)
        # instructions
        if mode.hasMoved == False:
            canvas.create_rectangle(mode.width/2 - 400, mode.height/2 - 80, 
                        mode.width/2 + 400, mode.height/2 + 80,
                        fill = '#fcfc9d')
            canvas.create_text(mode.width/2, mode.height/2 - 40, 
                        text = "- angel bunny can jump, evil bunny cannot",
                            font = 'Arial 30 bold')
            canvas.create_text(mode.width/2, mode.height/2, 
                        text = "- evil bunny can walk through lava, angel bunny cannot",
                            font = 'Arial 30 bold')
            canvas.create_text(mode.width/2, mode.height/2 + 40, 
                        text = "- don't let evil bunny get away!",
                            font = 'Arial 30 bold')
        # if bunny loses
        mode.endGame(canvas)
        # draw AI button
        mode.drawEvilButton(canvas)

    def evilAlgorithm(mode):
        evilPlatform = 'none'
        locExist = False
        mode.nearCar = False
        if mode.EonRoad:
            mode.EWalking = True
            mode.EonRoad = False
        if mode.evilAI:
            location = (mode.height*9/10 - mode.evilY)/75.5 + 1
            if location % 1 == 0 and 0 <= location < len(mode.platforms) - 1:
                evilPlatform = mode.platforms[int(location)]
                nextPlat = mode.platforms[int(location) + 1]
                if evilPlatform[0] != 'river':
                    mode.EonLog = False
                if evilPlatform[0] == 'road':
                    for car in evilPlatform[1]:
                        if (car[0] - mode.carWidth/2 - 120) <= mode.evilX <= (car[0] + mode.carWidth/2):
                            mode.EgoLeft = True
                if ((nextPlat[0] == 'grass' or nextPlat == 'ice' or nextPlat == 'sand'
                    or nextPlat[0] == 'lava')
                    and mode.timerFiredTime % 15 == 0):
                    mode.EwentBackward = False
                    mode.EWalking = True
                elif nextPlat[0] == 'road':
                    for car in nextPlat[1]:
                        if (car[0] - mode.carWidth/2 - 60) <= mode.evilX <= (car[0] + mode.carWidth/2):
                            return
                    mode.EWalking = True
                    if (mode.platforms[int(location) + 2][0] == 'grass' or 
                         mode.platforms[int(location) + 2] == 'ice' or mode.platforms[int(location) + 2] == 'sand'
                         or mode.platforms[int(location) + 2][0] == 'lava'):
                        mode.EonRoad = True
                elif nextPlat[0] == 'river':
                    for log in nextPlat[1]:
                        if (log[0] + 20 <= mode.evilX <= log[1] - 20):
                            mode.EWalking = True
                            return
                    mode.moveX = True
            if (mode.moveX and not(mode.EgoRight) and not(mode.EgoLeft) and 
                mode.timerFiredTime % 30 == 0
                and not(mode.EonLog) and evilPlatform[0] != 'road'):
                if mode.evilX < mode.width * 1/3:
                    mode.EgoRight = True
                elif mode.evilX > mode.width * 2/3:
                    mode.EgoLeft = True
                else:
                    RorL = random.randint(0,1)
                    if RorL == 0:
                        mode.EgoRight = True
                    else:
                        mode.EgoLeft = True
                mode.moveX = False


