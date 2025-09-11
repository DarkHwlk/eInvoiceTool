import xml.etree.ElementTree as ET

tree = ET.parse('data\\K25TTM-00218251-UKVF96OM2K5-DPH.xml')
root = tree.getroot()

# for element in root.iter():
#     print(f"{element.tag} - {element.text}")

benBan = root.find('DLHDon').find('NDHDon').find('NBan')
print(benBan.find("Ten").text)
print(benBan.find("MST").text)
print(benBan.find("DChi").text)


