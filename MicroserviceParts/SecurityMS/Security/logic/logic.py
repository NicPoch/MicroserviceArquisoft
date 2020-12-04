import hashlib
from cryptography.fernet import Fernet,MultiFernet
from SecurityMS.settings import HASHES,SALT,KEY_F1,KEY_F2,KEY_F3,KEY_F4
from ..models import AuthUser
#hash
m=hashlib.sha512()
#Encryption
K1=Fernet(KEY_F1)
K2=Fernet(KEY_F2)
K3=Fernet(KEY_F3)
K4=Fernet(KEY_F4)
MF=MultiFernet([K1,K2,K3,K4])

def hasher(msg:str)->str:
    hashedMsg=msg
    for i in range(HASHES):
        m.update((str(hashedMsg)+SALT).encode())
        hashedMsg=m.digest()
    return str(hashedMsg)

def encryptedMSG(msg:str)->bytes:
    return MF.encrypt(msg.encode())

def decryptorMSG(msg:bytes)->str:
    return MF.decrypt(msg).decode()

def verify(username,password)->dict:
    #User info integrity
    username=decryptorMSG(username)
    hashedUsername=hasher(username)
    #Password Integrity
    password=decryptorMSG(password)
    hashedPassword=hasher(password)
    #See if user exists
    user=AuthUser.objects.get(password=hashedPassword,username=hashedUsername)
    try:
        hashedRol=hasher(user.rol)
        response={
            'username':encryptedMSG(username),
            'hashedUsername':hashedUsername,
            'password':encryptedMSG(password),
            'hashedpassword':hashedPassword,
            'rol':encryptedMSG(user.rol),
            'hashedRol':hashedRol
        }
        return response
    except Exception:
        return None

def createUser(username,password,rol)->bool:
    #User info integrity    
    username=decryptorMSG(username)
    hashedUsername=hasher(username)
    #Password Integrity
    password=decryptorMSG(password)
    hashedPassword=hasher(password)
    #decrypts Rol
    rol=decryptorMSG(rol)
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