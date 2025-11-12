import sys
from datetime import datetime
import pandas as pd

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, 
                             QSizePolicy, QDockWidget, QAction)
from PyQt5.QtGui import QIcon

from Models.MainModel import MainModel
from Controllers.MainController import MainController
from Views.MainWidget import MainWidget
from Views.MenuBar import MenuBar
from Utils.Constant  import (APP_ICON_PATH)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Invoice Tool")
        self.initMVC()
        self.initUi()

    def initMVC(self):
        # data = [
        #     [1,"Khám Nội tiêu hóa","Lần",1,249400,249400,"KCT",0,249400],
        #     [1,"Khám Nội tiêu hóa","Lần",1,249400,249400,"KCT",0,249400],
        #     [1,"Khám Nội tiêu hóa","Lần",1,249400,249400,"KCT",0,249400]
        # ]
        # header = ["STT"," Tên hàng hóa, dịch vụ","Đơn vị tính","Số lượng",
        #     "Đơn giá","Tiền chưa thuế","% Thuế","Tiền thuế","Thành tiền"]
        
        self._mainModel = MainModel()
        self._mainWidget = MainWidget(self)
        self._mainController = MainController(self)
        self._mainController.setModel(self._mainModel)
        self._mainController.setView(self._mainWidget)
        self._mainWidget.setController(self._mainController)

    def initUi(self):
        self.resize(1280, 720)
        self.setWindowIcon(QIcon(APP_ICON_PATH))
        self.setCentralWidget(self._mainWidget)
        self.initMenu()

    def initMenu(self):
        self._menuBar = MenuBar(self)
        self._menuBar.setController(self._mainController)
        self.setMenuBar(self._menuBar)
