import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMenuBar, QAction, QFileDialog)
from Utils.DataTypes  import Menu, Action, ActionMessage

class MenuBar(QMenuBar):
    def __init__(self, parent = None):
        super().__init__(parent)
        self._actions = dict()
        self._controller = None
        self.initActions()
    
    def initActions(self):
        self._actions[Menu.FILE]  = self.addMenu("&File")
        self._actions[Menu.FILE_OPEN_XML] = QAction("&Open xml file", self)
        self._actions[Menu.FILE_OPEN_XML].triggered.connect(self.openXmlFileDialog)
        self._actions[Menu.FILE].addAction(self._actions[Menu.FILE_OPEN_XML])

    def setController(self, controller):
        self._controller = controller
    
    def openXmlFileDialog(self):
        fileName, selectedFilter = QFileDialog.getOpenFileName(self, caption='Open File', filter='Xml Files (*.xml)')
        if fileName:
            logging.info(f"MenuBar::openXmlFileDialog file: {fileName}")
            self._controller.triggerAction(
                ActionMessage(
                    Action.OPEN_XML_FILE,
                    {
                        Action.file: fileName
                    }
            ))
