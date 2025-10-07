# Selectabke TableView:
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QStyledItemDelegate, QLineEdit
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
 
class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        #Create a QLineEdit but disable editing
        editor = QLineEdit(parent)
        editor.setReadOnly(True)  # Make the QLineEdit read-only
        return editor
 
    def setModelData(self, editor, model, index):
        #Do nothing, preventing data from being written back to the model
        pass
 
class MyTableModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data
 
    def rowCount(self, parent=QModelIndex()):
        return len(self._data)
 
    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0]) if self._data else 0
 
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None
 
    def flags(self, index):
        #Allow selection and enable editing for the delegate to create an editor
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableView Text Selection Example")
 
        data = [
            ["Row 1, Col 1", "Row 1, Col 2", "Row 1, Col 3"],
            ["Row 2, Col 1", "Row 2, Col 2", "Row 2, Col 3"],
            ["Row 3, Col 1", "Row 3, Col 2", "Row 3, Col 3"],
        ]
 
        self.table_view = QTableView()
        self.model = MyTableModel(data)
        self.table_view.setModel(self.model)
 
        #Set the custom delegate for all columns
        self.delegate = ReadOnlyDelegate(self.table_view)
        self.table_view.setItemDelegate(self.delegate)
 
        #Allow single cell selection
        self.table_view.setSelectionBehavior(QTableView.SelectItems)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
 
        self.setCentralWidget(self.table_view)

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
 