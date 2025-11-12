from lxml import etree
from signxml import XMLVerifier, SignatureConfiguration
import os

# --- Algorithm URIs ---
RSA_SHA1_URI = 'http://www.w3.org/2000/09/xmldsig#rsa-sha1'
SHA1_URI = 'http://www.w3.org/2000/09/xmldsig#sha1'

# Dữ liệu XML mẫu
signed_xml_data = """
<SignedData xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="Some Schema Location">
    <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
<SignedInfo>
<CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315#WithComments"/>
<SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
<Reference URI="#f7689cf0-ae58-4c70-854f-2715c1d26078">
<Transforms>
<Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
</Transforms>
<DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
<DigestValue>InEvl+td7c0ZTMKQi5iyIthOOKY=</DigestValue>
</Reference>
<Reference URI="#Timestamp">
<DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
<DigestValue>K4En9GUg9OE02ybfAuGa1MFdlyY=</DigestValue>
</Reference>
</SignedInfo>
<SignatureValue>ogZ1SbM066OllRd9uppHp2YiY3Ng1+vq0vK1wMOoL3PGGCwfb5+wBpFxKOd/Vi6dGxEKySviVlH4i18N62hyRnaSOgX7XX/K4Ra95SEmUodYcdBSDZHsfMRjqutnCEMvNlS/BNcXb3UfspBJjKFO7zTqTdz4OJ69gUGl3xTHVx6iHZlvtzvs3JvyR0O4pST77I1afhx6PD6Pm7K7hObVradzQZ7wp5DnOZbXGcTyELyV8sWvhtAGVoL/DAtrn5K/A/kSxnS2WCtT5OKg+rGdXtRikEWJCk5QmhmUEVHkeXeYZHQDogh9L1Dn+jP8889LmIybb4e28SKVOgI1sv+SSg==</SignatureValue>
<KeyInfo>
<X509Data>
<X509SubjectName>UID=MST:0110329220, CN=CÔNG TY TNHH ĐÀO TẠO THIÊN ƯNG, ST=Thành phố Hà Nội, C=VN</X509SubjectName>
<X509Certificate>MIIFWzCCBEOgAwIBAgIQVAEBZwRs9KxmbEXU5cN1LDANBgkqhkiG9w0BAQsFADBbMRcwFQYDVQQDDA5GYXN0Q0EgU0hBLTI1NjEzMDEGA1UECgwqQ8OUTkcgVFkgQ+G7lCBQSOG6pk4gQ0jhu64gS8OdIFPhu5AgRkFTVENBMQswCQYDVQQGEwJWTjAeFw0yNDA0MTIwMjEwMDBaFw0yNTEyMjIwODI4NTJaMH4xCzAJBgNVBAYTAlZOMR8wHQYDVQQIDBZUaMOgbmggcGjhu5EgSMOgIE7hu5lpMS4wLAYDVQQDDCVDw5RORyBUWSBUTkhIIMSQw4BPIFThuqBPIFRIScOKTiDGr05HMR4wHAYKCZImiZPyLGQBAQwOTVNUOjAxMTAzMjkyMjAwggEiMA0GCSqGSIhkiG9w0BAQsFAAOCAQEACeg+ouff/GXV/XzKhy+HgGGRIJvf6NrF/Zjm2TLIV+nbhInhZ6N9UaWX58tpVwZbq3LEdzTR1e8N8WqsbqgaWEQjxcOlnV8V5RDs+K/ah1Qje41dwl2DxpERHo6CrLTAHixQIi6mVvWkcVPjOW7ylXw4ehXUZ3nKxr+O/56eLKRIR47OgiY1/kJcMDXAWubOdg1IyoY8pFGp77y8kUh8W69fhbEfnlo5z9SSP4w/rdVqfuvfYyD2zjRcuNaoo0X10gB+kcwT5+Nf5tBCQls2nl9dSdBRdI6f02Im4r9C86LntTUuWc7ZMdXbj0CKmV1QpuZF4ZZ8ZxVPCPwWghRovg==</X509Certificate>
</X509Data>
</KeyInfo>
<Object Id="Timestamp">
<SignatureProperties>
<SignatureProperty Target="">
<SigningTime>2025-01-07T17:53:47</SigningTime>
</SignatureProperty>
</SignatureProperties>
</Object>
<OriginalData>This is the data that was signed.</OriginalData>
</Signature>
</SignedData>
"""

# 1. Parse the signed XML
try:
    signed_root = etree.fromstring(signed_xml_data.encode('utf-8'))
    
    # 🚨 BƯỚC SỬA LỖI: Loại bỏ thuộc tính schema validation
    XSI_NAMESPACE = "{http://www.w3.org/2001/XMLSchema-instance}"
    if XSI_NAMESPACE + 'schemaLocation' in signed_root.attrib:
        del signed_root.attrib[XSI_NAMESPACE + 'schemaLocation']
    if XSI_NAMESPACE + 'noNamespaceSchemaLocation' in signed_root.attrib:
        del signed_root.attrib[XSI_NAMESPACE + 'noNamespaceSchemaLocation']
        
except Exception as e:
    print(f"❌ Lỗi phân tích XML: {e}")
    exit()

# 2. Tạo đối tượng SignatureConfiguration (Tối giản hóa)
try:
    custom_config = SignatureConfiguration(
        signature_methods=[RSA_SHA1_URI],
        digest_algorithms=[SHA1_URI]
    )
except TypeError as e:
    print(f"Lỗi: {e}. Phiên bản signxml của bạn không thể sử dụng SignatureConfiguration.")
    exit()

# 3. Thực hiện Xác minh
try:
    verifier = XMLVerifier()
    
    verified_data = verifier.verify(
        signed_root,
        expect_config=custom_config,
        require_x509=False,
    )

    print("✅ Xác minh chữ ký XML thành công!")
    
    print("\n--- Nội dung đã được ký và xác minh ---")
    print(etree.tostring(signed_root.find('OriginalData'), pretty_print=True).decode())

except Exception as e:
    print(f"❌ Xác minh chữ ký XML thất bại: {e}")