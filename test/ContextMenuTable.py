# Context menu TableView
from PyQt5 import QtWidgets, QtCore
 
class MyTableView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
 
        # Example Model and Data
        self.model = QtCore.QStringListModel()
        self.model.setStringList(['Item 1', 'Item 2', 'Item 3', 'Item 4'])
        self.setModel(self.model)
 
    def show_context_menu(self, pos):
        index = self.indexAt(pos) # Get the index of the item at the clicked position
 
        context_menu = QtWidgets.QMenu(self)
 
        # Add actions to the menu
        action1 = context_menu.addAction("Action 1")
        action2 = context_menu.addAction("Action 2")
        context_menu.addSeparator()
        action_exit = context_menu.addAction("Exit")
 
        # Connect actions to slots
        action1.triggered.connect(lambda: self.handle_action("Action 1", index))
        action2.triggered.connect(lambda: self.handle_action("Action 2", index))
        action_exit.triggered.connect(QtWidgets.QApplication.instance().quit)
 
        # Display the menu at the global cursor position
        context_menu.exec_(self.viewport().mapToGlobal(pos))
 
    def handle_action(self, action_name, index):
        if index.isValid():
            item_text = self.model.data(index, QtCore.Qt.DisplayRole)
            print(f"{action_name} performed on item: {item_text} at row {index.row()}, column {index.column()}")
        else:
            print(f"{action_name} performed on empty space.")

app = QtWidgets.QApplication([])
table_view = MyTableView()
table_view.show()
app.exec_()
 
