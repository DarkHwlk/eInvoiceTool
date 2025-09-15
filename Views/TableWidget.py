from PyQt5.QtWidgets import (QTableView, QSizePolicy, QHeaderView)

class TableWidget(QTableView):
    def __init__(self, parent):
        super().__init__(parent)
        self._model = None
        self.verticalHeader().hide()
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.horizontalHeader().setResizeMode(QHeaderView.Stretch)

    def setModel(self, model):
        self._model = model
        super().setModel(self._model)
        self.updateConfigStyle()

    def updateConfigStyle(self):
        self.resizeColumnsToContents()
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.horizontalHeader().setStyleSheet("QHeaderView::section { background-color:lightblue }")
