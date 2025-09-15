from abc import abstractmethod
from PyQt5.QtCore import QObject

class IView(QObject):
    @abstractmethod
    def setModel(self, model):
        pass
