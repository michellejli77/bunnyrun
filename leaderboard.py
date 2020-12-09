from cmu_112_graphics import *
from crossy import *
from operator import itemgetter

# leaderboard mode
class lbMode(crossyMode):
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
        # access leaderboard file and get scores
        leaderboard = open('leaderboard.txt', 'r')
        scores = leaderboard.readlines()
        mode.scores = []
        for score in scores:
            comma = score.find(',')
            name = score[:comma]
            pscore = score[comma + 1:-2]
            mode.scores.append([name, pscore])
        # from https://stackoverflow.com/questions/18563680/sorting-2d-list-python
        mode.scores = sorted(mode.scores, key=itemgetter(1), reverse=True)
    
    def mousePressed(mode, event):
        if (mode.bx1 <= event.x <= mode.bx2 and mode.by1 <= event.y <= mode.by2):
            mode.app.setActiveMode(mode.app.splashMode)
    
    def redrawAll(mode, canvas):
        # draw background
        canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.bgImage1))
        # back button
        canvas.create_rectangle(mode.bx1, mode.by1, mode.bx2, mode.by2, fill = 'pink')
        canvas.create_text((mode.bx1 + mode.bx2)/2, (mode.by1 + mode.by2)/2, text = 'back', font = 'System 15 bold')
        # scores
        canvas.create_image(mode.width/2, 50, image=ImageTk.PhotoImage(mode.leaderboard))
        y = 100
        totScore = 1
        for score in mode.scores:
            if totScore < 11:
                canvas.create_text(mode.width/2 - 100, y,
                    text = str(totScore) + '.     ' + score[0], font = 'Arial 20 bold', anchor = 'w')
                canvas.create_text(mode.width/2 + 100, y, text = score[1], font = 'Arial 20 bold', anchor = 'e')
                y += 40
                totScore += 1
