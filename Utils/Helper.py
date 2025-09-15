from enum import Enum

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, 
                             QSizePolicy, QGridLayout)
from PyQt5.QtGui import QFont

class SpacerPos(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4
    CENTER = 5

"""
layout = GridLayoutBuilder().addWidget(QWidget())
                            .addWidget(QSpacerItem())
                            .addWidget(QWidget())
                            .build()
"""
class HLayoutBuilder:
    def __init__(self):
        self.layout = QHBoxLayout()
 
    def addWidget(self, widget, **kwargs):
        for key, value in kwargs.items():
            if key == "color" and isinstance(widget, QLabel):
                widget.setStyleSheet("color: "+value)
            if key == "isBold" and value and isinstance(widget, QLabel):
                font = QFont()
                font.setBold(True)
                widget.setFont(font)
        if isinstance(widget, QWidget):
            self.layout.addWidget(widget)
        if isinstance(widget, QSpacerItem):
            self.layout.addItem(widget)
        return self
 
    def build(self):
        return self.layout

"""
layout = GridLayoutBuilder().addWidget(QLabel(), 0, 0)
                            .addWidget(QLabel(), 0, 0, 1, 2, 300)
                            .build()
"""
class GridLayoutBuilder:
    def __init__(self):
        self.layout = QGridLayout()
 
    def addWidget(self, widget: QWidget, row, col, rowSpan=1, colSpan=1, **kwargs):
        alignment = Qt.Alignment()
        for key, value in kwargs.items():
            if key == "align":
                alignment = value
            if key == "minW":
                minW = value
                widget.setMinimumWidth(minW)
            if key == "isBold" and value and isinstance(widget, QLabel):
                font = QFont()
                font.setBold(True)
                widget.setFont(font)
        self.layout.addWidget(widget, row, col, rowSpan, colSpan, alignment)
        return self
 
    def build(self):
        return self.layout

