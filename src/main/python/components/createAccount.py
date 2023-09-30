import os
import json


def createAccount(username, userAge, password, profilePicturePath):
    accountData = {
        "Username": username,
        "UserAge": userAge,
        "Password": password,
        "ProfilePicturePath": profilePicturePath
    }

    saveDirectory = f"../../../userdata/profiles/{username}'s profile"
    os.makedirs(saveDirectory, exist_ok = True)

    savePath = os.path.join(saveDirectory, "profile.json")

    try:
        with open(savePath, 'w') as jsonFile:
            json.dump(accountData, jsonFile)
        print("Account data saved to", savePath)
    except Exception as e:
        print("Error:", e)
