import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from Mainwindow import Mainwindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Mainwindow()

    app.exec_()

main()