from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLineEdit)
from PyQt5.QtGui import QFontMetrics

class AdjustableLineEdit(QLineEdit):
    def __init__(self, text = "", parent = None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.adjustWidth()
        self.textChanged.connect(lambda: self.adjustWidth())

    def adjustWidth(self):
        fm = QFontMetrics(self.font())
        text_width = fm.width(self.text())
        self.setFixedWidth(text_width + 10)
