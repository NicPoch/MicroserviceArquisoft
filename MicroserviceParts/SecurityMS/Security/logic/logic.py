import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from SecurityMS.settings import HASHES,SALT,KEY,IV,NONCE
from ..models import AuthUser
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

def verify(username,password)->dict:
    #User info integrity
    username=decryptorStr(username)
    hashedUsername=hasher(username)
    #Password Integrity
    password=decryptorStr(password)
    hashedPassword=hasher(password)
    #See if user exists
    user=AuthUser.objects.get(password=hashedPassword,username=hashedUsername)
    try:
        hashedRol=hasher(user.rol)
        response={
            'username':encryptedStr(username),
            'hashedUsername':hashedUsername,
            'password':encryptedStr(password),
            'hashedUsername':hashedPassword,
            'rol':encryptedStr(user.rol),
            'hashedRol':hashedRol
        }
        return response
    except Exception:
        return None

def createUser(username,password,rol)->bool:
    #User info integrity    
    username=decryptorStr(username)
    hashedUsername=hasher(username)
    #Password Integrity
    password=decryptorStr(password)
    hashedPassword=hasher(password)
    #decrypts Rol
    rol=decryptorStr(rol)
    #See if user exists
    user=AuthUser.objects.get(password=hashedPassword,username=hashedUsername)
    if user == None:
        try:
            newUser = AuthUser()
            newUser.rol=rol
            newUser.username=hashedUsername
            newUser.password=hashedPassword
            newUser.save()
            return True
        except Exception:
            return False
    else:
        return False