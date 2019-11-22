"""
ECB没有偏移量
"""
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


def add_to_16(text):
    print(type(text))
    if len(text) % 16:
        add = 16 - (len(text) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


# 加密函数
def encrypt(text):
    key = '*4&4^3%2$7#6@9!8'.encode('utf-8')
    mode = AES.MODE_ECB
    text = add_to_16(text)
    cryptos = AES.new(key, mode)

    cipher_text = cryptos.encrypt(text)
    return b2a_hex(cipher_text)


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(self, text):
    cryptor = AES.new(self.key, self.mode)
    plain_text = str(cryptor.decrypt(text), encoding='utf-8')
    return self.unpad(plain_text.rstrip('\0'))


if __name__ == '__main__':
    en_text = '{"status":1,"data":{"miniSwitch":1,"miniPage":[],"tray":[],"createDeskIcon":[],"popup":[],"Win10Toast":[],"trayPopup":[]}}'
    #de_text = "uaOp2Yi1ADdATF9HNAp8sZTInslYcL8wMkASNQ3rHrN/3/qxDPIqNx+s6aIYdvoKldkJNntkrITj6LpBeGfzM9vgGdcMGvKp/KKJGH5QGEf2Db/pRLkhN7Sm/dkg7+NGwzR1BFFwiX47TSVLWRkMekUu4xNuxedhOYBWudl/fgw="
    add_en_text=add_to_16(en_text)
    encrypt_text = encrypt(add_en_text)
    print("加密:", encrypt_text)
    #print("解密:", d)