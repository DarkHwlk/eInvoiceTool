import xml.etree.ElementTree as ET
import base64
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_der_x509_certificate
from cryptography.hazmat.backends import default_backend
import re

HOADON_PATH = r"E:\Hwng\Projects\Invoice Tool\test\hoa_don.xml"

# Đọc file XML hóa đơn
with open(HOADON_PATH, "r", encoding="utf-8") as f:
    xml_data = f.read()

# Namespace chữ ký số
ns = {
    'ds': 'http://www.w3.org/2000/09/xmldsig#'
}

# Xử lý nội dung XML: Loại bỏ tiền tố XML-stylesheet nếu có
xml_data_cleaned = re.sub(r"<\?xml-stylesheet.*?\?>", "", xml_data, 1)
root = ET.fromstring(xml_data_cleaned)

# --------------------------------------------------------------------------------
## 1. Tự động tìm kiếm DigestValue và Dữ liệu đã ký (DLHDon)
# --------------------------------------------------------------------------------

# 1.1. Sửa lỗi: Tìm tất cả thẻ Reference, sau đó lọc thủ công trong Python
# Sử dụng XPath đơn giản mà ET hỗ trợ
all_references = root.findall('.//ds:Reference', ns)
reference_node = None
dlh_id = None

# Lặp qua các Reference để tìm thẻ có URI bắt đầu bằng '#'
for ref in all_references:
    uri = ref.get('URI')
    if uri and uri.startswith('#'):
        reference_node = ref
        dlh_id = uri[1:] # Bỏ ký tự '#'
        break # Lấy tham chiếu đầu tiên thường là DLHDon chính

if reference_node is None:
    raise ValueError("Không tìm thấy thẻ <Reference> tham chiếu đến DLHDon.")

# Lấy giá trị DigestValue gốc
digest_value_node = reference_node.find('ds:DigestValue', ns)
if digest_value_node is None:
    raise ValueError("Không tìm thấy thẻ <DigestValue> trong Reference.")
digest_value = digest_value_node.text


# 1.2. Tự động trích xuất nội dung DLHDon để hash
# Tìm thẻ DLHDon dựa trên ID đã trích xuất
dlh_node = root.find(f'.//DLHDon[@Id="{dlh_id}"]')

if dlh_node is None:
    # Trường hợp không có thuộc tính Id, thử tìm DLHDon đầu tiên
    dlh_node = root.find('.//DLHDon')
    if dlh_node is None:
        raise ValueError("Không tìm thấy thẻ <DLHDon> trong hóa đơn.")

# 🚨 CẢNH BÁO C14N QUAN TRỌNG:
# ET.tostring() KHÔNG thực hiện chuẩn hóa XML Canonicalization (C14N) 1.0.
# Điều này làm cho hash tính toán (calculated_digest) hầu như chắc chắn bị SAI.
# Đây là lý do chính bạn cần dùng xmlsec/lxml.
dlh_xml_approx = ET.tostring(dlh_node, encoding='utf-8', method='xml')

# --------------------------------------------------------------------------------
## 2. Xác minh DigestValue (Kiểm tra tính toàn vẹn dữ liệu)
# --------------------------------------------------------------------------------

# Tính toán SHA1 hash
calculated_digest = base64.b64encode(hashlib.sha1(dlh_xml_approx).digest()).decode()
digest_valid = (digest_value == calculated_digest)

# --------------------------------------------------------------------------------
## 3. Xác minh Chữ ký số (Signature Verification)
# --------------------------------------------------------------------------------

# Trích xuất SignatureValue
signature_value = root.find('.//ds:SignatureValue', ns).text
signature_bytes = base64.b64decode(signature_value)

# Trích xuất SignedInfo (phần cần hash để verify)
signed_info_node = root.find('.//ds:SignedInfo', ns)

# 🚨 CẢNH BÁO C14N cho SignedInfo:
# Thẻ SignedInfo cũng cần C14N. ET.tostring() KHÔNG ĐỦ.
signed_info_xml = ET.tostring(signed_info_node, encoding='utf-8', method='xml')

# Trích xuất chứng thư số (Giữ nguyên)
cert_b64 = root.find('.//ds:X509Certificate', ns).text
cert_der = base64.b64decode(cert_b64)
certificate = load_der_x509_certificate(cert_der, default_backend())
public_key = certificate.public_key()

# Xác minh chữ ký
try:
    public_key.verify(
        signature_bytes,
        signed_info_xml, 
        padding.PKCS1v15(),
        hashes.SHA1() 
    )
    signature_valid = True
except Exception as e:
    signature_valid = False
    print(f"Lỗi xác minh chữ ký RSA-SHA1: {e}") 

# --------------------------------------------------------------------------------
## 4. In kết quả
# --------------------------------------------------------------------------------

print("--- KẾT QUẢ XÁC MINH HÓA ĐƠN ---")
print(f"ID DLHDon tự động trích xuất: {dlh_id}")
print(f"DigestValue gốc: {digest_value}")
print(f"DigestValue tính toán (C14N không chuẩn): {calculated_digest}")
print(f"✅ DigestValue: {'Hợp lệ (Chưa bị chỉnh sửa)' if digest_valid else '❌ Không hợp lệ (ĐÃ BỊ CHỈNH SỬA hoặc C14N SAI)'}")
print(f"✅ Chữ ký số: {'Hợp lệ (Chính xác)' if signature_valid else '❌ Không hợp lệ (Sai chữ ký hoặc C14N SAI)'}")
print("\n🔍 Thông tin chứng thư số:")
print(" - Chủ thể:", certificate.subject.rfc4514_string())
print(" - Nhà phát hành:", certificate.issuer.rfc4514_string())
print(" - Hiệu lực từ:", certificate.not_valid_before)
print(" - Hiệu lực đến:", certificate.not_valid_after)