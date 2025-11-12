import base64
import hashlib
import re
from lxml import etree 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_der_x509_certificate
from cryptography.hazmat.backends import default_backend

# ----------------------------------------------------------------------
# KHAI BÁO VÀ CHUẨN BỊ
# ----------------------------------------------------------------------
HOADON_PATH = r"E:\Hwng\Projects\Invoice Tool\test\hoa_don.xml"
DSIG_NAMESPACE = 'http://www.w3.org/2000/09/xmldsig#'
ns = {'ds': DSIG_NAMESPACE}

# Tải và chuẩn bị XML (Giữ nguyên)
try:
    with open(HOADON_PATH, "r", encoding="utf-8") as f:
        xml_data = f.read()
    xml_data_cleaned = re.sub(r"<\?xml-stylesheet.*?\?>", "", xml_data, count=1)
    root = etree.fromstring(xml_data_cleaned.encode('utf-8'))
except Exception as e:
    print(f"Lỗi tải/phân tích XML: {e}"); exit()

# ----------------------------------------------------------------------
# 1. KIỂM TRA TÍNH TOÀN VẸN (INTEGRITY)
# ----------------------------------------------------------------------

# Lấy DigestValue gốc và DLHDon node
xpath_reference = f'.//ds:Reference[starts-with(@URI, "#")]'
reference_node_list = root.xpath(xpath_reference, namespaces=ns)
if not reference_node_list: raise ValueError("Lỗi: Không tìm thấy Reference.")

reference = reference_node_list[0]
digest_value = reference.find('ds:DigestValue', ns).text
dlh_id = reference.get('URI')[1:]
dlh_node = root.find(f'.//DLHDon[@Id="{dlh_id}"]')

# Thực hiện C14N và Hash
c14n_dlh_xml = etree.tostring(dlh_node, method='c14n', exclusive=False, with_comments=False)
calculated_digest = base64.b64encode(hashlib.sha1(c14n_dlh_xml).digest()).decode()
digest_valid = (digest_value == calculated_digest)

# ----------------------------------------------------------------------
# 2. KIỂM TRA TÍNH XÁC THỰC (AUTHENTICITY)
# ----------------------------------------------------------------------

# Lấy SignatureValue và SignedInfo node
signature_value = root.find('.//ds:SignatureValue', ns).text
signature_bytes = base64.b64decode(signature_value)
signed_info_node = root.find('.//ds:SignedInfo', ns)
if signed_info_node is None: raise ValueError("Lỗi: Không tìm thấy SignedInfo.")

# Khắc phục lỗi C14N của SignedInfo (thêm xmlns thủ công)
if signed_info_node.tag == f'{{{DSIG_NAMESPACE}}}SignedInfo' and 'xmlns' not in signed_info_node.attrib:
    signed_info_node.set('xmlns', DSIG_NAMESPACE)

# Thực hiện C14N cho SignedInfo
c14n_signed_info_xml = etree.tostring(signed_info_node, method='c14n', exclusive=False, with_comments=False)

# Trích xuất Public Key
cert_b64 = root.find('.//ds:X509Certificate', ns).text
cert_der = base64.b64decode(cert_b64)
certificate = load_der_x509_certificate(cert_der, default_backend())
public_key = certificate.public_key()

signature_valid = False
signature_error_detail = ""
try:
    public_key.verify(
        signature_bytes,
        c14n_signed_info_xml, 
        padding.PKCS1v15(),
        hashes.SHA1() 
    )
    signature_valid = True
except Exception as e:
    signature_error_detail = str(e)
    
# ----------------------------------------------------------------------
# 3. KẾT LUẬN VÀ IN KẾT QUẢ
# ----------------------------------------------------------------------
print("--- KẾT QUẢ XÁC MINH HÓA ĐƠN ĐIỆN TỬ ---")
print(f"DigestValue gốc: {digest_value}")
print(f"DigestValue tính toán: {calculated_digest}")
print("-" * 50)

# LOGIC CHỈ RÕ LỖI
if digest_valid and signature_valid:
    print("✅ XÁC MINH HOÀN TOÀN THÀNH CÔNG!")
    print("   -> 1. Tính Toàn Vẹn Hóa Đơn: ĐẢM BẢO (DigestValue KHỚP).")
    print("   -> 2. Tính Xác Thực Chữ Ký: CHÍNH XÁC (Signature HỢP LỆ).")
    
elif not digest_valid:
    # LỖI: HÓA ĐƠN ĐÃ BỊ CHỈNH SỬA
    print("❌ XÁC MINH THẤT BẠI: DỮ LIỆU HÓA ĐƠN ĐÃ BỊ SỬA ĐỔI!")
    print("   -> 1. Tính Toàn Vẹn Hóa Đơn: ❌ KHÔNG ĐẢM BẢO (DigestValue KHÔNG KHỚP).")
    print("   -> 2. Tính Xác Thực Chữ Ký: KHÔNG THỂ KIỂM TRA (Dữ liệu đã sai).")

elif digest_valid and not signature_valid:
    # LỖI: CHỮ KÝ SỐ CÓ VẤN ĐỀ
    print("⚠️ XÁC MINH THẤT BẠI: LỖI CHỮ KÝ SỐ!")
    print("   -> 1. Tính Toàn Vẹn Hóa Đơn: ✅ ĐẢM BẢO (Hóa đơn CHƯA bị sửa đổi).")
    print("   -> 2. Tính Xác Thực Chữ Ký: ❌ SAI (Signature KHÔNG HỢP LỆ).")
    print(f"   * Nguyên nhân phổ biến: Sai sót C14N SignedInfo hoặc chữ ký bị lỗi/hỏng.")
    if signature_error_detail:
        print(f"   * Lỗi chi tiết (Cryptog.: {signature_error_detail})")

print("-" * 50)
print("\n🔍 Thông tin Chứng thư số:")
print(" - Chủ thể:", certificate.subject.rfc4514_string())
print(" - Nhà phát hành:", certificate.issuer.rfc4514_string())
print(" - Hiệu lực từ:", certificate.not_valid_before_utc)
print(" - Hiệu lực đến:", certificate.not_valid_after_utc)