import sys
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QFont

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
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d")
            if isinstance(value, float):
                return '{:,.2f}'.format(value).replace(',','*').replace('.', ',').replace('*','.')
            if isinstance(value, int):
                return '{:,}'.format(value).replace(',','.')
            return value
 
        if role == Qt.BackgroundRole:
            # return QtGui.QColor('lightgray')
            pass
 
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
        if section < len(self._header):
            if role == Qt.DisplayRole:
                if orientation == Qt.Horizontal:
                    return self._header[section]
                    #return str(self._tableData.columns[section])#Use for pandas
                if orientation == Qt.Vertical:
                    pass
                    #return str(self._tableData.index[section]) #Use for pandas
            if orientation == Qt.Horizontal and role == Qt.FontRole:
                # font = QFont()
                # font.setBold(True)
                # return font
                pass
            return QVariant()

    def setHeader(self, header):
        self._header = header
