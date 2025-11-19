import pandas as pd
from datetime import datetime
import os

def export_invoice_to_excel(invoice_data, file_name="hoa_don_dien_tu.xlsx"):
    """
    Xuất dữ liệu hóa đơn điện tử từ dictionary sang file Excel (.xlsx)
    với định dạng gần giống mẫu hóa đơn giá trị gia tăng.

    Args:
        invoice_data (dict): Dữ liệu hóa đơn đã được parse.
        file_name (str): Tên file Excel đầu ra.
    """
    
    # --- 1. Chuẩn bị Dữ liệu ---
    
    # Lấy thông tin chung
    general = invoice_data.get('General', {})
    tt_chung = general.get('TTChung', {})
    n_ban = general.get('NBan', {})
    n_mua = general.get('NMua', {})
    t_toan = general.get('TToan', {})
    
    # Chuyển đổi thông tin mặt hàng thành DataFrame
    table_data = invoice_data.get('Table', [])
    # Cột 6=4x5 là Thành tiền, lấy cột thứ 5 trong list (index 5)
    df_table = pd.DataFrame(table_data, columns=[
        'STT', 'Tên hàng hóa, dịch vụ', 'Đơn vị tính', 'Số lượng', 
        'Đơn giá', 'Thành tiền', 'CKhau%', 'STCKhau', 'Tổng cộng' 
    ])
    
    # Chỉ giữ lại các cột cần hiển thị trên hóa đơn (STT, Tên, ĐVT, SL, ĐG, TT)
    df_items = df_table[['STT', 'Tên hàng hóa, dịch vụ', 'Đơn vị tính', 'Số lượng', 'Đơn giá', 'Thành tiền']].copy()
    
    # Chuẩn bị giá trị cho tiêu đề
    invoice_type = tt_chung.get('THDon', 'HÓA ĐƠN')
    kh_hieu = tt_chung.get('KHHDon', '...')
    so_hd = tt_chung.get('SHDon', '...')
    nlap_str = tt_chung.get('NLap', '20..-..-..')
    try:
        # Xử lý trường hợp KHHDon có thêm ký tự
        kh_hieu_clean = kh_hieu.lstrip('1') 
    except:
        kh_hieu_clean = kh_hieu
        
    try:
        nlap = datetime.strptime(nlap_str, '%Y-%m-%d')
        ngay_thang_nam = f"Ngày {nlap.day} tháng {nlap.month} năm {nlap.year}"
    except:
        ngay_thang_nam = "Ngày ... tháng ... năm 20..."

    # Chuẩn bị giá trị tổng cộng
    # Đảm bảo các giá trị số là int để định dạng đúng trong Excel
    tong_cong_thanh_tien = int(t_toan.get('TgTCThue', 0))
    thue_suat = t_toan.get('LTSuat', {}).get('TSuat', 'KCT') 
    tien_thue = int(t_toan.get('TgTThue', 0))
    tong_cong_thanh_toan = int(t_toan.get('TgTTTBSo', 0))
    so_tien_bang_chu = t_toan.get('TgTTTBChu', '.................................')
    
    # --- 2. Ghi ra Excel ---
    
    # Sử dụng ExcelWriter để tùy chỉnh định dạng
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('HoaDon')
    
    # --- Khai báo Định dạng ---
    format_center = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    format_left = workbook.add_format({'align': 'left', 'valign': 'vcenter'})
    format_bold_center = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
    format_bold_left = workbook.add_format({'bold': True, 'align': 'left', 'valign': 'vcenter'})
    
    # Định dạng bảng (có border)
    format_header = workbook.add_format({
        'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True
    })
    format_data_center = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
    format_data_left = workbook.add_format({'border': 1, 'align': 'left', 'valign': 'vcenter'})
    # Định dạng số có dấu phẩy ngăn cách hàng nghìn
    format_data_right = workbook.add_format({'border': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0'})
    
    # Định dạng chữ ký (in nghiêng)
    format_signature_info = workbook.add_format({'align': 'center', 'italic': True, 'valign': 'vcenter'})


    # Cài đặt độ rộng cột (tham khảo)
    worksheet.set_column('A:A', 5)  # STT
    worksheet.set_column('B:B', 35) # Tên hàng hóa
    worksheet.set_column('C:C', 10) # Đơn vị tính
    worksheet.set_column('D:D', 10) # Số lượng
    worksheet.set_column('E:E', 15) # Đơn giá
    worksheet.set_column('F:F', 20) # Thành tiền

    # --- TIÊU ĐỀ ---
    start_row = 0
    worksheet.write(start_row, 0, "TÊN CỤC THUẾ:", format_bold_left)
    worksheet.merge_range(start_row, 1, start_row, 4, invoice_type.upper(), format_bold_center)
    worksheet.write(start_row, 5, f"Mẫu số: 01GTKT3/001", format_bold_left)
    
    start_row += 1
    worksheet.merge_range(start_row, 1, start_row, 4, "Liên 1: Lưu", format_center)
    worksheet.write(start_row, 5, f"Ký hiệu: {kh_hieu_clean}", format_left)

    start_row += 1
    worksheet.merge_range(start_row, 1, start_row, 4, ngay_thang_nam, format_center)
    worksheet.write(start_row, 5, f"Số: {so_hd}", format_left)
    
    start_row += 2 # Bắt đầu từ hàng 4 (index 4)
    
    # --- THÔNG TIN NGƯỜI BÁN ---
    worksheet.merge_range(start_row, 0, start_row, 5, f"Tên người bán: **{n_ban.get('Ten', '.................................')}**", format_bold_left)
    start_row += 1
    worksheet.merge_range(start_row, 0, start_row, 2, f"Mã số thuế: **{n_ban.get('MST', 'UNKNOWN!')}**", format_bold_left)
    start_row += 1
    worksheet.merge_range(start_row, 0, start_row, 5, f"Địa chỉ: {n_ban.get('DChi', '.................................')}", format_left)
    start_row += 1
    worksheet.merge_range(start_row, 0, start_row, 2, f"Điện thoại: .......................................", format_left)
    worksheet.merge_range(start_row, 3, start_row, 5, f"Số tài khoản: .......................................", format_left)
    
    start_row += 2
    
    # --- THÔNG TIN NGƯỜI MUA ---
    worksheet.merge_range(start_row, 0, start_row, 5, f"Tên người mua: **{n_mua.get('HVTNMHang', '.................................')}**", format_bold_left)
    start_row += 1
    # MST người mua không có trong dữ liệu mẫu, dùng '...'
    worksheet.merge_range(start_row, 0, start_row, 2, f"Mã số thuế: **................................**", format_bold_left) 
    start_row += 1
    worksheet.merge_range(start_row, 0, start_row, 5, f"Địa chỉ: {n_mua.get('DChi', '.................................')}", format_left)
    start_row += 1
    worksheet.merge_range(start_row, 0, start_row, 2, f"Số tài khoản: .......................................", format_left)
    
    start_row += 2
    
    # --- BẢNG CHI TIẾT HÀNG HÓA ---
    col_map = {
        'STT': 0, 
        'Tên hàng hóa, dịch vụ': 1, 
        'Đơn vị tính': 2, 
        'Số lượng': 3, 
        'Đơn giá': 4, 
        'Thành tiền': 5
    }
    
    # Header chính
    header_row = start_row
    worksheet.write(header_row, col_map['STT'], 'STT', format_header)
    worksheet.write(header_row, col_map['Tên hàng hóa, dịch vụ'], 'Tên hàng hóa, dịch vụ', format_header)
    worksheet.write(header_row, col_map['Đơn vị tính'], 'Đơn vị tính', format_header)
    worksheet.write(header_row, col_map['Số lượng'], 'Số lượng', format_header)
    worksheet.write(header_row, col_map['Đơn giá'], 'Đơn giá', format_header)
    worksheet.write(header_row, col_map['Thành tiền'], 'Thành tiền', format_header)

    # Header phụ (1, 2, 3, 4, 5, 6=4x5)
    header_row += 1
    worksheet.write(header_row, col_map['STT'], '1', format_header)
    worksheet.write(header_row, col_map['Tên hàng hóa, dịch vụ'], '2', format_header)
    worksheet.write(header_row, col_map['Đơn vị tính'], '3', format_header)
    worksheet.write(header_row, col_map['Số lượng'], '4', format_header)
    worksheet.write(header_row, col_map['Đơn giá'], '5', format_header)
    worksheet.write(header_row, col_map['Thành tiền'], '6=4x5', format_header)
    
    # Ghi dữ liệu chi tiết
    data_row = header_row + 1
    
    # Ghi dữ liệu từ DataFrame
    for index, row in df_items.iterrows():
        # Chuyển đổi sang kiểu dữ liệu phù hợp trước khi ghi
        stt = row['STT']
        ten = row['Tên hàng hóa, dịch vụ']
        dvt = row['Đơn vị tính']
        sl = int(row['Số lượng'])
        dg = int(row['Đơn giá'])
        tt = int(row['Thành tiền'])

        worksheet.write(data_row, col_map['STT'], stt, format_data_center)
        worksheet.write(data_row, col_map['Tên hàng hóa, dịch vụ'], ten, format_data_left)
        worksheet.write(data_row, col_map['Đơn vị tính'], dvt, format_data_center)
        worksheet.write(data_row, col_map['Số lượng'], sl, format_data_right)
        worksheet.write(data_row, col_map['Đơn giá'], dg, format_data_right)
        worksheet.write(data_row, col_map['Thành tiền'], tt, format_data_right)
        data_row += 1

    # Thêm 5 dòng trống cho đủ mẫu (nếu dữ liệu ít hơn 5 dòng)
    num_empty_rows = max(0, 5 - len(df_items))
    for _ in range(num_empty_rows):
        worksheet.write(data_row, 0, '', format_data_center)
        worksheet.write(data_row, 1, '', format_data_left)
        worksheet.write(data_row, 2, '', format_data_center)
        worksheet.write(data_row, 3, '', format_data_right)
        worksheet.write(data_row, 4, '', format_data_right)
        worksheet.write(data_row, 5, '', format_data_right)
        data_row += 1

    # --- THÔNG TIN TỔNG CỘNG ---
    
    # Cộng tiền hàng (TgTCThue)
    worksheet.merge_range(data_row, 0, data_row, 4, "Cộng tiền hàng:", format_bold_left)
    worksheet.write(data_row, 5, tong_cong_thanh_tien, format_data_right)
    data_row += 1
    
    # Thuế suất GTGT & Tiền thuế GTGT
    thue_suat_text = f"Thuế suất GTGT: {thue_suat}" 
    if thue_suat == 'KCT':
        thue_suat_text = "Thuế suất GTGT: KCT (Không chịu thuế)"
    
    worksheet.merge_range(data_row, 0, data_row, 2, thue_suat_text, format_bold_left)
    worksheet.merge_range(data_row, 3, data_row, 4, "% Tiền thuế GTGT:", format_bold_left)
    worksheet.write(data_row, 5, tien_thue, format_data_right)
    data_row += 1

    # Tổng cộng tiền thanh toán (TgTTTBSo)
    worksheet.merge_range(data_row, 0, data_row, 4, "Tổng cộng tiền thanh toán:", format_bold_left)
    worksheet.write(data_row, 5, tong_cong_thanh_toan, format_data_right)
    data_row += 1

    # Số tiền viết bằng chữ (TgTTTBChu)
    worksheet.merge_range(data_row, 0, data_row, 5, f"Số tiền viết bằng chữ: {so_tien_bang_chu}", format_bold_left)
    data_row += 2
    
    # --- CHỮ KÝ ---
    
    # Người mua hàng
    worksheet.merge_range(data_row, 0, data_row, 2, "NGƯỜI MUA HÀNG", format_bold_center)
    # Người bán hàng
    worksheet.merge_range(data_row, 3, data_row, 5, "NGƯỜI BÁN HÀNG", format_bold_center)
    data_row += 1
    
    # Ghi chú dưới chữ ký
    # *** ĐÃ SỬA LỖI: Thay 'font_italic' bằng 'italic' ***
    worksheet.merge_range(data_row, 0, data_row, 2, "(Cần kiểm tra, đối chiếu khi lập, giao, nhận hóa đơn)", format_signature_info)
    worksheet.merge_range(data_row, 3, data_row, 5, "(Ký, đóng dấu, ghi rõ họ, tên)", format_signature_info)
    data_row += 1

    # Thêm khoảng trống cho chữ ký
    data_row += 3
    
    # --- GHI CHÚ (LIÊN) ---
    worksheet.merge_range(data_row, 0, data_row, 5, "Ghi chú:", format_bold_left)
    data_row += 1
    worksheet.merge_range(data_row, 0, data_row, 5, "- Liên 1: Lưu", format_left)
    data_row += 1
    worksheet.merge_range(data_row, 0, data_row, 5, "- Liên 2: Giao người mua", format_left)
    data_row += 1
    worksheet.merge_range(data_row, 0, data_row, 5, "- Liên 3: Nội bộ", format_left)
    
    # Lưu file
    writer.close()
    print(f"✅ Đã xuất dữ liệu hóa đơn ra file: {file_name}")

# --- 3. DỮ LIỆU ĐẦU VÀO (TEST) ---

data = {'General': {'TTChung': {'PBan': '2.1.0', 'THDon': 'Hóa đơn giá trị gia tăng', 'KHMSHDon': '1', 'KHHDon': 'K25TTM', 'SHDon': '00218251', 'NLap': '2025-09-06', 'DVTTe': 'VND', 'TGia': '1', 'HTTToan': 'Tiền mặt/Chuyển khoản', 'MSTTCGP': '0101360697'}, 'NBan': {'Ten': 'CÔNG TY TNHH BỆNH VIỆN ĐKTN AN SINH - PHÚC TRƯỜNG MINH', 'MST': '0106793535', 'DChi': 'Số 8 đường Châu Văn Liêm, Phường Từ Liêm, Thành phố Hà Nội, Việt Nam'}, 'NMua': {'DChi': '129 Nguyễn Trãi, Phường Khương Đình, Thành phố Hà Nội', 'HVTNMHang': 'Đặng Khánh Hưng (03820000621)'}, 'TToan': {'LTSuat': {'TSuat': 'KCT', 'ThTien': '407000', 'TThue': '0'}, 'THTTLTSuat': None, 'TgTCThue': '407000', 'TgTThue': '0', 'TTCKTMai': '0', 'TgTTTBSo': '407000', 'TgTTTBChu': 'Bốn trăm lẻ bảy nghìn đồng chẵn./.'}, 'DSCKS': {'NBan': '{\n\t"integrity_check": {\n\t\t"valid": true,\n\t\t"digest_xml": "8fGl/eslMB/mPhF1NNjb33qOCdE=",\n\t\t"digest_calculated": "8fGl/eslMB/mPhF1NNjb33qOCdE="\n\t},\n\t"signature_check": {\n\t\t"valid": true,\n\t\t"error_detail": null\n\t},\n\t"certificate_info": {\n\t\t"subject": "C=VN,ST=Hà Nội,CN=CÔNG TY TNHH BỆNH VIỆN ĐKTN AN SINH - PHÚC TRƯỜNG MINH,UID=MST:0106793535",\n\t\t"issuer": "CN=BkavCA SHA256,O=Bkav Corporation,C=VN",\n\t\t"not_valid_before": "2024-05-24T12:16:28+00:00",\n\t\t"not_valid_after": "2029-05-09T03:33:06+00:00"\n\t},\n\t"SigningTime": "2025-09-06T11:20:34"\n}'}, 'XmlFilePath': 'E:/Hwng/Projects/Invoice Tool/data/K25TTM-00218251-UKVF96OM2K5-DPH.xml'}, 'Table': [['1', 'Khám Nội tiêu hóa', 'Lần', '1', '249400', 249400, 0, 0, '249400'], ['2', 'Đo hoạt độ AST (GOT)', 'Lần', '1', '90000', 90000, 0, 0, '90000'], ['3', 'Đo hoạt độ ALT (GPT)', 'Lần', '1', '67600', 67600, 0, 0, '67600']]}

# Tên file xuất ra
output_file = "hoa_don_gia_tri_gia_tang.xlsx"

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