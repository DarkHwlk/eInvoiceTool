from PyQt5.QtCore import QObject, pyqtSignal

from Views.IView import IView

class MainController(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self._model = None
        self._view = None
        self.iview = IView(parent)

    def setModel(self, model):
        print("MainController set model")
        self._model = model
        
    def setView(self, view: IView):
        print("MainController set view")
        self._view = view
        if self._model:
            view.setModel(self._model)

