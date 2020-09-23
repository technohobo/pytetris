from PyQt5 import QtCore
import Playarea
from time import sleep

class MoveDownThread(QtCore.QThread):
    isGame = True
    def __init__(self, Playarea, time=0.2):
        super(MoveDownThread,self).__init__()
        self.playarea = Playarea
        self.time = time

    
    def run(self):
        while True:
            while self.playarea.isGame:
                self.playarea.movepiece()
                sleep(self.time)