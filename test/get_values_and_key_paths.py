def get_values_and_key_paths(data, current_path=None):
    """
    Duyệt đệ quy qua dictionary lồng nhau và trả về một list các tuples:
    [(value, ['key1', 'key2', ...]), ...]
    """
    if current_path is None:
        current_path = []
    
    results = []
    
    # Kiểm tra nếu 'data' là một dictionary
    if isinstance(data, dict):
        for key, value in data.items():
            # Tạo đường dẫn mới bằng cách thêm khóa hiện tại
            new_path = current_path + [key]
            
            # Kiểm tra nếu giá trị là một dictionary lồng nhau khác
            if isinstance(value, dict):
                # Gọi đệ quy cho dictionary lồng nhau
                results.extend(get_values_and_key_paths(value, new_path))
            # Kiểm tra nếu giá trị là một list (để tránh lặp sâu vào list)
            elif isinstance(value, list):
                # Bạn có thể chọn cách xử lý list:
                # 1. Bỏ qua (như ví dụ này)
                # 2. Lặp qua list và thêm chỉ mục (index) vào path
                results.append((value, new_path))
            else:
                # Đây là giá trị cuối cùng (leaf value)
                results.append((value, new_path))
    
    # Nếu 'data' là giá trị không phải dict/list (ví dụ: chuỗi, số, None)
    else:
        results.append((data, current_path))
        
    return results

def getDataFromDepths(data_dict, depths):
    """
    Lấy giá trị từ dictionary lồng nhau bằng cách cung cấp một list các khóa (keys path).

    Tham số:
    - data_dict (dict): Dictionary nguồn (ví dụ: nested_data).
    - depths (list): List các khóa chỉ ra đường dẫn đến giá trị cần lấy.

    Trả về:
    - Giá trị tương ứng với depths.
    - None nếu không tìm thấy key ở bất kỳ cấp độ nào.
    """
    current_level = data_dict

    # Duyệt qua từng key trong list depths
    for key in depths:
        # Kiểm tra nếu cấp độ hiện tại là một dictionary VÀ key tồn tại trong đó
        if isinstance(current_level, dict) and key in current_level:
            # Di chuyển xuống cấp độ tiếp theo
            current_level = current_level[key]
        else:
            # Nếu key không tồn tại hoặc cấp độ hiện tại không phải là dict,
            # trả về None (hoặc có thể raise KeyError)
            print(f"Lỗi: Không tìm thấy key '{key}' trong đường dẫn.")
            return None
    
    # current_level chính là giá trị cuối cùng sau khi đã duyệt hết depths
    return current_level

nested_data = {
    "user_id": 101,
    "profile": {
        "name": "Alice",
        "contact": {
            "email": "alice@example.com",
            "phone": "123-456-789"
        },
        "details": {
            "status": "active"
        }
    },
    "settings": None
}
# Áp dụng hàm
final_results = get_values_and_key_paths(nested_data)
print(final_results)
print("---------------------------------")
for value, path in final_results:
    # Định dạng path cho dễ nhìn
    path_str = " -> ".join(path)
    print(f"Path: {path_str}")
    print(f"Value: {repr(value)}") # Dùng repr() để hiển thị chính xác các giá trị như None
    print("---")

print("getDataFromDepths:")
print(getDataFromDepths(nested_data, ['profile', 'name']))
