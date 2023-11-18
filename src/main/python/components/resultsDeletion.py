import json

from src.main.python.components.errorMessage import errorMessage


def resultsDeletion(username, dataPath):
    try:
        with open(dataPath, 'r') as jsonFile:
            fileContents = json.load(jsonFile)

        if username in fileContents:
            fileContents[username]["LearnMedal"] = 1
            fileContents[username]["QuizMedal"] = 1
            fileContents[username]["EmailMedal"] = 1
            fileContents[username]["badge01"] = 1
            fileContents[username]["badge02"] = 1
            fileContents[username]["badge03"] = 1
            fileContents[username]["badge04"] = 1
            fileContents[username]["badge05"] = 1
            fileContents[username]["badge06"] = 1
            fileContents[username]["Score"] = 20000

            with open(dataPath, 'w') as jsonFile:
                json.dump(fileContents, jsonFile, indent=4)

    except Exception as e:
        errorMessage(f"Hiba: {e}")
