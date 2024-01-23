import json

from src.main.python.components.logger import *
from src.main.python.components.securePwd import encodePassword


def createAccount(username, userAge, password, profilePicturePath):
    accountData = {
        username: {
            "UserAge": userAge,
            "Password": encodePassword(password),
            "ProfilePicturePath": profilePicturePath,
            "timeSpentInLearn": 0,
            "goodAnswersInLearn": 0,
            "LearnMedal": 0,
            "QuizMedal": 0,
            "EmailMedal": 0,
            "badge01": 0,
            "badge02": 0,
            "badge03": 0,
            "badge04": 0,
            "badge05": 0,
            "badge06": 0,
            "Score": 0,
            "Theme": "default"
        }
    }

    saveDirectory = "../../../userdata/profiles"
    os.makedirs(saveDirectory, exist_ok = True)

    savePath = os.path.join(saveDirectory, "profiles.json")

    try:
        existingAccounts = {}
        if os.path.exists(savePath):
            with open(savePath, 'r') as jsonFile:
                fileContents = jsonFile.read()
                if fileContents.strip():
                    existingAccounts = json.loads(fileContents)

        if username in existingAccounts:
            return False

        existingAccounts.update(accountData)

        with open(savePath, 'w') as jsonFile:
            json.dump(existingAccounts, jsonFile, indent=4)

        return True

    except Exception as e:
        logger.info(f"Hiba: {e}")
