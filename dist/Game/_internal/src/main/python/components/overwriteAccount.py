import json

from src.main.python.components.logger import *
from src.main.python.components.securePwd import encodePassword


def overwriteAccount(basePath, username, userAge, profilePicturePath, theme, password=None):

    saveDirectory = os.path.join(basePath, "userdata/profiles")
    savePath = os.path.join(saveDirectory, "profiles.json")

    if "src" in profilePicturePath:
        path = profilePicturePath.split("src", 1)
        root = "src"
    else:
        path = profilePicturePath.split("userdata", 1)
        root = "userdata"

    try:
        existingAccounts = {}

        if os.path.exists(savePath):
            with open(savePath, 'r', encoding = "UTF-8") as jsonFile:
                fileContents = jsonFile.read()
                if fileContents.strip():
                    existingAccounts = json.loads(fileContents)

        existingAccounts[username]["UserAge"] = userAge
        existingAccounts[username]["ProfilePicturePath"] = root + path[1]
        existingAccounts[username]["Theme"] = theme

        if password is not None:
            existingAccounts[username]["Password"] = encodePassword(password)

        with open(savePath, 'w', encoding = "UTF-8") as jsonFile:
            json.dump(existingAccounts, jsonFile, indent=4)

        return True

    except Exception as e:
        logger.info(f"Hiba: {e}")
        return False


def overWriteGuestAccount(basePath, username, theme):
    saveDirectory = os.path.join(basePath, "userdata/profiles")
    savePath = os.path.join(saveDirectory, "guestProfile.json")

    try:
        existingAccounts = {}

        if os.path.exists(savePath):
            with open(savePath, 'r') as jsonFile:
                fileContents = jsonFile.read()
                if fileContents.strip():
                    existingAccounts = json.loads(fileContents)

        existingAccounts[username]["Theme"] = theme

        with open(savePath, 'w') as jsonFile:
            json.dump(existingAccounts, jsonFile, indent=4)

        return True

    except Exception as e:
        logger.info(f"Hiba: {e}")
        return False
