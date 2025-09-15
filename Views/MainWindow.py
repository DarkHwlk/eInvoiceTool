import sys
from datetime import datetime

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, 
                             QSizePolicy)

from Models.MainModel import MainModel
from Controllers.MainController import MainController
from Views.MainWidget import MainWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Invoice Tool")
        self.initMVC()
        self.initUi()

    def initMVC(self):
        data = [
            [1,"Khám Nội tiêu hóa","Lần",1,249400,249400,"KCT",0,249400],
            [1,"Khám Nội tiêu hóa","Lần",1,249400,249400,"KCT",0,249400],
            [1,"Khám Nội tiêu hóa","Lần",1,249400,249400,"KCT",0,249400]
        ]
        header = ["STT"," Tên hàng hóa, dịch vụ","Đơn vị tính","Số lượng",
            "Đơn giá","Tiền chưa thuế","% Thuế","Tiền thuế","Thành tiền"]
        self._mainModel = MainModel(data)
        self._mainModel.setHeader(header)
        self._mainWidget = MainWidget(self)
        self._mainController = MainController(self)
        self._mainController.setModel(self._mainModel)
        self._mainController.setView(self._mainWidget)

    def initUi(self):
        self.resize(1280, 720)
        self.setCentralWidget(self._mainWidget)


