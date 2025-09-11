from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLabel)

class SelectableLabel(QLabel):
    def __init__(self, text = "", parent = None):
        super().__init__(text, parent)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.setMouseTracking(True)
    
    def mouseMoveEvent(self, event):
            self.setCursor(Qt.IBeamCursor)
            super().mouseMoveEvent(event)
