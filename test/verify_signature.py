import xml.etree.ElementTree as ET
import base64
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_der_x509_certificate
from cryptography.hazmat.backends import default_backend
 
HOADON_PATH = r"E:\Hwng\Projects\Invoice Tool\test\hoa_don.xml"

#Đọc file XML hóa đơn
with open(HOADON_PATH, "r", encoding="utf-8") as f:
    xml_data = f.read()
 
#Namespace chữ ký số
ns = {'ds': 'http://www.w3.org/2000/09/xmldsig#'}
root = ET.fromstring(xml_data)
 
#Trích xuất DigestValue
digest_value = root.find('.//ds:Reference[@URI="#fb01448e-259e-4e8e-900c-614537201c0b"]/ds:DigestValue', ns).text
 
#Trích xuất nội dung DLHDon để hash
dlh_node = root.find('.//DLHDon')
dlh_xml = ET.tostring(dlh_node, encoding='utf-8', method='xml')
 
#Tính toán SHA1 hash
calculated_digest = base64.b64encode(hashlib.sha1(dlh_xml).digest()).decode()
digest_valid = (digest_value == calculated_digest)
 
#Trích xuất SignatureValue
signature_value = root.find('.//ds:SignatureValue', ns).text
signature_bytes = base64.b64decode(signature_value)
 
#Trích xuất SignedInfo
signed_info_node = root.find('.//ds:SignedInfo', ns)
signed_info_xml = ET.tostring(signed_info_node, encoding='utf-8', method='xml')
 
#Trích xuất chứng thư số
cert_b64 = root.find('.//ds:X509Certificate', ns).text
cert_der = base64.b64decode(cert_b64)
certificate = load_der_x509_certificate(cert_der, default_backend())
public_key = certificate.public_key()
 
#Xác minh chữ ký
try:
    public_key.verify(
        signature_bytes,
        signed_info_xml,
        padding.PKCS1v15(),
        hashes.SHA1()
    )
    signature_valid = True
except Exception:
    signature_valid = False
 
#In kết quả
print("✅ DigestValue:", "Hợp lệ" if digest_valid else "Không hợp lệ")
print("✅ Chữ ký số:", "Hợp lệ" if signature_valid else "Không hợp lệ")
print("🔍 Thông tin chứng thư số:")
print(" - Chủ thể:", certificate.subject.rfc4514_string())
print(" - Nhà phát hành:", certificate.issuer.rfc4514_string())
print(" - Hiệu lực từ:", certificate.not_valid_before)
 
#Nếu DigestValue khớp → hóa đơn chưa bị chỉnh sửa.
#Nếu không khớp → hóa đơn đã bị chỉnh sửa sau khi ký.
