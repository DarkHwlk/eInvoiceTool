import logging

from PyQt5.QtCore import (QObject, pyqtSignal)

from Views.IView import IView
from Utils.DataTypes  import Action, ActionMessage
from Utils.XmlReader import XmlReader
from Utils.Helper import runThread

class MainController(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self._model = None
        self._view = None

    def setModel(self, model):
        logging.debug("")
        self._model = model
        
    def setView(self, view):
        logging.debug("")
        self._view = view
        if self._model:
            view.setModel(self._model)

    def triggerAction(self, data: dict):
        runThread(self.onTriggerAction, data)

    def onTriggerAction(self, data: dict):
        action = data[Action.action]
        message = data[Action.message]
        logging.info(f"Action: {action} | Message: {message}")
        if action == Action.OPEN_XML_FILE:
            self.__openXmlFile(message[Action.file])
        
        elif action == Action.EXPORT_ONE_EXCEL:
            self.__exportExcelFile()
        
        elif action == Action.EXPORT_ALL_EXCEL:
            self.__exportExcelFile(isAll=True)

    def __openXmlFile(self, file):
        logging.info(f"file: {file}")
        self.__readXmlFile(file)
        
    def __exportExcelFile(self, isAll=False):
        logging.info(f"isAll: {isAll}")

    def __readXmlFile(self, file):
        logging.info(f"file: {file}")
        data = XmlReader().readFiles([file], self.__onReadXmlFileFinished)
    
    def __onReadXmlFileFinished(self, data):
        logging.debug(f"data: {data}")
        self._model.setData(data)
