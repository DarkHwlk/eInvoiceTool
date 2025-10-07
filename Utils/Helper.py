import threading

from PyQt5.QtCore import (QSize, Qt, QThreadPool)
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, 
                             QSizePolicy, QGridLayout, QBoxLayout, QFrame)
from PyQt5.QtGui import QFont

from Utils.Worker  import Worker

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

class VLayoutBuilder:
    def __init__(self):
        self.layout = QVBoxLayout()
 
    def addWidget(self, widget, **kwargs):
        alignment = Qt.Alignment()
        for key, value in kwargs.items():
            if key == "color" and isinstance(widget, QLabel):
                widget.setStyleSheet("color: "+value)
            if key == "isBold" and value and isinstance(widget, QLabel):
                font = QFont()
                font.setBold(True)
                widget.setFont(font)
            if key == "align":
                alignment = value
        if isinstance(widget, QWidget):
            self.layout.addWidget(widget, alignment=alignment)
        if isinstance(widget, QSpacerItem):
            self.layout.addItem(widget)
        if isinstance(widget, QBoxLayout):
            self.layout.addLayout(widget)
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
            if key == "color" and isinstance(widget, QLabel):
                widget.setStyleSheet("color: "+value)
        self.layout.addWidget(widget, row, col, rowSpan, colSpan, alignment)
        return self
 
    def build(self):
        return self.layout

""" Spliter """
class Spliter:
    def __new__(self, parent=None, lineWidth=5, vertical=False):
        self.spliter = QFrame(parent)
        if vertical:
            self.spliter.setFrameShape(QFrame.HLine)
        else:
            self.spliter.setFrameShape(QFrame.VLine)
        self.spliter.setFrameShadow(QFrame.Sunken)
        self.spliter.setLineWidth(lineWidth)
        return self.spliter

"""
A decorator that transforms a class into a thread-safe singleton.

@singleton
class CustomSingleton:
"""
def singleton(cls):
    instances = {}
    lock = threading.Lock()
 
    def get_instance(*args, **kwargs):
        with lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

def runThread(func, *args, **kwargs):
    QThreadPool().globalInstance().start(
        Worker(func, *args, **kwargs))

def extractKeyPathsValue(data: dict, parent_keys=None):
    if parent_keys is None:
        parent_keys = []
    result = []
    for key, value in data.items():
        current_path = parent_keys + [key]
        if isinstance(value, dict):
            result.extend(extractKeyPathsValue(value, current_path))
        else:
            result.append((current_path, value))
    return result
