import requests
import AES_demo

url = "http://www.160.com"
r = requests.get(url)
#r = requests.g
print(r.status_code)
print(r.content)
AES_demo.encrypt_oracle( str(r.content, encoding = "utf-8"))