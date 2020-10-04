from PyQt5 import QtWidgets, QtGui, QtCore
from ActivePiece import ActivePiece
from MoveDownThread import MoveDownThread
import random


piecerngtable = {
        0: "T",
        1: "O", 
        2: "I",
        3: "L",
        4: "J",
        5: "Z",
        6: "S" 
    }

class Playarea(QtWidgets.QFrame):

    score = 0
    pointsgotsignal = QtCore.pyqtSignal()
    refreshmapsignal = QtCore.pyqtSignal()
    advancelevelsignal = QtCore.pyqtSignal()
    isGame = False
    lines = 0
    level = 0
    piece = None

    def __init__(self,*args,**kwargs): #
        super(Playarea,self).__init__(*args,**kwargs) #this fucking thing has to be here for some reason 
        
        self.margin = 5

        self.gridx = 10
        self.gridy = 20
        
        self.playistaken = []

        for i in range(self.gridy):
            temp = []
            for j in range(self.gridx):
                temp.append(False)
            self.playistaken.append(temp)
        
        self.movedownthread = MoveDownThread(self)
        self.movedownthread.start()

        self.refreshmapsignal.connect(self.repaint)
    

    def newgame(self, level=0):
        for i in range(self.gridy):
            for j in range(self.gridx):
                self.playistaken[i][j] = False

        self.piece = ActivePiece(piecerngtable[random.randrange(0,6)],self.gridx)
        self.score = 0
        self.level=level

        self.movedownthread.time = 1.0-self.level*0.05

        self.isGame = True

        self.refreshmapsignal.emit()
        self.pointsgotsignal.emit()
        

    def rotpiece(self, isRight=True):
        if self.isGame:
            if self.piece.name == "L" or self.piece.name == "J" or self.piece.name == "T":
                self.rotpieceLJT(isRight)
            elif self.piece.name == "I" or self.piece.name == "Z" or self.piece.name == "S":
                self.rotpieceIZS()

    def rotpieceIZS(self):
        for i in range(4):
            x=self.piece.data[i][0]+self.piece.transforms[i][0]
            y=self.piece.data[i][1]+self.piece.transforms[i][1]
            if x<0 or x>=self.gridx or self.playistaken[y][x] == True:
                return -1

        for i in range(4):
            x=self.piece.data[i][0]+self.piece.transforms[i][0]
            y=self.piece.data[i][1]+self.piece.transforms[i][1]
            self.piece.data[i] = (x,y)

            self.piece.transforms[i][0]*=-1
            self.piece.transforms[i][1]*=-1

        if self.piece.rot == 1:
            self.piece.rot = 0
        else:
            self.piece.rot = 1
        self.refreshmapsignal.emit()


    def rotpieceLJT(self, isRight):

        transformqueue = []

        x=self.piece.data[0][0]+self.piece.firstv[0]
        y=self.piece.data[0][1]+self.piece.firstv[1]
        if x<0 or x>=self.gridx or self.playistaken[y][x] == True:
                return -1
        transformqueue.append((x,y))

        x=self.piece.data[2][0]+self.piece.firstv[0]*-1
        y=self.piece.data[2][1]+self.piece.firstv[1]*-1
        if x<0 or x>=self.gridx or self.playistaken[y][x] == True:
                return -1
        transformqueue.append((0,0))
        transformqueue.append((x,y))

        x=self.piece.data[3][0]+self.piece.lastv[0]
        y=self.piece.data[3][1]+self.piece.lastv[1]
        if x<0 or x>=self.gridx or self.playistaken[y][x] == True:
                return -1
        transformqueue.append((x,y))

        for i in range(4):
            if i != 1:
                self.piece.data[i] = transformqueue[i]
    
        
        if self.piece.rot % 2 == 0:
            self.piece.firstv[0] += self.piece.firststep[0][0]
            self.piece.firstv[1] += self.piece.firststep[0][1]
            self.piece.lastv[0] += self.piece.laststep[0][0]
            self.piece.lastv[1] += self.piece.laststep[0][1]
        else:
            self.piece.firstv[0] += self.piece.firststep[1][0]
            self.piece.firstv[1] += self.piece.firststep[1][1]
            self.piece.lastv[0] += self.piece.laststep[1][0]
            self.piece.lastv[1] += self.piece.laststep[1][1]

        if self.piece.rot == 3:
            self.piece.rot = 0
        else:
            self.piece.rot+=1
        
        if self.piece.rot % 2 == 0:
            for i in range(2):
                for j in range(2):
                    self.piece.firststep[i][j]*=-1
                    self.piece.laststep[i][j]*=-1
                    
        self.refreshmapsignal.emit()
        return 0


    def movehorizontal(self, direction):
        
        if self.isGame:
            isxpos = True
            isxneg = True

            for i in range(len(self.piece.data)):
                x = self.piece.data[i][0]
                y = self.piece.data[i][1]
                if x+1 == self.gridx or self.playistaken[y][x+1]:
                    isxpos = False
                if x-1<0 or self.playistaken[y][x-1]:
                    isxneg = False

            for i in range(len(self.piece.data)):
                nx = self.piece.data[i][0]
                ny = self.piece.data[i][1]
                if(direction == True):
                    if not isxpos:
                        return -1
                    nx+=1
                else:
                    if not isxneg:
                        return -1
                    nx-=1
                
                self.piece.data[i] = (nx, ny)
            self.refreshmapsignal.emit()

    def movepiece(self):

        for i in range(len(self.piece.data)): #kinda fucked up here, indexes have to be swapped (it just works (tm))
            if(self.piece.data[i][1] >= self.gridy-1) or self.playistaken[self.piece.data[i][1]+1][self.piece.data[i][0]]:
                self.destroypiece()
                return -1
                
        for i in range(len(self.piece.data)):
            ny = self.piece.data[i][1]
            nx = self.piece.data[i][0]
            ny+=1
            self.piece.data[i] = (nx,ny)

        self.deleterows()

        self.refreshmapsignal.emit()
    
    def destroypiece(self):
        for i in range(len(self.piece.data)):
            x=self.piece.data[i][0]
            y=self.piece.data[i][1]
            self.playistaken[y][x] = True
        self.piece = ActivePiece(piecerngtable[random.randrange(0,6)], self.gridx)

    def deleterows(self):

        i = len(self.playistaken)-1
        rowcounter = 0

        while i>=0:
            isTaken = True
            for j in range(self.gridx):
                if self.playistaken[i][j] == False:
                    isTaken = False

            if isTaken:
                rowcounter+=1

                for j in range(len(self.playistaken[i])):
                    self.playistaken[i][j] = False
                
                for j in reversed(range(i)):
                    for k in range(self.gridx):
                        self.playistaken[j+1][k] = self.playistaken[j][k]
                        self.playistaken[j][k] = False

                self.lines+=1
      
            i-=1
        
        if self.lines == self.level * 10 + 10:
            self.level+=1
            self.movedownthread.time = 1.0-self.level*0.5
            self.advancelevelsignal.emit()
            
        if rowcounter>0:           
            scorelist = {
                1: 40*(self.level+1),
                2: 100*(self.level+1),
                3: 300*(self.level+1),
                4: 1200*(self.level+1)
            }
            self.score+=scorelist[rowcounter]
            self.pointsgotsignal.emit()
            
                            
    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        
        x=self.margin
        y=self.margin

        size = self.frameSize()
        sizex = size.width()
        sizey = size.height()

        rectx = self.gridx
        recty = self.gridy

        for i in range(recty):
            for j in range(rectx):

                color = QtCore.Qt.blue

                if self.piece:
                    for k in range(len(self.piece.data)):
                        if self.piece.data[k][0] == j and self.piece.data[k][1] == i:
                            color= QtCore.Qt.yellow
                            break
                
                if self.playistaken[i][j] == True:
                    color = QtCore.Qt.red
                
                rect = QtCore.QRect(x, y, (sizex-((rectx+1)*self.margin))/rectx, (sizey-((recty+1)*self.margin))/recty)
                painter.fillRect(rect,color)

                x+=(sizex-self.margin/2)/rectx
            x=self.margin
            y+=self.margin+(sizey-((recty+1)*self.margin))/recty
        
