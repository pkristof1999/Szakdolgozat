import os
import json

from encodePwd import *


def createAccount(username, userAge, password, profilePicturePath):
    """encPwd = """
    accountData = {
        "Username": username,
        "UserAge": userAge,
        "Password": password,
        "ProfilePicturePath": profilePicturePath
    }

    saveDirectory = "../../../userdata/profiles"
    os.makedirs(saveDirectory, exist_ok = True)

    savePath = os.path.join(saveDirectory, "profiles.json")

    try:
        with open(savePath, 'w') as jsonFile:
            json.dump(accountData, jsonFile)
        print("Account data saved to", savePath)
    except Exception as e:
        print("Error:", e)
