import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, 
                             QSizePolicy)

from Views.MainWidget import MainWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Invoice Tool")
        self.initUi()

    def initUi(self):
        self.resize(1280, 720)
        mainWidget = MainWidget(self)
        self.setCentralWidget(mainWidget)


