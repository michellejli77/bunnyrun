# this class/file creates the leaderboard
from cmu_112_graphics import *
from twoPlayer import *

# leaderboard mode
class lbMode(twoPlayer):
    def appStarted(mode):
        super().appStarted()
        # background
        # https://s3.envato.com/files/236825710/114.9mb%20pre%20image%20cartoon%20rainbow%20night%20sky1.jpg
        mode.bgImage = mode.loadImage('images/sky.jpg')
        bgW, bgH = mode.bgImage.size
        bgScale = mode.height/bgH
        mode.bgImage1 = mode.scaleImage(mode.bgImage, bgScale)
        # leaderboard pic, made w pic collage
        mode.leaderboard1 = mode.loadImage('images/leader.jpg')
        mode.leaderboard = mode.scaleImage(mode.leaderboard1, .3)
        # back button
        mode.bx1, mode.by1 = 20, 20
        mode.bx2, mode.by2 = 120, 50
    
    def timerFired(mode):
        mode.appStarted()
    
    def mousePressed(mode, event):
        if (mode.bx1 <= event.x <= mode.bx2 and mode.by1 <= event.y <= mode.by2):
            mode.app.setActiveMode(mode.app.splashMode)
            pygame.mixer.music.pause()
    
    def redrawAll(mode, canvas):
        # draw background
        canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.bgImage1))
        # back button
        canvas.create_rectangle(mode.bx1, mode.by1, mode.bx2, mode.by2, fill = 'pink')
        canvas.create_text((mode.bx1 + mode.bx2)/2, (mode.by1 + mode.by2)/2, text = 'back', font = 'System 15 bold')
        # scores
        canvas.create_rectangle(mode.width/2 - 150, 90, mode.width/2 + 150, 120 + 10*40, fill = 'pink')
        canvas.create_image(mode.width/2, 50, image=ImageTk.PhotoImage(mode.leaderboard))
        y = 120
        totScore = 1
        for score in mode.highScores:
            if totScore < 11:
                canvas.create_text(mode.width/2 - 100, y,
                    text = str(totScore) + '.     ' + score[0], font = 'Arial 20 bold', anchor = 'w')
                canvas.create_text(mode.width/2 + 100, y, text = str(score[1]), font = 'Arial 20 bold', anchor = 'e')
                y += 40
                totScore += 1


