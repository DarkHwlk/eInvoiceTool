# Read xml
import xml.etree.ElementTree as ET
 
xmlFile = 'E:\Hwng\Projects\Invoice Tool\data\K25TTM-00218251-UKVF96OM2K5-DPH.xml'
 
tree = ET.parse(xmlFile)
root = tree.getroot()
#for child in root:
#    print(child.tag, child.attrib)
 
data = dict()
data["NBan"] = dict()
data["NMua"] = dict()
data["DSHHDVu"] = list()
data["TToan"] = dict()
data["DSCKS"] = dict()
 
print("==================")
print("NBan:")
NBan = root.find("DLHDon").find("NDHDon").find("NBan")
for child in NBan:
    print(child.tag, child.text)
    data["NBan"][child.tag] = child.text
 
print("==================")
print("NMua:")
NMua = root.find("DLHDon").find("NDHDon").find("NMua")
for child in NMua:
    print(child.tag, child.text)
    data["NMua"][child.tag] = child.text
 
print("==================")
print("DSHHDVu:")
DSHHDVu = root.find("DLHDon").find("NDHDon").find("DSHHDVu")
for rows in DSHHDVu:
    row = dict()
    for col in rows:
        row[col.tag] = col.text
    print(row)
    data["DSHHDVu"].append(row)
 
print("==================")
print("TToan:")
TToan = root.find("DLHDon").find("NDHDon").find("TToan")
for child in TToan:
    if(child.tag == "THTTLTSuat"):
        data["TToan"]["LTSuat"] = dict()
        LTSuat = child.find("LTSuat")
        for subChild in LTSuat:
            data["TToan"]["LTSuat"][subChild.tag] = subChild.text
            print("LTSuat", subChild.tag, subChild.text)
    print(child.tag, child.text)
    data["TToan"][child.tag] = child.text
 
print("==================")
print("DSCKS:")
DSCKS = root.find("DSCKS")
for child in DSCKS:
    print(child.tag, child)
    data["DSCKS"][child.tag] = child
 
print("==================")
print("data", data)