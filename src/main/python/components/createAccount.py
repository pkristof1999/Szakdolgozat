import os
import json

from src.main.python.components.encodePwd import encodePassword


def createAccount(username, userAge, password, profilePicturePath):
    accountData = {
        username: {
            "UserAge": userAge,
            "Password": encodePassword(password),
            "ProfilePicturePath": profilePicturePath
        }
    }

    saveDirectory = "../../../userdata/profiles"
    os.makedirs(saveDirectory, exist_ok = True)

    savePath = os.path.join(saveDirectory, "profiles.json")

    try:
        existingAccounts = {}
        if os.path.exists(savePath):
            with open(savePath, 'r') as jsonFile:
                existingAccounts = json.load(jsonFile)

        existingAccounts.update(accountData)

        with open(savePath, 'w') as jsonFile:
            json.dump(existingAccounts, jsonFile, indent=4)

    except Exception as e:
        print("Hiba: ", e)
