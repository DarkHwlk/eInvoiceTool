import sys
import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from Views.MainWindow import MainWindow

""" Logging config """
log_format = "%(asctime)s | %(levelname)s | %(filename)s::%(funcName)s > %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
