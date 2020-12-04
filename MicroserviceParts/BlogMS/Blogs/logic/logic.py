import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from BlogMS.settings import HASHES,SALT,KEY,IV,NONCE

#hash
m=hashlib.sha512()
#Encryption
algorithm=algorithms.ChaCha20(KEY.encode(),nonce=NONCE.encode())
cipher=Cipher(algorithm=algorithm,mode=None,backend=default_backend())#modes.CBC(IV.encode()),backend=default_backend())
encryptor=cipher.encryptor()
decryptor=cipher.decryptor()

def hasher(msg:str)->str:
    hashedMsg=msg
    for i in range(HASHES):
        m.update((str(hashedMsg)+SALT).encode())
        hashedMsg=m.digest()
    return str(hashedMsg)

def encryptedStr(msg:str)->str:
    return str(encryptor.update(msg)+encryptor.finalize())

def decryptorStr(msg:str)->str:
    return str(decryptor.update(msg.encode())+decryptor.finalize())

def credentialCheck(credential:dict)->bool:
    #username check
    username=decryptorStr(credential['username'])
    if(hasher(username)!=credential['hashedUsername']):
        return False
    #rol check
    rol=decryptorStr(credential['rol'])
    if(hasher(rol)!=credential['hashedRol']):
        return False
    #password check
    password=decryptorStr(credential['password'])
    if(hasher(password)!=credential['hashedPassword']):
        return False
    return True