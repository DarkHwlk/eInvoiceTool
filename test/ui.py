from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton

app = QApplication([])
window = QWidget()
layout = QGridLayout(window)

# Set horizontal spacing to 30 pixels and vertical spacing to 10 pixels
layout.setHorizontalSpacing(30)
layout.setVerticalSpacing(10)

layout.addWidget(QPushButton("Button 1"), 0, 0)
layout.addWidget(QPushButton("Button 2"), 0, 1)
layout.addWidget(QPushButton("Button 3"), 1, 0)
layout.addWidget(QPushButton("Button 4"), 1, 1)

window.show()
app.exec_()