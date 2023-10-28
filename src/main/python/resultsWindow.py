import json

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QFrame, QPushButton, QLabel

from src.main.python.components.logger import *


class ResultsUI(QMainWindow):
    def __init__(self, parent, username):
        super(ResultsUI, self).__init__()
        loadUi(f"../resources/ui/default/resultsWindow.ui", self)

        self.parent = parent

        self.learnMedal = self.findChild(QFrame, "learnMedal")
        self.quizMedal = self.findChild(QFrame, "quizMedal")
        self.emailMedal = self.findChild(QFrame, "emailMedal")
        self.badge01 = self.findChild(QFrame, "badge01")
        self.badge02 = self.findChild(QFrame, "badge02")
        self.badge03 = self.findChild(QFrame, "badge03")
        self.badge04 = self.findChild(QFrame, "badge04")
        self.badge05 = self.findChild(QFrame, "badge05")
        self.badge06 = self.findChild(QFrame, "badge06")
        self.userScore = self.findChild(QLabel, "userScore")
        self.backButton = self.findChild(QPushButton, "backButton")

        self.userScore.setText(f"{username} felhasználó pontszáma: {self.getUserScore(username)}.")

        self.backButton.clicked.connect(self.close)

    def getUserScore(self, username):
        dataPath = "../../../userdata/profiles/profiles.json"
        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()
                    existingAccounts = json.loads(fileContents)
                    return existingAccounts[username]["Score"]

        except Exception as e:
            logger.error(f"Hiba: {e}")
