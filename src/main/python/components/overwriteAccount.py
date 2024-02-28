import json

from src.main.python.components.logger import *
from src.main.python.components.securePwd import encodePassword


def overwriteAccount(username, userAge, profilePicturePath, theme, password=None):
    saveDirectory = "userdata/profiles"
    savePath = os.path.join(saveDirectory, "profiles.json")

    try:
        existingAccounts = {}

        if os.path.exists(savePath):
            with open(savePath, 'r') as jsonFile:
                fileContents = jsonFile.read()
                if fileContents.strip():
                    existingAccounts = json.loads(fileContents)

        existingAccounts[username]["UserAge"] = userAge
        existingAccounts[username]["ProfilePicturePath"] = profilePicturePath
        existingAccounts[username]["Theme"] = theme

        if password is not None:
            existingAccounts[username]["Password"] = encodePassword(password)

        with open(savePath, 'w') as jsonFile:
            json.dump(existingAccounts, jsonFile, indent=4)

        return True

    except Exception as e:
        logger.info(f"Hiba: {e}")
        return False


def overWriteGuestAccount(username, theme):
    saveDirectory = "userdata/profiles"
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
