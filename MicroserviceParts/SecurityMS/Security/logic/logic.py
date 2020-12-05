import hashlib
from cryptography.fernet import Fernet,MultiFernet
from SecurityMS.settings import HASHES,SALT,KEY_F1,KEY_F2,KEY_F3,KEY_F4
from ..models import AuthUser
#Encryption
K1=Fernet(KEY_F1)
K2=Fernet(KEY_F2)
K3=Fernet(KEY_F3)
K4=Fernet(KEY_F4)
MF=MultiFernet([K1,K2,K3,K4])

def hasher(msg:str)->str:
    m=hashlib.sha512()
    hashedMsg=(msg+SALT)
    for i in range(HASHES):
        m.update(hashedMsg.encode('utf-8'))
        hashedMsg=m.hexdigest()
    return str(hashedMsg)

def encryptedMSG(msg:str)->str:
    return str(MF.encrypt(msg.encode('utf-8'))).encode('utf-8')

def decryptorMSG(msg:str)->str:
    return MF.decrypt(eval(msg)).decode()

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

def createUser(request:dict)->bool:
    print("start create")
    if(hasher(decryptorMSG(request['username']))!=request['hashedUsername']):
        return False
    if(hasher(decryptorMSG(request['password']))!=request['hashedPassword']):
        return False
    if(hasher(decryptorMSG(request['rol']))!=request['hashedRol']):
        return False
    user=AuthUser.objects.check(password=hasher(decryptorMSG(request['password'])),username=hasher(decryptorMSG(request['username'])),rol=hasher(decryptorMSG(request['rol'])))
    if user == []:
        try:
            newUser = AuthUser()
            newUser.rol=hasher(decryptorMSG(request['rol']))
            newUser.username=hasher(decryptorMSG(request['username']))
            newUser.password=hasher(decryptorMSG(request['password']))
            newUser.save()
            return True
        except Exception:
            return False
    else:
        print(user)
        return False