import threading
import xml.etree.ElementTree as ET
import logging

from PyQt5.QtCore import (QObject, pyqtSignal)
from Utils.Helper import singleton, runThread
from Utils.Constant  import *
from Utils.SignatureVerifier  import verify_xml_signature

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
        # try:
        tree = ET.parse(path)
        root = tree.getroot()

        """ General Data """
        generalData = self.__getGeneralData(root, path)

        """ Table Data """
        tableData = self.__getTableData(root)

        """ Signature Data """
        signatureData = verify_xml_signature(path)

        logging.debug(f"General: {generalData}")
        logging.debug(f"Table: {tableData}")
        logging.info(f"Signature: {signatureData}")
        data = {
            "General": generalData,
            "Table": tableData,
            "Signature": signatureData
        }
        return data
        # except Exception as e:
        #     logging.error(f"Error when read xml file: {path} | error: {e}")
        #     return {"General": dict(), "Table": list()}

    def __getGeneralData(self, root, path):
        generalData = dict()
        generalData["TTChung"] = dict()
        generalData["NBan"] = dict()
        generalData["NMua"] = dict()
        generalData["TToan"] = dict()
        generalData["DSCKS"] = dict()
        generalData["XmlFilePath"] = path
        #TTChung
        TTChung = root.find("DLHDon").find("TTChung")
        for child in TTChung:
            if child.tag == "KHHDon":
                generalData["TTChung"]["KHHDon"] = generalData["TTChung"]["KHMSHDon"] + child.text
            elif child.tag == "SHDon":
                generalData["TTChung"]["SHDon"] = str(int(child.text)).zfill(8)
            else:
                generalData["TTChung"][child.tag] = child.text
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

        return generalData

    def __getTableData(self, root):
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
                # TSuat
                if col.tag == 'TSuat' and col.text == 'KCT':
                    rowData['TSuat'] = 0
                elif col.tag == 'TSuat':
                    rowData['TSuat'] = int(col.text[:-1])
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

        return tableData
