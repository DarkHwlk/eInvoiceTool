# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QLabel, QFrame
# )
# import sys

# class BorderLayoutDemo(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Layout có border")

#         # Tạo layout bên trong
#         inner_layout = QVBoxLayout()
#         inner_layout.addWidget(QLabel("Nội dung bên trong layout"))

#         # Tạo widget bọc layout
#         container = QFrame()
#         container.setLayout(inner_layout)
#         container.setStyleSheet("""
#             QFrame {
#                 border-bottom: 2px solid #007ACC;
#                 padding: 5px;
#                 background-color: #f0f0f0;
#             }
#         """)

#         # Layout chính
#         main_layout = QVBoxLayout()
#         main_layout.addWidget(container)
#         self.setLayout(main_layout)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     demo = BorderLayoutDemo()
#     demo.show()
#     sys.exit(app.exec_())


from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout, QFrame
import sys

app = QApplication(sys.argv)

main_widget = QWidget()
main_layout = QVBoxLayout(main_widget)
main_layout.addWidget(QLabel("Nội dung bên trong layout"))


# Tạo QFrame làm border dưới
bottom_border = QFrame()
bottom_border.setFrameShape(QFrame.HLine)
bottom_border.setFrameShadow(QFrame.Sunken)
bottom_border.setLineWidth(2)

main_layout.addWidget(bottom_border)

main_widget.show()
sys.exit(app.exec_())
