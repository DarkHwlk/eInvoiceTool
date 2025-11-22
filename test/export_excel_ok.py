import pandas as pd
from datetime import datetime
import os

DOT_BLANK = '....................................................................'

# --- Định dạng ---
format_base_left = {'align': 'left', 'valign': 'vcenter', "font_size": 10}
format_base_left_wrap = {'align': 'left', 'valign': 'vcenter', "font_size": 10, 'text_wrap': True}
format_base_left_top = {'align': 'left', 'valign': 'top', "font_size": 10}
format_base_left_top_wrap = {'align': 'left', 'valign': 'top', 'text_wrap': True, "font_size": 10}
format_center = {'align': 'center', 'valign': 'vcenter', "font_size": 10}
format_bold_center = {'bold': True, 'align': 'center', 'valign': 'vcenter', "font_size": 10}
format_bold_left = {'bold': True, 'align': 'left', 'valign': 'vcenter', "font_size": 10}

format_header = {
    'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, "font_size": 10
}
format_data_center = {'border': 1, 'align': 'center', 'valign': 'vcenter', "font_size": 10}
format_data_left = {'border': 1, 'align': 'left', 'valign': 'vcenter', "font_size": 10}
format_data_right = {'border': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0', "font_size": 10}
format_signature_info = {'align': 'center', 'italic': True, 'valign': 'vcenter', "font_size": 10}

format_border = {
    'top': {'top': 1},
    'bottom': {'bottom': 1},
    'left': {'left': 1},
    'right': {'right': 1},
    'top_thick': {'top': 2},
    'bottom_thick': {'bottom': 2}
}

def export_invoice_to_excel(invoice_data, file_name="hoa_don_dien_tu.xlsx"):
    # --- 1. Chuẩn bị Dữ liệu ---
    general = invoice_data.get('General', {})
    tt_chung = general.get('TTChung', {})
    n_ban = general.get('NBan', {})
    n_mua = general.get('NMua', {})
    t_toan = general.get('TToan', {})
    
    # Chuyển đổi thông tin mặt hàng thành DataFrame
    table_data = invoice_data.get('Table', [])
    df_table = pd.DataFrame(table_data, columns=[
        'STT', 'Tên hàng hóa, dịch vụ', 'Đơn vị tính', 'Số lượng', 
        'Đơn giá', 'Thành tiền', 'CKhau%', 'STCKhau', 'Tổng cộng' 
    ])
    df_items = df_table[['STT', 'Tên hàng hóa, dịch vụ', 'Đơn vị tính', 'Số lượng', 'Đơn giá', 'Thành tiền']].copy()
    
    kh_hieu = tt_chung.get('KHHDon', '...')
    so_hd = tt_chung.get('SHDon', '...')
    nlap_str = tt_chung.get('NLap', '20..-..-..')
        
    # Xử lý Ngày lập
    try:
        nlap = datetime.strptime(nlap_str, '%Y-%m-%d')
        ngay_thang_nam = f"Ngày {nlap.day} tháng {nlap.month} năm {nlap.year}"
    except:
        ngay_thang_nam = "Ngày ... tháng ... năm 20..."

    # Chuẩn bị giá trị tổng cộng
    tong_cong_thanh_tien = f"{int(t_toan.get('TgTCThue')):,}" if 'TgTCThue' in t_toan else DOT_BLANK
    thue_suat = t_toan.get('LTSuat', {}).get('TSuat', 'KCT') 
    tien_thue = f"{int(t_toan.get('TgTThue')):,}" if 'TgTThue' in t_toan else DOT_BLANK
    tong_cong_thanh_toan = f"{int(t_toan.get('TgTTTBSo')):,}" if 'TgTTTBSo' in t_toan else DOT_BLANK
    so_tien_bang_chu = t_toan.get('TgTTTBChu', DOT_BLANK)
    
    # --- 2. Ghi ra Excel ---
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('HoaDon')

    # --- TIÊU ĐỀ (Hàng 0-2) ---
    start_row = 0
    worksheet.set_row(start_row, 25)
    worksheet.merge_range(start_row, 0, start_row, 5, f"TÊN CỤC THUẾ: {DOT_BLANK}",\
        workbook.add_format({**format_bold_left, **format_border['top'], **format_border['left']}))
    worksheet.merge_range(start_row, 6, start_row, 7, f"Mẫu số: 01GTKT3/001",\
        workbook.add_format({**format_base_left, **format_border['top'], **format_border['right']}))

    start_row += 1
    worksheet.merge_range(start_row, 0, start_row, 5, tt_chung.get('THDon', 'HÓA ĐƠN').upper(),\
        workbook.add_format({**format_bold_center, **format_border['left']}))
    worksheet.merge_range(start_row, 6, start_row, 7, f"Ký hiệu: {kh_hieu}",\
        workbook.add_format({**format_base_left, **format_border['right']}))
    
    start_row += 1
    worksheet.merge_range(start_row, 0, start_row, 5, "Liên 1: Lưu",\
        workbook.add_format({**format_center, **format_border['left']}))
    worksheet.merge_range(start_row, 6, start_row, 7, f"Số: {so_hd}",\
        workbook.add_format({**format_base_left, **format_border['right']}))

    start_row += 1
    worksheet.merge_range(start_row, 0, start_row, 5, ngay_thang_nam,\
        workbook.add_format({**format_center, **format_border['bottom_thick'], **format_border['left']}))
    worksheet.merge_range(start_row, 6, start_row, 7, "",\
        workbook.add_format({**format_border['bottom_thick'], **format_border['right']}))
    
    # --- THÔNG TIN NGƯỜI BÁN ---
    start_row += 1
    worksheet.set_row(start_row, 30)
    worksheet.merge_range(start_row, 0, start_row, 7, f"Tên người bán: {n_ban.get('Ten', DOT_BLANK)}",\
        workbook.add_format({**format_base_left_wrap, **format_border['left'], **format_border['right']}))
    start_row += 1
    worksheet.merge_range(start_row, 0, start_row + 1, 7, f"Mã số thuế: {n_ban.get('MST', 'UNKNOWN!')}",\
        workbook.add_format({**format_base_left_top, **format_border['left'], **format_border['right']}))
    start_row += 2
    worksheet.set_row(start_row, 30)
    worksheet.merge_range(start_row, 0, start_row, 7, f"Địa chỉ: {n_ban.get('DChi', DOT_BLANK)}",\
        workbook.add_format({**format_base_left_top_wrap, **format_border['left'], **format_border['right']}))
    start_row += 1
    worksheet.set_row(start_row, 30)
    worksheet.merge_range(start_row, 0, start_row, 3, f"Điện thoại: {DOT_BLANK}",\
        workbook.add_format({**format_base_left_top, **format_border['bottom_thick'], **format_border['left']}))
    worksheet.merge_range(start_row, 4, start_row, 7, f"Số tài khoản: {DOT_BLANK}",\
        workbook.add_format({**format_base_left_top, **format_border['bottom_thick'], **format_border['right']}))
    
    # --- THÔNG TIN NGƯỜI MUA ---
    start_row += 1
    worksheet.set_row(start_row, 30)
    worksheet.merge_range(start_row, 0, start_row, 7, f"Tên người mua: {n_mua.get('HVTNMHang', DOT_BLANK)}",\
        workbook.add_format({**format_base_left_wrap, **format_border['left'], **format_border['right']}))
    start_row += 1
    worksheet.merge_range(start_row, 0, start_row + 1, 7, f"Mã số thuế: {DOT_BLANK}",\
        workbook.add_format({**format_base_left_top, **format_border['left'], **format_border['right']})) 
    start_row += 2
    worksheet.set_row(start_row, 30)
    worksheet.merge_range(start_row, 0, start_row, 7, f"Địa chỉ: {n_mua.get('DChi', DOT_BLANK)}",\
        workbook.add_format({**format_base_left_top_wrap, **format_border['left'], **format_border['right']}))
    start_row += 1
    worksheet.set_row(start_row, 30)
    worksheet.merge_range(start_row, 0, start_row, 7, f"Số tài khoản: {DOT_BLANK}",\
        workbook.add_format({**format_base_left_top_wrap, **format_border['bottom_thick'], **format_border['left'], **format_border['right']}))
    
    # --- BẢNG CHI TIẾT HÀNG HÓA ---
    start_row += 1
    col_map = {
        'STT': 0, 'Tên hàng hóa, dịch vụ': 1, 'Đơn vị tính': 4, 
        'Số lượng': 5, 'Đơn giá': 6, 'Thành tiền': 7
    }
    
    header_row = start_row
    headers_main = ['STT', 'Tên hàng hóa, dịch vụ', 'Đơn vị tính', 'Số lượng', 'Đơn giá', 'Thành tiền']
    headers_sub = ['1', '2', '3', '4', '5', '6=4x5']
    
    # Ghi Header
    for i, title in enumerate(headers_main):
        col = i if i < 2 else i + 2
        if i == 1:
            worksheet.merge_range(header_row, col, header_row, col+2, title, workbook.add_format(format_header))
            worksheet.merge_range(header_row + 1, col, header_row + 1, col+2, headers_sub[i], workbook.add_format(format_header))
        worksheet.write(header_row, col, title, workbook.add_format(format_header))
        worksheet.write(header_row + 1, col, headers_sub[i], workbook.add_format(format_header))
    
    # Ghi dữ liệu chi tiết
    data_row = header_row + 2
    for _, row in df_items.iterrows():
        sl = int(row['Số lượng'])
        dg = int(row['Đơn giá'])
        tt = int(row['Thành tiền'])
        worksheet.write(data_row, col_map['STT'], row['STT'], workbook.add_format(format_data_center))
        worksheet.merge_range(data_row, col_map['Tên hàng hóa, dịch vụ'], data_row,\
            col_map['Đơn vị tính']-1, row['Tên hàng hóa, dịch vụ'],\
            workbook.add_format(format_data_left))
        worksheet.write(data_row, col_map['Đơn vị tính'], row['Đơn vị tính'], workbook.add_format(format_data_center))
        worksheet.write(data_row, col_map['Số lượng'], sl, workbook.add_format(format_data_right))
        worksheet.write(data_row, col_map['Đơn giá'], dg, workbook.add_format(format_data_right))
        worksheet.write(data_row, col_map['Thành tiền'], tt, workbook.add_format(format_data_right))
        data_row += 1

    # Thêm dòng trống
    num_empty_rows = max(0, 6 - len(df_items))
    for _ in range(num_empty_rows):
        col = i if i < 2 else i + 2
        worksheet.write(data_row, 0, '', workbook.add_format(format_data_center))
        worksheet.merge_range(data_row, 1, data_row, 3, '', workbook.add_format(format_header))
        worksheet.write_row(data_row, 4, [''] * 4, workbook.add_format(format_data_center))
        data_row += 1

    # --- THÔNG TIN TỔNG CỘNG ---
    
    # Cộng tiền hàng 
    worksheet.set_row(data_row, 25)
    worksheet.merge_range(data_row, 0, data_row, 7, f"Cộng tiền hàng: {tong_cong_thanh_tien}",\
        workbook.add_format({**format_base_left, **format_border['left'], **format_border['right'], **format_border['top_thick'], **format_border['bottom_thick']}))
    data_row += 1
    
    # Thuế suất GTGT & Tiền thuế GTGT
    worksheet.set_row(data_row, 25)
    thue_suat_text = "Thuế suất GTGT: KCT" if thue_suat == 'KCT' else f"Thuế suất GTGT: {thue_suat} %"
    
    worksheet.merge_range(data_row, 0, data_row, 2, thue_suat_text,\
        workbook.add_format({**format_base_left, **format_border['left'],  **format_border['bottom_thick']}))
    worksheet.merge_range(data_row, 3, data_row, 7, f"Tiền thuế GTGT: {tien_thue}",\
        workbook.add_format({**format_base_left, **format_border['right'],  **format_border['bottom_thick']}))
    data_row += 1

    # Tổng cộng tiền thanh toán 
    worksheet.set_row(data_row, 25)
    worksheet.merge_range(data_row, 0, data_row, 7, f"Tổng cộng tiền thanh toán: {tong_cong_thanh_toan}",\
        workbook.add_format({**format_base_left, **format_border['left'], **format_border['right'], **format_border['top_thick']}))
    data_row += 1

    # Số tiền viết bằng chữ
    worksheet.set_row(data_row, 25)
    worksheet.merge_range(data_row, 0, data_row, 7, f"Số tiền viết bằng chữ: {so_tien_bang_chu}",\
        workbook.add_format({**format_base_left_wrap, **format_border['left'], **format_border['right'], **format_border['bottom_thick']}))
    data_row += 1
    
    # --- CHỮ KÝ ---
    worksheet.merge_range(data_row, 0, data_row, 2, "NGƯỜI MUA HÀNG",\
        workbook.add_format({**format_bold_center, **format_border['left']}))
    worksheet.merge_range(data_row, 3, data_row, 7, "NGƯỜI BÁN HÀNG",\
        workbook.add_format({**format_bold_center, **format_border['right']}))
    data_row += 1
    
    worksheet.merge_range(data_row, 0, data_row, 2, "(Ký, ghi rõ họ, tên)",\
        workbook.add_format({**format_signature_info, **format_border['left']}))
    worksheet.merge_range(data_row, 3, data_row, 7, "(Ký, đóng dấu, ghi rõ họ, tên)",\
        workbook.add_format({**format_signature_info, **format_border['right']}))
    data_row += 1
    worksheet.merge_range(data_row, 0, data_row, 7, "(Cần kiểm tra, đối chiếu khi lập, giao, nhận hóa đơn)",\
        workbook.add_format({**format_signature_info, **format_border['left'], **format_border['right'], **format_border['bottom_thick']}))
    data_row += 2
    
    # --- GHI CHÚ (LIÊN) ---
    worksheet.merge_range(data_row, 0, data_row, 5, "Ghi chú:", workbook.add_format(format_bold_left))
    data_row += 1
    worksheet.merge_range(data_row, 0, data_row, 5, "- Liên 1: Lưu", workbook.add_format(format_base_left))
    data_row += 1
    worksheet.merge_range(data_row, 0, data_row, 5, "- Liên 2: Giao người mua", workbook.add_format(format_base_left))
    data_row += 1
    worksheet.merge_range(data_row, 0, data_row, 5, "- Liên 3: Nội bộ", workbook.add_format(format_base_left))
    
    writer.close()
    print(f"✅ Đã xuất dữ liệu hóa đơn ra file: {file_name}")

# --- 3. DỮ LIỆU ĐẦU VÀO (TEST) ---
data = {'General': {'TTChung': {'PBan': '2.1.0', 'THDon': 'Hóa đơn giá trị gia tăng', 'KHMSHDon': '1', 'KHHDon': 'K25TTM', 'SHDon': '00218251', 'NLap': '2025-09-06', 'DVTTe': 'VND', 'TGia': '1', 'HTTToan': 'Tiền mặt/Chuyển khoản', 'MSTTCGP': '0101360697'}, 'NBan': {'Ten': 'CÔNG TY TNHH BỆNH VIỆN ĐKTN AN SINH - PHÚC TRƯỜNG MINH', 'MST': '0106793535', 'DChi': 'Số 8 đường Châu Văn Liêm, Phường Từ Liêm, Thành phố Hà Nội, Việt Nam'}, 'NMua': {'DChi': '129 Nguyễn Trãi, Phường Khương Đình, Thành phố Hà Nội', 'HVTNMHang': 'Đặng Khánh Hưng (03820000621)'}, 'TToan': {'LTSuat': {'TSuat': 'KCT', 'ThTien': '407000', 'TThue': '0'}, 'THTTLTSuat': None, 'TgTCThue': '407000', 'TgTThue': '0', 'TTCKTMai': '0', 'TgTTTBSo': '407000', 'TgTTTBChu': 'Bốn trăm lẻ bảy nghìn đồng chẵn./.'}, 'DSCKS': {'NBan': '{\n\t"integrity_check": {\n\t\t"valid": true,\n\t\t"digest_xml": "8fGl/eslMB/mPhF1NNjb33qOCdE=",\n\t\t"digest_calculated": "8fGl/eslMB/mPhF1NNjb33qOCdE="\n\t},\n\t"signature_check": {\n\t\t"valid": true,\n\t\t"error_detail": null\n\t},\n\t"certificate_info": {\n\t\t"subject": "C=VN,ST=Hà Nội,CN=CÔNG TY TNHH BỆNH VIỆN ĐKTN AN SINH - PHÚC TRƯỜNG MINH,UID=MST:0106793535",\n\t\t"issuer": "CN=BkavCA SHA256,O=Bkav Corporation,C=VN",\n\t\t"not_valid_before": "2024-05-24T12:16:28+00:00",\n\t\t"not_valid_after": "2029-05-09T03:33:06+00:00"\n\t},\n\t"SigningTime": "2025-09-06T11:20:34"\n}'}, 'XmlFilePath': 'E:/Hwng/Projects/Invoice Tool/data/K25TTM-00218251-UKVF96OM2K5-DPH.xml'}, 'Table': [['1', 'Khám Nội tiêu hóa', 'Lần', '1', '249400', 249400, 0, 0, '249400'], ['2', 'Đo hoạt độ AST (GOT)', 'Lần', '1', '90000', 90000, 0, 0, '90000'], ['3', 'Đo hoạt độ ALT (GPT)', 'Lần', '1', '67600', 67600, 0, 0, '67600']]}

output_file = "hoa_don_gia_tri_gia_tang_optimized.xlsx"

# Gọi hàm
if __name__ == "__main__":
    try:
        export_invoice_to_excel(data, output_file)
    except ModuleNotFoundError as e:
        print(f"Lỗi: {e}")
        print("\nĐể chạy code này, bạn cần cài đặt các thư viện sau:")
        print("pip install pandas xlsxwriter")
    except Exception as e:
        print(f"Đã xảy ra lỗi trong quá trình xuất Excel: {e}")