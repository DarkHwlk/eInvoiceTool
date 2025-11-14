import base64
import hashlib
import re
from lxml import etree 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_der_x509_certificate
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import json

DSIG_NAMESPACE = 'http://www.w3.org/2000/09/xmldsig#'
NS = {'ds': DSIG_NAMESPACE}

def _verify_single_signature(root_element: etree._Element, signature_node: etree._Element) -> dict:
    
    result = {
        "integrity_check": {"valid": False, "digest_xml": None, "digest_calculated": None},
        "signature_check": {"valid": False, "error_detail": None},
        "certificate_info": {},
        "SigningTime": None
    }
    digest_valid = False

    # KIỂM TRA TÍNH TOÀN VẸN (DIGEST)
    try:
        xpath_ref = f'./ds:SignedInfo/ds:Reference[starts-with(@URI, "#")]'
        reference = signature_node.xpath(xpath_ref, namespaces=NS)[0]
        
        digest_value_xml = reference.find('ds:DigestValue', NS).text
        result['integrity_check']['digest_xml'] = digest_value_xml
        
        dlh_id = reference.get('URI')[1:]
        dlh_node = root_element.find(f'.//DLHDon[@Id="{dlh_id}"]')

        c14n_dlh_xml = etree.tostring(dlh_node, method='c14n', exclusive=False, with_comments=False)
        digest_calculated = base64.b64encode(hashlib.sha1(c14n_dlh_xml).digest()).decode()
        
        result['integrity_check']['digest_calculated'] = digest_calculated
        
        digest_valid = (digest_value_xml == digest_calculated)
        result['integrity_check']['valid'] = digest_valid
        
    except Exception as e:
        result['integrity_check']['digest_calculated'] = f"LỖI_TÍNH_TOÁN: {e}"
        return result
        
    # KIỂM TRA TÍNH XÁC THỰC (SIGNATURE)
    if digest_valid:
        try:
            signature_value = signature_node.find('./ds:SignatureValue', NS).text
            signature_bytes = base64.b64decode(signature_value)
            signed_info_node = signature_node.find('./ds:SignedInfo', NS)
            
            # CHUẨN HÓA C14N CHO SignedInfo (DÙNG EXCLUSIVE C14N)
            signed_info_copy = signed_info_node.xpath('.', namespaces=NS)[0]
            
            c14n_signed_info_xml = etree.tostring(
                signed_info_copy, 
                method='c14n', 
                exclusive=True, 
                with_comments=False
            )
            
            # Trích xuất Public Key và thông tin chứng thư
            cert_b64 = signature_node.find('.//ds:X509Certificate', NS).text
            cert_der = base64.b64decode(cert_b64)
            certificate = load_der_x509_certificate(cert_der, default_backend())
            public_key = certificate.public_key()
            
            # Lấy thời gian ký (SigningTime)
            xpath_signing_time = './/ds:Object//*[local-name()="SigningTime"]'
            signing_time_nodes = signature_node.xpath(xpath_signing_time, namespaces=NS)
            
            if signing_time_nodes:
                result['SigningTime'] = signing_time_nodes[0].text
            
            # Lưu thông tin chứng thư
            result['certificate_info'] = {
                "subject": certificate.subject.rfc4514_string(),
                "issuer": certificate.issuer.rfc4514_string(),
                "not_valid_before": certificate.not_valid_before_utc.isoformat(),
                "not_valid_after": certificate.not_valid_after_utc.isoformat(),
            }

            # Xác minh chữ ký (SHA1)
            public_key.verify(signature_bytes, c14n_signed_info_xml, padding.PKCS1v15(), hashes.SHA1())
            result['signature_check']['valid'] = True
            result['signature_check']['error_detail'] = None
            
        except InvalidSignature as e:
            error_msg = str(e) if str(e) else "Invalid Signature (Verification Failed)"
            result['signature_check']['error_detail'] = error_msg
            result['signature_check']['valid'] = False
        except Exception as e:
            error_msg = str(e) if str(e) else type(e).__name__
            result['signature_check']['error_detail'] = f"Lỗi khác: {error_msg}"
            result['signature_check']['valid'] = False
        
    else:
        result['signature_check']['error_detail'] = "Xác minh THẤT BẠI. Dữ liệu đã bị SỬA ĐỔI (Digest không hợp lệ)."

    return result


def verify_multi_signature(file_path: str) -> dict:
    
    final_result = {}
    
    # Tải và làm sạch XML
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            xml_data = f.read()
        
        xml_data_cleaned = re.sub(r"<\?xml-stylesheet.*?\?>", "", xml_data, count=1) 
        root = etree.fromstring(xml_data_cleaned.encode('utf-8'))
        
    except Exception as e:
        return {"ERROR": f"Lỗi tải/phân tích XML: {e}"}

    # Lặp qua các bên ký trong DSCKS
    dscks_node = root.find('.//DSCKS')
    if dscks_node is None:
        return {"WARNING": "Không tìm thấy khối chữ ký DSCKS nào trong hóa đơn."}

    for child in dscks_node:
        entity_key = child.tag
        signature_node = child.find('./ds:Signature', NS)
        
        if signature_node is not None:
            entity_result = _verify_single_signature(root, signature_node)
            final_result[entity_key] = entity_result
            
        else:
            final_result[entity_key] = None
            
    return final_result

# --- CÁCH SỬ DỤNG ---
# HOADON_PATH = r"E:\Hwng\Projects\Invoice Tool\test\hoa_don.xml"
# print(json.dumps(verify_multi_signature(HOADON_PATH), indent=4, ensure_ascii=False))