# TableViewExample
import sys
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

import pathlib
curDir = str(pathlib.Path(__file__).parent.absolute())
 
class MainModel(QtCore.QAbstractTableModel):
    def __init__(self, tableData, generalData = dict()):
        super().__init__()
        self._tableData = tableData
        self._generalData = generalData
        self._header = list()
 
    def data(self, index, role):
        value = self._tableData[index.row()][index.column()]
 
        if role == Qt.DisplayRole:
            #Perform per-type checks and render accordingly.
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d")
            if isinstance(value, float):
                return "%.2f" % value
            if isinstance(value, str):
                return '"%s"' % value
            return value
 
        if role == Qt.BackgroundRole:
            return QtGui.QColor('lightgray')
 
        if role == Qt.TextAlignmentRole:
            if isinstance(value, int) or isinstance(value, float):
                return Qt.AlignVCenter + Qt.AlignRight
 
        if role == Qt.ForegroundRole: #color text
            if (isinstance(value, int) or isinstance(value, float)) and value < 0:
                return QtGui.QColor('red')
 
        if role == Qt.DecorationRole:
            if isinstance(value, bool):
                if value:
                    return QtGui.QIcon(curDir+'/../resources/ok.png')
                return QtGui.QIcon(curDir+'/../resources/nok.png')
            return 
 
    def rowCount(self, index):
        return len(self._tableData)
 
    def columnCount(self, index):
        return len(self._tableData[0])
 
    def headerData(self, section, orientation, role):
        #section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._header[section]
                #return str(self._tableData.columns[section])#Use for pandas
            #if orientation == Qt.Vertical:
                #return str(self._tableData.index[section]) #Use for pandas
 
    def setHeader(self, header):
        self._header = header
 
 
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
 
        self.table = QtWidgets.QTableView()
 
        data = [
            [True, 9, 2],
            [1, -1, 'hello'],
            [3.023, 5, -5],
            [3, 3, datetime(2017,10,1)],
            [7.555, 8, False],
        ]
        header = ["A", "B", "C"]
 
        self.model = MainModel(data)
        self.model.setHeader(header)
        self.table.setModel(self.model)
 
        self.setCentralWidget(self.table)
 
 
app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec_()
 
"""
Model:
    tableData [][]
    generalData dict()
 
    signal: generalDataChanged(value, depths[])
 
View:
    tableWidget
    generalWidgets dict()
 
    slot: onGeneralDataChanged(value, depths[])
"""
