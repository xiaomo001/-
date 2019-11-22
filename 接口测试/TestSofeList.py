import requests
import base64
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import os
import json
import sys
import traceback

class prpcrypt():  
    def __init__(self,key):  
        self.key = key
        self.mode = AES.MODE_ECB  
        self.BS = AES.block_size  
        #补位  
        self.pad = lambda s: s + (self.BS - len(s.encode('utf-8')) % self.BS) * chr(self.BS - len(s.encode('utf-8')) % self.BS)   
        self.unpad = lambda s : s[0:-ord(s[-1])]  
       
    def encrypt(self,text):  
        newtext = self.pad(text).encode('utf-8')
        cryptor = AES.new(self.key,self.mode)  
        #目前AES-128 足够目前使用 
        ciphertext = cryptor.encrypt(newtext)
        return ciphertext

       
    #解密后，去掉补足的空格用strip() 去掉  
    def decrypt(self,text):  
        cryptor = AES.new(self.key,self.mode)  
        plain_text=str(cryptor.decrypt(text), encoding='utf-8')
        return self.unpad(plain_text.rstrip('\0'))  


class GetSoftList(object):
    def __init__(self):
        self._aeskey=b'*4&4^3%2$7#6@9!8'
        self.filename='softlist.json'
        self.headers = \
        {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }  
    
    def AnalysisResult(self,datainfo):
        dictext=json.loads(datainfo)
        print('...............软件列表..................')
        if 1 == dictext.get('status',0):
            print('找到相关软件 {} 款\n\n'.format(dictext['data'].get('count')))
            count=0
            if 'data' in dictext:
                for item in dictext['data']['list']:
                    softname=item.get('SoftInfoName')
                    print(softname)
                    count+=1
        print('\n\n返回软件数量为：{}'.format(count))
        print('................软件列表.................')

    def SaveData(self,datainfo,filepath):
        print('正在生成文件')
        try:
            with open(filepath, 'w',encoding='utf-8') as f:    #在代码当前目录生成一个data.json的文件
                 #json.dump(datainfo, f,ensure_ascii=False)
                f.write(datainfo)  
        except Exception as ex:
            ex_type, ex_val, ex_stack = sys.exc_info()
            print(ex_type)
            print(ex_val)
            for stack in traceback.extract_tb(ex_stack):
                print(stack)
            print('生成文件失败')

    def formatjson(self,jsoninfo):
        trimdata=jsoninfo.replace("\x05", "").replace("\x06", "").replace("\x07", "").replace("\t", "").replace("\n", "")
        filepath=db_file = os.path.join(os.path.dirname(__file__),self.filename)
        self.SaveData(trimdata,filepath)
        self.AnalysisResult(trimdata)


    def PrintBannerInfo(self,info):
        dictext=json.loads(info)
        print('...............横幅列表..................')
        if 1 == dictext.get('status',0):
            if 'data' in dictext:
                for item in dictext['data']['list']:
                    Description=item.get('Description')
                    TopicID=item.get('TopicID')
                    LongImageUrl=item.get('LongImageUrl')
                    SmallImageUrl=item.get('SmallImageUrl')
                    print('\n 描述：{des}\t TopId:{topid}\n bigimg:{bigimg}\n smallimg:{smallimg}\n'.format(des=Description,topid=TopicID,bigimg=LongImageUrl,smallimg=SmallImageUrl))

    def PrintSoftInfo(self,info):
        dictext=json.loads(info)
        print('...............软件列表..................')
        if 1 == dictext.get('status',0):
            count=0
            if 'data' in dictext:
                for item in dictext['data']['list']:
                    softname=item.get('SoftInfoName')
                    print(softname)
                    count+=1
        print('\n\n返回软件数量为：{}'.format(count))
        print('................软件列表.................')


    def GetbannerList(self,apiurl):
        "获取横幅信息"
        filepath=db_file = os.path.join(os.path.dirname(__file__),'横幅列表.json')
        m_aes=prpcrypt(self._aeskey)
        result=requests.post(apiurl,headers=self.headers)
        if 200 == result.status_code:
            print('正在解密数据...')
            try:
                bdata=base64.b64decode(result.text)
                strdata=m_aes.decrypt(bdata)
                trimdata=strdata.replace("\x05", "").replace("\x06", "").replace("\x07", "").replace("\t", "").replace("\n", "")
                self.SaveData(trimdata,filepath)
                self.PrintBannerInfo(trimdata)
            except Exception as ex:
                ex_type, ex_val, ex_stack = sys.exc_info()
                print(ex_type)
                print(ex_val)
                for stack in traceback.extract_tb(ex_stack):
                    print(stack)
                print('分析数据失败')
        else:
            print('获取横幅信息失败')



    def getListBySoftCategoryIdForHomePage(self,data,apiurl):
        "获取首页装机必备软件列表"
        filepath=db_file = os.path.join(os.path.dirname(__file__),'{name}.json'.format(name=data["SoftCategoryID"]))
        m_aes=prpcrypt(self._aeskey)

        jsonstr=json.dumps(data,ensure_ascii=False)
        cenddata=m_aes.encrypt(jsonstr)
        bcenddata=base64.b64encode(cenddata)
        cendstr=str(bcenddata, encoding='utf-8')

        result=requests.post(apiurl,data =cendstr,headers=self.headers)
        if 200 == result.status_code:
            print('正在解密数据...')
            try:
                bdata=base64.b64decode(result.text)
                strdata=m_aes.decrypt(bdata)
                trimdata=strdata.replace("\x05", "").replace("\x06", "").replace("\x07", "").replace("\t", "").replace("\n", "")
                self.PrintSoftInfo(trimdata)
                self.SaveData(trimdata,filepath)

            except Exception as ex:
                ex_type, ex_val, ex_stack = sys.exc_info()
                print(ex_type)
                print(ex_val)
                for stack in traceback.extract_tb(ex_stack):
                    print(stack)
                print('分析数据失败')
        else:
            print('获取软件信息失败')
        


    def GetCategroyId(self,url):
        "获取软件类别"
        m_aes=prpcrypt(self._aeskey)
        result=requests.post(url,headers=self.headers)
        softid_dict={}
        if 200 == result.status_code:
             print('正在解密数据...')
             try:
                bdata=base64.b64decode(result.text)
                strdata=m_aes.decrypt(bdata)
                trimdata=strdata.replace("\x05", "").replace("\x06", "").replace("\x07", "").replace("\t", "").replace("\n", "")
                dictext=json.loads(trimdata)
                if 1 == dictext.get('status',0):
                    if 'data' in dictext:
                        for item in dictext['data']['list']:
                            softtypeid=item.get('SoftCategoryID')
                            softtypename=item.get('SoftCategoryName')
                            softid_dict[softtypeid]=softtypename

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

    def GetSoft(self,data,apiurl):
        m_aes=prpcrypt(self._aeskey)

        jsonstr=json.dumps(data,ensure_ascii=False)
        cenddata=m_aes.encrypt(jsonstr)
        bcenddata=base64.b64encode(cenddata)
        cendstr=str(bcenddata, encoding='utf-8')

        result=requests.post(apiurl,data =cendstr,headers=self.headers)
        if 200 == result.status_code:
            #print('原始数据')
            #print(result.text)
            print('正在解密数据...')
            try:
                bdata=base64.b64decode(result.text)
                strdata=m_aes.decrypt(bdata)
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



