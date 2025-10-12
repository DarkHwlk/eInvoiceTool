import sys
from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtCore import pyqtSignal, Qt
from Utils.Helper import singleton
from Utils.MainThreadInvoker  import *

class LoadingDialog(QProgressDialog):
    def __init__(self, parent=None):
        super().__init__("", "Hủy bỏ", 0, 100, parent)
        self.setWindowTitle("Loading...")
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModal) 
        self.setAutoClose(True)
        self.setAutoReset(True)
        self.labelText = ""

    def show(self, labelText="Loading...", maximum=100, minimum=0):
        self.setRange(minimum, maximum)
        self.setValue(minimum)
        self.labelText = labelText
        self.setLabelText(labelText + f" ({self.value()}/{self.maximum()})")
        super().exec()

    def setValue(self, value):
        super().setValue(value)
        self.setLabelText(self.labelText + f" ({self.value()}/{self.maximum()})")
        # if self.value() >= self.maximum():
        #     self.close()
