import requests

x = requests.get('https://hoadondientu.gdt.gov.vn:30000/captcha', verify=False)
print(x.text)


