def extract_key_paths_value(data, parent_keys=None):
    if parent_keys is None:
        parent_keys = []
    result = []
    for key, value in data.items():
        current_path = parent_keys + [key]
        if isinstance(value, dict):
            result.extend(extract_key_paths_value(value, current_path))
        else:
            result.append((current_path, value))
    return result
 
def get_value_by_key_path(data, key_path):
    current = data
    for key in key_path:
        current = current[key]
    return current
 
def set_value_by_key_path(data, key_path, value):
    current = data
    for key in key_path[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    current[key_path[-1]] = value
 
data = {"test": "aaa", 'NBan': {'Ten': 'CÔNG TY TNHH BỆNH VIỆN ĐKTN AN SINH - PHÚC TRƯỜNG MINH', 'MST': '0106793535', 'DChi': 'Số 8 đường Châu Văn Liêm, Phường Từ Liêm, Thành phố Hà Nội, Việt Nam'}, 'NMua': {'DChi': '129 Nguyễn Trãi,  Phường Khương Đình, Thành phố Hà Nội', 'HVTNMHang': 'Đặng Khánh Hưng (03820000621)'}, 'TToan': {'LTSuat': {'TSuat': 'KCT', 'ThTien': '407000', 'TThue': '0'}, 'THTTLTSuat': None, 'TgTCThue': '407000', 'TgTThue': '0', 'TTCKTMai': '0', 'TgTTTBSo': '407000', 'TgTTTBChu': 'Bốn trăm lẻ bảy nghìn đồng chẵn./.'}}
 
# print("extract_key_paths_value:")
paths = extract_key_paths_value(data)
# for path, value in paths:
    # print(f"{path} => {value}")
 
key_path = ['test']
value = get_value_by_key_path(data, key_path)
print("get_value_by_key_path:", key_path, value)
 
# print("set_value_by_key_path:")
set_value_by_key_path(data, ['a', 'b', 'd'], 999)
 
set_value_by_key_path(data, ['x', 'y', 'z'], 'new')
 
# print(data)