class SoftMgr(object):

    
    def SearchSoft(self):
        OSID=[131072,65536,2048,1024,8,4]
        ostype=OSID[0]
        print('------系统类型说明-> (0: win10/64)\t(1: win10/32)\t(2: win7/64)\t(3: win7/32)\t(4: xp/64)\t(5: xp/32)------')
        try:
            ostype=OSID[int(input("请输入系统类型(0--5)"))]
        except:
            print('输入有误!!')
            return

        apiurl=r'http://isoft.updrv.com/api/soft/getListForSearchPage'
        info=GetSoftList()
        keyword=input('搜索软件：')
        print("开始获取软件信息")
        info.filename=keyword+'.json'
        data = \
            {
            "Rows":999,
            "Page":1,
            "Keywords":keyword,
            "SortWay":1,
            "OSID":ostype
            }

        info.GetSoft(data,apiurl)
        print("获取软件信息结束（原始数据保存在当前目录下）\n\n")

    def GetCategroyId(self):
        OSID=[131072,65536,2048,1024,8,4]
        ostype=OSID[0]
        print('------系统类型说明-> (0: win10/64)\t(1: win10/32)\t(2: win7/64)\t(3: win7/32)\t(4: xp/64)\t(5: xp/32)------')
        try:
            ostype=OSID[int(input("请输入系统类型(0--5)"))]
        except:
            print('输入有误!!')
            return

        print("正在获取软件类别列表.....")
        apiurl=r'http://isoft.updrv.com/api/softCategory/getListAllForHomePage'
        info=GetSoftList()
        iddict= info.GetCategroyId(apiurl)
        CategoryID=0
        if iddict:
            for item in iddict.keys():
                print('(ID:{id} Name:{name})'.format(id=item,name=iddict[item]),end="\t")
        else:
            print('从服务器获取页装机必备软件类别列表失败')
            return

        try:
            CategoryID=int(input('\n\n请输入软件类别ID:'))
            if CategoryID not in iddict.keys():
                print('软件类别无效!!')
                return;
            print("正在获取软件列表")
            data = \
            {
            "SoftCategoryID":CategoryID,
            "OSID":ostype
            }
            Getapiurl=r'http://isoft.updrv.com/api/soft/getListBySoftCategoryIdForHomePage'
            info.getListBySoftCategoryIdForHomePage(data,Getapiurl)
        except:
            print('获取数据出错!!')


    
    def GetBannerList(self):
        OSID=[131072,65536,2048,1024,8,4]
        ostype=OSID[0]
        print('------系统类型说明-> (0: win10/64)\t(1: win10/32)\t(2: win7/64)\t(3: win7/32)\t(4: xp/64)\t(5: xp/32)------')
        try:
            ostype=OSID[int(input("请输入系统类型(0--5)"))]
        except:
            print('输入有误!!')
            return

        print("正在获取横幅列表.....")
        apiurl=r'http://isoft.updrv.com/api/banner/getListAll'
        info=GetSoftList()
        iddict= info.GetbannerList(apiurl)


if __name__ == "__main__":

    while True:
        print("(1：测试搜索功能)\t  (2: 测试必备软件)\t (3:测试横幅)")
        functionID=1
        try:
            functionID=int(input('输入功能ID(1 2)：'))
            if functionID==1:
                m_SoftMgr = SoftMgr()
                m_SoftMgr.SearchSoft()
            elif functionID==2:
                m_SoftMgr = SoftMgr()
                m_SoftMgr.GetCategroyId()
            elif functionID==3:
                m_SoftMgr = SoftMgr()
                m_SoftMgr.GetBannerList()
        except:
            continue