from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel)
from PyQt5.QtGui import QPixmap

from Utils.Helper  import VLayoutBuilder
from Utils.Constant  import *

class DigitalSignatureWidget(QWidget):
    def __init__(self, parent = None, name="", date="", isValid=False):
        super().__init__(parent)
        self._nameLabel = QLabel("", self)
        self._nameLabel.setWordWrap(True)
        self._nameLabel.setAlignment(Qt.AlignCenter)
        self._dateLabel = QLabel("", self)
        self.setName(name)
        self.setDate(date)
        self.setIsValid(isValid)
        self.initUI()
    
    def setDate(self, date):
        self._dateLabel.setText(f"Ký ngày: {date}")

    def setName(self, name):
        self._nameLabel.setText(name)

    def setIsValid(self, isValid):
        self._isValid = isValid
        if isValid:
            self._bgColor = "#dff0d8"
        else:
            self._bgColor = "#f8a5c2"
        self.setStyleSheet(
            f"background-color: {self._bgColor};"
            # f"background-image: url({ICON_OK_PATH}); "
            "background-repeat: no-repeat; "
            "background-position: center;")
    
    def initUI(self):
        layoutBuilder = VLayoutBuilder()
        layoutBuilder.addWidget(QLabel("Đã được ký điện tử bởi:", self))
        layoutBuilder.addWidget(self._nameLabel, isBold=True)
        layoutBuilder.addWidget(self._dateLabel)
        vLayout = layoutBuilder.build()
        self.setLayout(vLayout)
        self.setAttribute(Qt.WA_StyledBackground, True)
