import requests
import base64
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import os
import json
import sys
import traceback


class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_ECB
        self.BS = AES.block_size
        # 补位
        self.pad = lambda s: s + (self.BS - len(s.encode('utf-8')) % self.BS) * chr(
            self.BS - len(s.encode('utf-8')) % self.BS)
        self.unpad = lambda s: s[0:-ord(s[-1])]

    def encrypt(self, text):
        newtext = self.pad(text).encode('utf-8')
        cryptor = AES.new(self.key, self.mode)
        # 目前AES-128 足够目前使用
        ciphertext = cryptor.encrypt(newtext)
        return ciphertext

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode)
        plain_text = str(cryptor.decrypt(text), encoding='utf-8')
        return self.unpad(plain_text.rstrip('\0'))


class GetSoftList(object):
    def __init__(self):
        self._aeskey = b'*4&4^3%2$7#6@9!8'
        self.filename = 'softlist.json'
        #self.headers = \
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
            }

    def AnalysisResult(self, datainfo):
        pass

    def SaveData(self, datainfo, filepath):
     pass

    def formatjson(self, jsoninfo):
        pass

    def PrintBannerInfo(self, info):
       pass

    def PrintSoftInfo(self, info):
       pass

    def GetbannerList(self, apiurl):
        pass

    def getListBySoftCategoryIdForHomePage(self, data, apiurl):
        "获取首页装机必备软件列表"
        filepath = db_file = os.path.join(os.path.dirname(__file__), '{name}.json'.format(name=data["SoftCategoryID"]))
        m_aes = prpcrypt(self._aeskey)

        jsonstr = json.dumps(data, ensure_ascii=False)
        cenddata = m_aes.encrypt(jsonstr)
        bcenddata = base64.b64encode(cenddata)
        cendstr = str(bcenddata, encoding='utf-8')

        result = requests.post(apiurl, data=cendstr, headers=self.headers)
        if 200 == result.status_code:
            print('正在解密数据...')
            try:
                bdata = base64.b64decode(result.text)
                strdata = m_aes.decrypt(bdata)
                trimdata = strdata.replace("\x05", "").replace("\x06", "").replace("\x07", "").replace("\t",
                                                                                                       "").replace("\n",
                                                                                                                   "")
                self.PrintSoftInfo(trimdata)
                self.SaveData(trimdata, filepath)

            except Exception as ex:
                ex_type, ex_val, ex_stack = sys.exc_info()
                print(ex_type)
                print(ex_val)
                for stack in traceback.extract_tb(ex_stack):
                    print(stack)
                print('分析数据失败')
        else:
            print('获取软件信息失败')

    def GetCategroyId(self, url):
        "获取软件类别"
        m_aes = prpcrypt(self._aeskey)
        result = requests.post(url, headers=self.headers)
        softid_dict = {}
        if 200 == result.status_code:
            print('正在解密数据...')
            try:
                bdata = base64.b64decode(result.text)
                strdata = m_aes.decrypt(bdata)
                trimdata = strdata.replace("\x05", "").replace("\x06", "").replace("\x07", "").replace("\t",
                                                                                                       "").replace("\n",
                                                                                                                   "")
                dictext = json.loads(trimdata)
                if 1 == dictext.get('status', 0):
                    if 'data' in dictext:
                        for item in dictext['data']['list']:
                            softtypeid = item.get('SoftCategoryID')
                            softtypename = item.get('SoftCategoryName')
                            softid_dict[softtypeid] = softtypename

            except Exception as ex:
                ex_type, ex_val, ex_stack = sys.exc_info()
                print(ex_type)
                print(ex_val)
                for stack in traceback.extract_tb(ex_stack):
                    print(stack)
                print('分析数据失败')
        else:
            print('获取软件信息失败')
        return softid_dict

    def GetSoft(self, data, apiurl):
        m_aes = prpcrypt(self._aeskey)

        jsonstr = json.dumps(data, ensure_ascii=False)
        cenddata = m_aes.encrypt(jsonstr)
        bcenddata = base64.b64encode(cenddata)
        cendstr = str(bcenddata, encoding='utf-8')

        result = requests.post(apiurl, data=cendstr, headers=self.headers)
        if 200 == result.status_code:
            # print('原始数据')
            # print(result.text)
            print('正在解密数据...')
            try:
                bdata = base64.b64decode(result.text)
                strdata = m_aes.decrypt(bdata)
                self.formatjson(strdata)
            except Exception as ex:
                ex_type, ex_val, ex_stack = sys.exc_info()
                print(ex_type)
                print(ex_val)
                for stack in traceback.extract_tb(ex_stack):
                    print(stack)
                print('分析数据失败')
        else:
            print('获取软件信息失败')


if __name__ == "__main__":

    while True:
        print("(1：测试搜索功能)\t  (2: 测试必备软件)\t (3:测试横幅)")
        functionID = 1
        try:
            functionID = int(input('输入功能ID(1 2)：'))
            if functionID == 1:
                m_SoftMgr = SoftMgr()
                m_SoftMgr.SearchSoft()
            elif functionID == 2:
                m_SoftMgr = SoftMgr()
                m_SoftMgr.GetCategroyId()
            elif functionID == 3:
                m_SoftMgr = SoftMgr()
                m_SoftMgr.GetBannerList()
        except:
            continue