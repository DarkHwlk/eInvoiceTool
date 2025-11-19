import logging
import json
import re

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel)
from PyQt5.QtGui import QPixmap

from Utils.Helper  import VLayoutBuilder
from Utils.Constant  import *
from Views.BaseViews.SelectableLabel  import SelectableLabel

class DigitalSignatureWidget(QWidget):
    def __init__(self, parent = None, name="", date="", isValid=False):
        super().__init__(parent)
        self._nameLabel = SelectableLabel("", self)
        self._nameLabel.setWordWrap(True)
        self._dateLabel = SelectableLabel("", self)
        self._verifyLabel = QLabel("", self)
        self.setName(name)
        self.setDate(date)
        self.setIsValid(isValid)
        self.initUI()
    
    def setData(self, data: str):
        data = json.loads(data) if data != "" else None
        logging.debug(f"data: {data}")
        if data is None:
            self.setName("")
            self.setDate("")
            self.setIsValid(False)
            return

        name = data["certificate_info"]["subject"]\
            if "certificate_info" in data and "subject" in data["certificate_info"] else ""
        name = self.getNameFromSubject(name)
        self.setName(name)

        date = data["SigningTime"]\
            if "SigningTime" in data and data["SigningTime"] is not None else ""
        self.setDate(date)

        integrity_check = data["integrity_check"]["valid"]\
            if data and "integrity_check" in data and "valid" in data["integrity_check"] else False
        signature_check = data["signature_check"]["valid"]\
            if data and "signature_check" in data and "valid" in data["signature_check"] else False
        isValid = integrity_check and signature_check
        self.setIsValid(isValid)

    def setDate(self, date):
        self._dateLabel.setText(f"Ký ngày: <b>{date}</b>")

    def setName(self, name):
        self._nameLabel.setText(f"Ký bởi: <b>{name}</b>")

    def setIsValid(self, isValid):
        self._isValid = isValid
        if isValid:
            self._bgColor = "#dff0d8"
            self._verifyLabel.setText("SIGNATURE VALID ✅")
            self._verifyLabel.setStyleSheet("color: green;")
        else:
            self._bgColor = "#f8a5c2"
            self._verifyLabel.setText("SIGNATURE INVALID ❌")
            self._verifyLabel.setStyleSheet("color: red;")
        if self._nameLabel.text() == "Ký bởi: <b></b>":
            self._bgColor = "#ffffff"
            self._verifyLabel.setText("")
        self.setStyleSheet(
            f"""
            background-color: {self._bgColor};
            """)
    
    def initUI(self):
        layoutBuilder = VLayoutBuilder()
        layoutBuilder.addWidget(self._nameLabel)
        layoutBuilder.addWidget(self._dateLabel)
        layoutBuilder.addWidget(self._verifyLabel, isBold=True)
        vLayout = layoutBuilder.build()
        self.setLayout(vLayout)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def getNameFromSubject(self, input_string):
        cn_match = re.search(r"CN=([^,]+)", input_string)
        if cn_match:
            return cn_match.group(1) 
        return ""

