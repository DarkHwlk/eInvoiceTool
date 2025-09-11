import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt

def main_window():
    # 1. Create a QApplication instance
    app = QApplication(sys.argv)

    # 2. Create a QMainWindow
    window = QMainWindow()
    window.setWindowTitle("My First PyQt5 App")
    window.setGeometry(100, 100, 400, 200) # x, y, width, height

    # 3. Create a QLabel and set it as the central widget
    label = QLabel("Hello, PyQt5!", window)
    label.setAlignment(Qt.AlignCenter) # Center the text
    window.setCentralWidget(label)

    # 4. Show the window
    window.show()

    # 5. Start the application's event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main_window()
