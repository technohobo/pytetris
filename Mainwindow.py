from PyQt5 import QtWidgets, QtCore, QtGui, uic
from Playarea import Playarea
import sys
from PyQt5.QtCore import Qt


class Mainwindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Mainwindow, self).__init__()
        uic.loadUi('pytetrisdesign.ui',self)

        self.setWindowTitle("pytetris")

        self.label = self.findChild(QtWidgets.QLabel, "label")
        
        newaction = self.findChild(QtWidgets.QAction, "actionNew")
        newaction.setShortcut("Ctrl+N")
        newaction.triggered.connect(self.newGame)

        quitaction = self.findChild(QtWidgets.QAction, "actionQuit")
        quitaction.setShortcut("Ctrl+Q")
        quitaction.triggered.connect(self.quitapp)

        self.scorelabel = self.findChild(QtWidgets.QLabel, "scorelabel")
        self.levellabel = self.findChild(QtWidgets.QLabel, "levellabel")

        self.playarea = self.findChild(QtWidgets.QFrame, "playArea")
        self.playarea.pointsgotsignal.connect(self.updateScore)
        self.playarea.advancelevelsignal.connect(self.updateLevel)

        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.playarea.movehorizontal(True)
        elif event.key() == Qt.Key_Left:
            self.playarea.movehorizontal(False)
        elif event.key() == Qt.Key_X:
            self.playarea.rotpiece()
        elif event.key() == Qt.Key_Space:
            self.playarea.isGame = not self.playarea.isGame
        elif event.key() == Qt.Key_Down:
            self.playarea.movedownthread.time = 0.1
    
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Down:
            self.playarea.movedownthread.time = 1.0-self.playarea.level*0.1

    def updateScore(self):
        self.scorelabel.setText(str(self.playarea.score))
    
    def updateLevel(self):
        self.levellabel.setText(str(self.playarea.level))
        
    def newGame(self, action):
        self.playarea.newgame()

    def testmethod(self):
        print("test")
    
    def quitapp(self):
        sys.exit(0)
        
