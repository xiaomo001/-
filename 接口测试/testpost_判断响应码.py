#coding:utf-8
import requests
import json
#payload ={"appid":"1111","unionid":"1111","pcid":"abc123456"}
f = open("data\\test.json","r")
payload = f.read()
print(payload)

#data_json=json.dumps(payload)
#r=requests.post('http://api.common.updrv.com/json/mininews_status',data=payload)

r=requests.post('http://api.common.updrv.com/json/mininews_status',json=payload)
print(r.text)
print (r.status_code)
if r.status_code == 200:
    print("请求成功。")
else:
    print("请求失败。")
