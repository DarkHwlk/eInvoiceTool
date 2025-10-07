# XmlReader
 
import threading
import xml.etree.ElementTree as ET
 
def singleton(cls):
    """
    A decorator that transforms a class into a thread-safe singleton.
    """
    instances = {}
    lock = threading.Lock()
 
    def get_instance(*args, **kwargs):
        with lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
 
@singleton
class XmlReader:
    def __init__(self):
        self._lock = threading.Lock()
        self._dataFiles = list()
 
    def readMultiFiles(self, paths):
        self._dataFiles.clear()
        total = len(paths)
        for path in paths:
            self.__readFileInThread(path, total) #TODO: Add to thread here
 
    def __readFileInThread(self, path, total):
        data = self.readFile(path)
        with self._lock:
            self._dataFiles.append(data)
            if len(self._dataFiles) == total:
                #TODO: emit signal finished readMultiFiles, send data: self._dataFiles
                #print(self._dataFiles)
                pass
 
    def readFile(self, path):
        tree = ET.parse(xmlFile)
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
        for rows in DSHHDVu:
            row = dict()
            for col in rows:
                row[col.tag] = col.text
                if col.tag == 'TSuat' and col.text == 'KCT':
                    row[col.tag] = 0
            tableData.append([
                row["STT"], row["THHDVu"], row["DVTinh"],
                int(row["SLuong"]), int(row["DGia"]),
                int(row["SLuong"]) * int(row["DGia"]), #Tien chua thue
                int(row["TSuat"]),
                int(row["SLuong"]) * int(row["DGia"]) * int(row["TSuat"]), #Tien thue
                row["ThTien"]
            ])
 
        print("Table: ", tableData)
        data = {"General": generalData, "Table": tableData}
        return data
 
xmlFile = 'data/hoadon.xml'
print("========= readFile =========")
XmlReader().readFile(xmlFile)
print("========= readMultiFiles =========")
XmlReader().readMultiFiles([xmlFile, xmlFile, xmlFile])
