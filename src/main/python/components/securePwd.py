import bcrypt
import base64


def encodePassword(password):
    encryptedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return base64.b64encode(encryptedPassword).decode('utf-8')


def checkPassword(givenPassword, storedPassword):
    if bcrypt.checkpw(givenPassword.encode("utf-8"), storedPassword):
        return True
    else:
        return False
