import base64
from Crypto.Cipher import AES

'''
采用AES对称加密算法
'''
# str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes

#加密方法
def encrypt_oracle(encrypt_text):
    # 秘钥
    key = '*4&4^3%2$7#6@9!8'
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #先进行aes加密
    encrypt_aes = aes.encrypt(add_to_16(encrypt_text))
    #用base64转成字符串形式
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
    print(encrypted_text)
    
#解密方法
def decrypt_oralce(decrypt_text):
    # 秘钥
    key = '*4&4^3%2$7#6@9!8'
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(decrypt_text.encode(encoding='utf-8'))
    #执行解密密并转码返回str
    decrypted_text = str(aes.decrypt(base64_decrypted),encoding='utf-8').replace('\0','')
    print(decrypted_text)

if __name__ == '__main__':
    en_text = '{"status":1,"data":{"miniSwitch":1,"miniPage":[],"tray":[],"createDeskIcon":[],"popup":[],"Win10Toast":[],"trayPopup":[]}}'
    de_text = "uaOp2Yi1ADdATF9HNAp8sZTInslYcL8wMkASNQ3rHrN/3/qxDPIqNx+s6aIYdvoKldkJNntkrITj6LpBeGfzM9vgGdcMGvKp/KKJGH5QGEf2Db/pRLkhN7Sm/dkg7+NGwzR1BFFwiX47TSVLWRkMekUu4xNuxedhOYBWudl/fgw="
    encrypt_oracle(en_text)
    decrypt_oralce(de_text)