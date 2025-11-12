import base64
import hashlib
import re
from lxml import etree 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_der_x509_certificate
from cryptography.hazmat.backends import default_backend
import json
import os

DSIG_NAMESPACE = 'http://www.w3.org/2000/09/xmldsig#'
NS = {'ds': DSIG_NAMESPACE}

def verify_xml_signature(file_path: str) -> dict:
    # 1. Khởi tạo cấu trúc kết quả JSON nhất quán
    result = {
        "verified": False,
        "status": "UNCHECKED",
        "message": "Chưa kiểm tra hoặc lỗi khởi tạo.",
        "integrity_check": {"valid": False, "digest_xml": "", "digest_calculated": ""},
        "signature_check": {"valid": False, "error_detail": None},
        "certificate_info": {}
    }
    
    digest_valid = False
    signature_valid = False

    # 2. Tải và làm sạch XML
    try:
        if not os.path.exists(file_path):
            result['status'] = "LOAD_ERROR"
            result['message'] = f"Lỗi: Không tìm thấy file {file_path}"
            return result
            
        with open(file_path, "r", encoding="utf-8") as f:
            xml_data = f.read()
        
        xml_data_cleaned = re.sub(r"<\?xml-stylesheet.*?\?>", "", xml_data, count=1) 
        root = etree.fromstring(xml_data_cleaned.encode('utf-8'))
        
    except Exception as e:
        result['status'] = "LOAD_ERROR"
        result['message'] = f"Lỗi tải/phân tích XML: {e}"
        return result

    # 3. KIỂM TRA TÍNH TOÀN VẸN (INTEGRITY)
    try:
        xpath_ref = f'.//ds:Reference[starts-with(@URI, "#")]'
        reference = root.xpath(xpath_ref, namespaces=NS)[0]
        
        result['integrity_check']['digest_xml'] = reference.find('ds:DigestValue', NS).text
        dlh_id = reference.get('URI')[1:]
        dlh_node = root.find(f'.//DLHDon[@Id="{dlh_id}"]')
        
        c14n_dlh_xml = etree.tostring(dlh_node, method='c14n', exclusive=False, with_comments=False)
        result['integrity_check']['digest_calculated'] = base64.b64encode(hashlib.sha1(c14n_dlh_xml).digest()).decode()
        
        digest_valid = (result['integrity_check']['digest_xml'] == result['integrity_check']['digest_calculated'])
        result['integrity_check']['valid'] = digest_valid
        
    except Exception as e:
        result['status'] = "DIGEST_ERROR"
        result['message'] = f"Lỗi kiểm tra Digest (Tính Toàn Vẹn): {e}"
        return result
        
    # 4. KIỂM TRA TÍNH XÁC THỰC (AUTHENTICITY)
    if digest_valid:
        try:
            signature_value = root.find('.//ds:SignatureValue', NS).text
            signature_bytes = base64.b64decode(signature_value)
            signed_info_node = root.find('.//ds:SignedInfo', NS)
            
            # Chuẩn hóa SignedInfo
            signed_info_copy = signed_info_node.xpath('.', namespaces=NS)[0]
            if 'xmlns' not in signed_info_copy.attrib:
                signed_info_copy.set('xmlns', DSIG_NAMESPACE)

            c14n_signed_info_xml = etree.tostring(signed_info_copy, method='c14n', exclusive=False, with_comments=False)
            
            # Trích xuất Public Key và thông tin chứng thư
            cert_b64 = root.find('.//ds:X509Certificate', NS).text
            cert_der = base64.b64decode(cert_b64)
            certificate = load_der_x509_certificate(cert_der, default_backend())
            public_key = certificate.public_key()
            
            result['certificate_info'] = {
                "subject": certificate.subject.rfc4514_string(),
                "issuer": certificate.issuer.rfc4514_string(),
                "not_valid_before": certificate.not_valid_before_utc.isoformat(),
                "not_valid_after": certificate.not_valid_after_utc.isoformat(),
            }

            public_key.verify(signature_bytes, c14n_signed_info_xml, padding.PKCS1v15(), hashes.SHA1())
            signature_valid = True
            
        except Exception as e:
            result['signature_check']['error_detail'] = str(e)
            signature_valid = False
        
        result['signature_check']['valid'] = signature_valid

    # 5. TỔNG HỢP KẾT QUẢ CUỐI CÙNG
    if digest_valid and signature_valid:
        result['verified'] = True
        result['status'] = "SUCCESS"
        result['message'] = "Xác minh HOÀN TOÀN THÀNH CÔNG."
    elif digest_valid and not signature_valid:
        result['status'] = "SIGNATURE_INVALID"
        result['message'] = "Lỗi CHỮ KÝ SỐ. Dữ liệu không bị sửa đổi, nhưng chữ ký không khớp."
    else:
        result['status'] = "DATA_MODIFIED"
        result['message'] = "Xác minh THẤT BẠI. Dữ liệu hóa đơn đã bị SỬA ĐỔI."
        
    return result

