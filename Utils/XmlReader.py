import threading
import xml.etree.ElementTree as ET
import logging

from PyQt5.QtCore import (QObject, pyqtSignal)
from Utils.Helper import singleton, runThread
from Utils.Constant  import *

@singleton
class XmlReader(QObject):
    def __init__(self):
        self._lock = threading.Lock()
        self.__dataFiles = list()
        self.__readFinishedCallback = None
 
    def readFiles(self, paths, readFinishedCallback):
        self.__dataFiles.clear()
        self.__readFinishedCallback = readFinishedCallback
        total = len(paths)
        for path in paths:
            runThread(self.__readFileInThread, path, total)
 
    def __readFileInThread(self, path, total):
        data = self.__readFile(path)
        with self._lock:
            self.__dataFiles.append(data)
            if len(self.__dataFiles) == total:
                self.__readFinishedCallback(self.__dataFiles)
                self.__readFinishedCallback = None
 
    def __readFile(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
 
        """ General Data """
        generalData = dict()
        generalData["NBan"] = dict()
        generalData["NMua"] = dict()
        generalData["TToan"] = dict()
        generalData["DSCKS"] = dict()
        generalData["XmlFilePath"] = path
        #NBan
        NBan = root.find("DLHDon").find("NDHDon").find("NBan")
        for child in NBan:
            generalData["NBan"][child.tag] = child.text
        #NMua
        NMua = root.find("DLHDon").find("NDHDon").find("NMua")
        for child in NMua:
            generalData["NMua"][child.tag] = child.text
        #TToan
        TToan = root.find("DLHDon").find("NDHDon").find("TToan")
        for child in TToan:
            if(child.tag == "THTTLTSuat"):
                generalData["TToan"]["LTSuat"] = dict()
                LTSuat = child.find("LTSuat")
                for subChild in LTSuat:
                    generalData["TToan"]["LTSuat"][subChild.tag] = subChild.text
            generalData["TToan"][child.tag] = child.text
        #DSCKS
        DSCKS = root.find("DSCKS")
        for child in DSCKS:
            generalData["DSCKS"][child.tag] = child
 
        """ Table Data """
        tableData = list()
        #DSHHDVu
        DSHHDVu = root.find("DLHDon").find("NDHDon").find("DSHHDVu")
        for rawRow in DSHHDVu:
            rowData = dict()
            for col in rawRow:
                # logging.debug(f"col.tag: {col.tag} | rawRow[col.tag]: {rawRow[col.tag]} | type: {type(rawRow[col.tag])}")
                if col.text is None:
                    if col.tag == "THHDVu" or col.tag == "DVTinh":
                        rowData[col.tag] = ""
                    else:
                        rowData[col.tag] = 0
                else:
                    rowData[col.tag] = col.text
                if col.tag == 'TSuat' and col.text == 'KCT':
                    rowData[col.tag] = 0
            row = list()
            for tag in TABLE_HEADER_TAG:
                if tag in rowData:
                    tmp = rowData[tag]
                else:
                    if tag == "TCThue":
                        tmp = int(rowData["SLuong"]) * int(rowData["DGia"])
                    elif tag == "TThue":
                        tmp = int(rowData["SLuong"]) * int(rowData["DGia"]) * int(rowData["TSuat"])
                    else:
                        if tag == "THHDVu" or tag == "DVTinh":
                            tmp = ""
                        else:
                            tmp = 0
                        rowData[tag] = tmp
                row.append(tmp)
            tableData.append(row)
 
        logging.debug(f"General: {generalData}")
        logging.debug(f"Table: {tableData}")
        data = {"General": generalData, "Table": tableData}
        return data

