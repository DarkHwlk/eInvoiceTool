# Copy selected items in TableView to Clipboard
from PyQt5.QtWidgets import QApplication, QTableView, QAbstractItemModel, QItemSelectionModel
from PyQt5.QtCore import Qt, QModelIndex
 
def copy_selected_items(table_view: QTableView):
    """Copies the data of selected cells in a QTableView to the clipboard."""
    model = table_view.model()
    selection_model = table_view.selectionModel()
    selected_indexes = selection_model.selectedIndexes()
 
    if not selected_indexes:
        return
 
    # Determine the bounding box of the selection for structured copying
    min_row = min(index.row() for index in selected_indexes)
    max_row = max(index.row() for index in selected_indexes)
    min_col = min(index.column() for index in selected_indexes)
    max_col = max(index.column() for index in selected_indexes)
 
    clipboard_text = []
    for row in range(min_row, max_row + 1):
        row_data = []
        for col in range(min_col, max_col + 1):
            index = model.index(row, col)
            if index in selected_indexes: # Only include data from truly selected cells
                row_data.append(str(model.data(index, Qt.DisplayRole)))
            else:
                row_data.append("") # Or a placeholder if you want to maintain structure
        clipboard_text.append("\t".join(row_data))
 
    clipboard = QApplication.clipboard()
    clipboard.setText("\n".join(clipboard_text))
