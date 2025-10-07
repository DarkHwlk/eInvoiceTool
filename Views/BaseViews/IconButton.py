from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QPushButton)
from PyQt5.QtGui import QIcon

from Utils.Constant  import *

class IconButton(QPushButton):
    def __init__(self, icon = "", text = "", parent = None):
        super().__init__( QIcon(icon), f"  {text}", parent)
        self.setFixedWidth(MAIN_BUTTON_WIDTH)
        self.setStyleSheet("text-align:left;")

    def setText(self, text):
        super().setText(f"  {text}")
