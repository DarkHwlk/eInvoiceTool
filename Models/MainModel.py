import sys
import pandas as pd
import numpy as np
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QVariant, pyqtSignal
from PyQt5.QtGui import QFont

from Utils.Constant  import *
from Utils.DataTypes  import Data
from Utils.Helper  import extractKeyPathsValue

import pathlib
curDir = str(pathlib.Path(__file__).parent.absolute())
 
class MainModel(QtCore.QAbstractTableModel):
    def __init__(self, tableData = list(), generalData = dict()):
        super().__init__()
        self.__tableData = pd.DataFrame(tableData, columns = TABLE_HEADER)
        self.__generalData = generalData
        """
            data = [{"Table": list, "General": dict},...]
        """
        self.__data = list()
        self.__totalPage = 0
        self.__currentPage = 0
 
    def data(self, index, role):
        value = self.__tableData.iloc[index.row(), index.column()]
        if role == Qt.DisplayRole:
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d")
            if isinstance(value, float):
                return '{:,.2f}'.format(value).replace(',','*').replace('.', ',').replace('*','.')
            if isinstance(value, int):
                return '{:,}'.format(value).replace(',','.')
            if isinstance(value, np.int64):
                return '{:,}'.format(int(value)).replace(',','.')
            return str(value)
 
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
        return len(self.__tableData)
 
    def columnCount(self, index):
        return len(self.__tableData.columns)
 
    def headerData(self, section, orientation, role):
        # ection is the index of the column/row.
        if section < len(self.__tableData.columns):
            if role == Qt.DisplayRole:
                if orientation == Qt.Horizontal:
                    return self.__tableData.columns[section]
                    #return str(self.__tableData.columns[section])#Use for pandas
            if orientation == Qt.Horizontal and role == Qt.FontRole:
                # font = QFont()
                # font.setBold(True)
                # return font
                pass
            return QVariant()
    
    def setData(self, data: list):
        self.__data = data
        self.setTotalPage(len(data))
        self.setCurrentPage(0)
    
    def setTableData(self, data: list):
        self.beginResetModel()
        self.__tableData = pd.DataFrame(data, columns = TABLE_HEADER)
        self.endResetModel()
    
    def setGeneralData(self, data, key_path = []):
        if key_path == [] and isinstance(data, dict):
            self.__generalData = data
            paths = extractKeyPathsValue(data)
            print(paths)
            for path, value in paths:
                # Trigger signals
                print(path, value)
                self.generalDataUpdated.emit(value, path)
            return

        current = self.__generalData
        for key in key_path[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        current[key_path[-1]] = data
        # Trigger signal
        self.generalDataUpdated.emit(data, key_path)

    def getGeneralData(self, key_path = []):
        if key_path == []:
            return self.__generalData

        current = self.__generalData
        for key in key_path:
            current = current[key]
        return current
    
    def setCurrentPage(self, page: int):
        if page < 0 or page >= self.__totalPage:
            return
        self.__currentPage = page
        self.setGeneralData(self.__data[self.__currentPage]["General"])
        self.setTableData(self.__data[self.__currentPage]["Table"])
        self.currentPageUpdated.emit(self.__currentPage)
    
    def currentPage(self):
        return self.__currentPage

    def setTotalPage(self, total: int):
        if total < 0:
            return
        self.__totalPage = total
        self.totalPageUpdated.emit(self.__totalPage)

    def totalPage(self):
        return self.__totalPage

    generalDataUpdated = pyqtSignal(object, list)
    currentPageUpdated = pyqtSignal(int)
    totalPageUpdated = pyqtSignal(int)
