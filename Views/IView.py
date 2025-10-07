import logging

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLabel, QTableView, QLineEdit)

from Views.TableWidget import TableWidget

class IView(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self._generalWidgets = dict()
        self._tableWidget = TableWidget(self)

    def setModel(self, model):
        logging.debug("")
        self._model = model
        self._tableWidget.setModel(self._model)
        self._model.generalDataUpdated.connect(
            self.onGeneralDataUpdated)
    
    def setController(self, controller):
        logging.debug("")
        self._controller = controller
    
    def onGeneralDataUpdated(self, data, key_path):
        if key_path == []:
            return

        current = self._generalWidgets
        for key in key_path[:-1]:
            if key not in current or not isinstance(current[key], dict):
                logging.warn(f"No element have path: {key_path}")
                return 
            current = current[key]
        if key_path[-1] not in current:
            logging.warn(f"No element have path: {key_path}")
            return
        else:
            widget = current[key_path[-1]]
        
            if isinstance(widget, QLabel) or isinstance(widget, QLineEdit):
                widget.setText(data)
