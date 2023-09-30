import os
import json

from src.main.python.components.encodePwd import encodePassword


def createAccount(username, userAge, password, profilePicturePath):
    accountData = {
        "Username": username,
        "UserAge": userAge,
        "Password": encodePassword(password),
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
