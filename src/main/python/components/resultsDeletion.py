import json

from src.main.python.components.errorMessage import errorMessage


def resultsDeletion(username, dataPath):
    try:
        with open(dataPath, 'r') as jsonFile:
            fileContents = json.load(jsonFile)

        if username in fileContents:
            fileContents[username]["LearnMedal"] = 1
            fileContents[username]["QuizMedal"] = 0
            fileContents[username]["EmailMedal"] = 0
            fileContents[username]["badge01"] = 1
            fileContents[username]["badge02"] = 0
            fileContents[username]["badge03"] = 0
            fileContents[username]["badge04"] = 0
            fileContents[username]["badge05"] = 0
            fileContents[username]["badge06"] = 0
            fileContents[username]["Score"] = 10000

            with open(dataPath, 'w') as jsonFile:
                json.dump(fileContents, jsonFile, indent=4)

    except Exception as e:
        errorMessage(f"Hiba: {e}")
