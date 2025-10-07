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

        # Testing only
        # table_data = [
        #     [1,"Khám Nội tiêu hóa","Lần",1,249400,249400,"KCT",0,249400],
        #     [2,"Khám Nội tiêu hóa","Lần",1,249400,249400,"KCT",0,249400],
        #     [3,"Khám Nội tiêu hóa","Lần",1,249400,249400,"KCT",0,249400]
        # ]
        # self._mainModel.setTableData(table_data)

        # self._mainModel.setGeneralData({'NBan': {'Ten': 'CÔNG TY TNHH BỆNH VIỆN ĐKTN AN SINH - PHÚC TRƯỜNG MINH', 'MST': '0106793535', 'DChi': 'Số 8 đường Châu Văn Liêm, Phường Từ Liêm, Thành phố Hà Nội, Việt Nam'}, 'NMua': {'DChi': '129 Nguyễn Trãi,  Phường Khương Đình, Thành phố Hà Nội', 'HVTNMHang': 'Đặng Khánh Hưng (03820000621)'}, 'TToan': {'LTSuat': {'TSuat': 'KCT', 'ThTien': '407000', 'TThue': '0'}, 'THTTLTSuat': None, 'TgTCThue': '407000', 'TgTThue': '0', 'TTCKTMai': '0', 'TgTTTBSo': '407000', 'TgTTTBChu': 'Bốn trăm lẻ bảy nghìn đồng chẵn./.'}})
        # self._mainModel.setGeneralData("Hung", ["MaCoQuanThue"])
        # self._mainModel.setGeneralData("Hung", ["NBan", "Ten"])

    def initUi(self):
        self.resize(1280, 720)
        self.setWindowIcon(QIcon(APP_ICON_PATH))
        self.setCentralWidget(self._mainWidget)
        self.initMenu()

    def initMenu(self):
        self._menuBar = MenuBar(self)
        self._menuBar.setController(self._mainController)
        self.setMenuBar(self._menuBar)
