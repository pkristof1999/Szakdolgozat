import json

from src.main.python.components.logger import *
from src.main.python.components.securePwd import encodePassword


def createAccount(basePath, username, userAge, password, profilePicturePath, notDefault):
    if notDefault:
        path = profilePicturePath.split("userdata", 1)
        root = "userdata"
    else:
        path = profilePicturePath.split("src", 1)
        root = "src"

    accountData = {
        username: {
            "UserAge": userAge,
            "Password": encodePassword(password),
            "ProfilePicturePath": root + path[1],
            "completedLessonInLearn": {
                "lesson1": 0,
                "lesson2": 0,
                "lesson3": 0,
                "lesson4": 0,
                "lesson5": 0,
                "lesson6": 0,
                "lesson7": 0,
                "lesson8": 0
            },
            "timeSpentInLearn": {
                "lesson1": 0,
                "lesson2": 0,
                "lesson3": 0,
                "lesson4": 0,
                "lesson5": 0,
                "lesson6": 0,
                "lesson7": 0,
                "lesson8": 0
            },
            "goodAnswersInLearn": {
                "lesson1": 0,
                "lesson2": 0,
                "lesson3": 0,
                "lesson4": 0,
                "lesson5": 0,
                "lesson6": 0,
                "lesson7": 0,
                "lesson8": 0
            },
            "LearnMessageShown": False,
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

    saveDirectory = os.path.join(basePath, "userdata/profiles")
    os.makedirs(saveDirectory, exist_ok=True)

    savePath = os.path.join(saveDirectory, "profiles.json")

    try:
        existingAccounts = {}
        if os.path.exists(savePath):
            with open(savePath, 'r', encoding = "UTF-8") as jsonFile:
                fileContents = jsonFile.read()
                if fileContents.strip():
                    existingAccounts = json.loads(fileContents)

        if username in existingAccounts:
            return False

        existingAccounts.update(accountData)

        with open(savePath, 'w', encoding = "UTF-8") as jsonFile:
            json.dump(existingAccounts, jsonFile, indent=4)

        return True

    except Exception as e:
        logger.info(f"Hiba: {e}")
