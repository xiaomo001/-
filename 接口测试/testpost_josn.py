#coding:utf-8
import requests
import json

url = "http://api.common.updrv.com/json/mininews_status"
#payload ={"appid":"1111","unionid":"1111","pcid":"abc123456"}
f = open("data\\test.json","r")
payload = f.read()
print(payload)

#data_json=json.dumps(payload)
#r=requests.post('http://api.common.updrv.com/json/mininews_status',data=payload)

r = requests.post(url,json=payload)
print(r.status_code)
print(r.text)