import json
import os.path

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

                    self.loadUserAchievementsComponent(existingAccounts, username)

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
        try:
            pixmap = QPixmap(f"../resources/emblems{pathToBadge}")

            if not os.path.exists(f"../resources/emblems{pathToBadge}"):
                raise Exception("A megadott kép nem található!")

            frameSize = medal.size()
            pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                   QtCore.Qt.TransformationMode.SmoothTransformation)

            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label.setGeometry(medal.rect())
            label.setPixmap(pixmap)

            path, to, badge = pathToBadge.split("/")
            logger.info(f"{badge} sikeresen betöltésre került!")

        except Exception as e:
            logger.error(f"Hiba: {e}")

    def loadUserAchievementsComponent(self, account, username):
        try:
            if account[username]["LearnMedal"] == 0:
                self.badgeLoader(
                    "/learning/Learning_Locked.png", self.learnMedal, self.learnMedalLabel
                )
            elif account[username]["LearnMedal"] == 1:
                self.badgeLoader(
                    "/learning/Learning_Unlocked.png", self.learnMedal, self.learnMedalLabel
                )
            else:
                raise Exception("Hiba a 'LearnMedal' jelvény betöltésekor!")

            # TODO EMAIL

            if account[username]["badge01"] == 0:
                self.badgeLoader(
                    "/learning/Learning_100Percent_Locked.png", self.badge01, self.badge01Label
                )
            elif account[username]["badge01"] == 1:
                self.badgeLoader(
                    "/learning/Learning_100Percent_Unlocked.png", self.badge01, self.badge01Label
                )
            else:
                raise Exception("Hiba a 'badge01' jelvény betöltésekor!")

            if account[username]["badge02"] == 0:
                self.badgeLoader(
                    "/learning/Learning_Fast_Completion_Locked.png", self.badge02, self.badge02Label
                )
            elif account[username]["badge02"] == 1:
                self.badgeLoader(
                    "/learning/Learning_Fast_Completion_Unlocked.png", self.badge02, self.badge02Label
                )
            else:
                raise Exception("Hiba a 'badge02' jelvény betöltésekor!")

            if account[username]["badge03"] == 0:
                self.badgeLoader(
                    "/quiz/Quiz_100Percent_Locked.png", self.badge03, self.badge03Label
                )
            elif account[username]["badge03"] == 1:
                self.badgeLoader(
                    "/quiz/Quiz_100Percent_Unlocked.png", self.badge03, self.badge03Label
                )
            else:
                raise Exception("Hiba a 'badge03' jelvény betöltésekor!")

            if account[username]["badge04"] == 0:
                self.badgeLoader(
                    "/quiz/Quiz_Fast_Completion_Locked.png", self.badge04, self.badge04Label
                )
            elif account[username]["badge04"] == 1:
                self.badgeLoader(
                    "/quiz/Quiz_Fast_Completion_Locked.png", self.badge04, self.badge04Label
                )
            else:
                raise Exception("Hiba a 'badge04' jelvény betöltésekor!")

            if account[username]["badge05"] == 0:
                self.badgeLoader(
                    "/email/Email_100Percent_Locked.png", self.badge05, self.badge05Label
                )
            elif account[username]["badge05"] == 1:
                self.badgeLoader(
                    "/email/Email_100Percent_Unlocked.png", self.badge05, self.badge05Label
                )
            else:
                raise Exception("Hiba a 'badge05' jelvény betöltésekor!")

            if account[username]["badge06"] == 0:
                self.badgeLoader(
                    "/email/Email_Fast_Completion_Locked.png", self.badge06, self.badge06Label
                )
            elif account[username]["badge06"] == 1:
                self.badgeLoader(
                    "/email/Email_Fast_Completion_Unlocked.png", self.badge06, self.badge06Label
                )
            else:
                raise Exception("Hiba a 'badge06' jelvény betöltésekor!")

        except Exception as f:
            logger.error(f"Hiba: {f}")
