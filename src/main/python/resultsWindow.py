import json

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
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

        self.learnMedalLabel = QLabel(self.learnMedal)
        self.quizMedalLabel = QLabel(self.quizMedal)
        self.emailMedalLabel = QLabel(self.emailMedal)
        self.badge01Label = QLabel(self.badge01)
        self.badge02Label = QLabel(self.badge02)
        self.badge03Label = QLabel(self.badge03)
        self.badge04Label = QLabel(self.badge04)
        self.badge05Label = QLabel(self.badge05)
        self.badge06Label = QLabel(self.badge06)

        self.userScore.setText(f"{username} felhasználó pontszáma: {self.getUserScore(username)}.")

        self.backButton.clicked.connect(self.close)

        self.loadUserAchievements(username)

    """def loadDefaultImage(self):
        pixmap = QPixmap("../resources/pictures/userDefault.png")

        frameSize = self.profilePicture.size()
        pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                               QtCore.Qt.TransformationMode.SmoothTransformation)

        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(self.profilePicture.rect())
        self.label.setPixmap(pixmap)
        logger.info("Alap profilkép betöltésre került!")
        "Teszt Elek": {
        "UserAge": 30,
        "Password": "JDJiJDEyJHJKdXRlUFU2ZnhDL1V1Q2RGR2F6bWVwcDRwaGxsVm9MMVpneVFwU2hwdTFZOXR4eXViVy8u",
        "ProfilePicturePath": "../resources/pictures/userDefault.png",
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
        "Theme": "default"""

    def loadUserAchievements(self, username):
        if username != "Vendég":
            dataPath = "../../../userdata/profiles/profiles.json"
        else:
            dataPath = "../../../userdata/profiles/guestProfile.json"
        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()
                    existingAccounts = json.loads(fileContents)

                    if existingAccounts[username]["LearnMedal"] == 0:
                        self.badgeLoader(
                            "/learning/Learning_Locked.png", self.learnMedal, self.learnMedalLabel
                        )
                    elif existingAccounts[username]["LearnMedal"] == 1:
                        self.badgeLoader(
                            "/learning/Learning_Unlocked.png", self.learnMedal, self.learnMedalLabel
                        )
                    else:
                        raise Exception("Hiba a 'LearnMedal' jelvény betöltésekor!")

                    #TODO EMAIL
                    #TODO QUIZ

                    if existingAccounts[username]["badge01"] == 0:
                        self.badgeLoader(
                            "/learning/Learning_100Percent_Locked.png", self.badge01, self.badge01Label
                        )
                    elif existingAccounts[username]["badge01"] == 1:
                        self.badgeLoader(
                            "/learning/Learning_100Percent_Unlocked.png", self.badge01, self.badge01Label
                        )
                    else:
                        raise Exception("Hiba a 'badge01' jelvény betöltésekor!")

                    if existingAccounts[username]["badge02"] == 0:
                        self.badgeLoader(
                            "/learning/Learning_Fast_Completion_Locked.png", self.badge02, self.badge02Label
                        )
                    elif existingAccounts[username]["badge02"] == 1:
                        self.badgeLoader(
                            "/learning/Learning_Fast_Completion_Unlocked.png", self.badge02, self.badge02Label
                        )
                    else:
                        raise Exception("Hiba a 'badge02' jelvény betöltésekor!")

        except Exception as e:
            logger.error(f"Hiba: {e}")

    def getUserScore(self, username):
        if username != "Vendég":
            dataPath = "../../../userdata/profiles/profiles.json"
        else:
            dataPath = "../../../userdata/profiles/guestProfile.json"
        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()
                    existingAccounts = json.loads(fileContents)
                    return existingAccounts[username]["Score"]

        except Exception as e:
            logger.error(f"Hiba: {e}")

    def badgeLoader(self, pathToBadge, medal, label):
        pixmap = QPixmap(f"../resources/emblems{pathToBadge}")

        frameSize = medal.size()
        pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                               QtCore.Qt.TransformationMode.SmoothTransformation)

        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setGeometry(medal.rect())
        label.setPixmap(pixmap)
        logger.info(f"{medal} sikeresen betöltésre került!")
