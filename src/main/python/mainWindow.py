import json

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QMainWindow
from PyQt6.uic import loadUi

from src.main.python import resultsWindow
from src.main.python import settingsWindow
from src.main.python import guestSettingsWindow
from src.main.python import loginScreen
from src.main.python.components.logger import *
from src.main.python.components.errorMessage import errorMessage
from src.main.python.infoscreens import gameModeInfo


class MainWindowUI(QMainWindow):
    def __init__(self, username):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            super(MainWindowUI, self).__init__()

            self.username = username
            default = "default"

            loadUi(f"../resources/ui/{default}/mainWindow.ui", self)

            self.profilePicture = self.findChild(QFrame, "profilePicture")
            self.usernameLabel = self.findChild(QLabel, "usernameLabel")
            self.resultsButton = self.findChild(QPushButton, "resultsButton")
            self.settingsButton = self.findChild(QPushButton, "settingsButton")
            self.logOutButton = self.findChild(QPushButton, "logOutButton")
            self.exitButton = self.findChild(QPushButton, "exitButton")

            self.usernameLabel.setText(f"Üdv, {username}!")

            self.learningGameButton = self.findChild(QPushButton, "learningGameButton")
            self.quizGameButton = self.findChild(QPushButton, "quizGameButton")
            self.emailGameButton = self.findChild(QPushButton, "emailGameButton")

            self.resultsScreen = None
            self.settingsScreen = None
            self.guestSettingsScreen = None
            self.loginWindow = None
            self.infoWindow = None

            self.resultsButton.clicked.connect(self.openResults)
            self.settingsButton.clicked.connect(lambda: self.openSettings(username))
            self.logOutButton.clicked.connect(self.logOut)
            self.exitButton.clicked.connect(self.close)

            self.learningGameInfo = """Ide lesz majd a leírás"""
            self.quizGameInfo = """Ide lesz majd a leírás"""
            self.emailGameInfo = """Ide lesz majd a leírás"""

            self.learningGameButton.clicked.connect(
                lambda: self.openQuestionWindow(self.learningGameInfo,
                                                self.handleLearningGameOpen,
                                                username
                                              )
            )

            self.quizGameButton.clicked.connect(
                lambda: self.openQuestionWindow(self.quizGameInfo,
                                                self.handleQuizGameOpen,
                                                username
                                                )
            )

            self.emailGameButton.clicked.connect(
                lambda: self.openQuestionWindow(self.emailGameInfo,
                                                self.handleEmailGameOpen,
                                                username
                                                )
            )

            self.label = QLabel(self.profilePicture)

            self.imagePath = self.getImagePath(username)
            self.loadImage(self.imagePath)

        except Exception as e:
            errorMessage(e)
            self.close()

    def getImagePath(self, username):
        if username != "Vendég":
            dataPath = "../../../userdata/profiles/profiles.json"
        else:
            dataPath = "../../../userdata/profiles/guestProfile.json"

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()
                    existingAccounts = json.loads(fileContents)
                    if "avatar" in existingAccounts[username]["ProfilePicturePath"]:
                        return "../../" + existingAccounts[username]["ProfilePicturePath"]
                    else:
                        return existingAccounts[username]["ProfilePicturePath"]

        except Exception as e:
            errorMessage(f"Hiba: {e}")

    def loadImage(self, imagePath):
        try:
            pixmap = QPixmap(imagePath)

            if not os.path.exists(imagePath):
                raise Exception("A megadott kép nem található!")

            frameSize = self.profilePicture.size()
            pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                   QtCore.Qt.TransformationMode.SmoothTransformation)

            self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.label.setGeometry(self.profilePicture.rect())
            self.label.setPixmap(pixmap)

        except Exception as e:
            logger.error(f"Hiba: {e}")

    def openResults(self):
        if not self.resultsScreen:
            self.resultsScreen = resultsWindow.ResultsUI(self, self.username)
        self.resultsScreen.show()
        self.settingsScreen = None

    def openSettings(self, username):
        if username == "Vendég":
            if not self.guestSettingsScreen:
                self.guestSettingsScreen = guestSettingsWindow.GuestSettingsWindowUI(self, username)
            self.guestSettingsScreen.show()
            self.guestSettingsScreen = None
        else:
            if not self.settingsScreen:
                self.settingsScreen = settingsWindow.SettingsWindowUI(self, username)
            self.settingsScreen.show()
            self.settingsScreen = None

    def openQuestionWindow(self, info, handler, username = None):
        self.infoWindow = None
        if not self.infoWindow:
            self.infoWindow = gameModeInfo.GameModeInfoUI(info, "default")

        if username is not None:
            self.infoWindow.finished.connect(lambda result: handler(result, username))
        else:
            self.infoWindow.finished.connect(handler)

        self.infoWindow.show()

    def handleLearningGameOpen(self, result, username):
        if result == "Yes":
            self.openLearningGame(username)

    def handleQuizGameOpen(self, result, username):
        if result == "Yes":
            self.openQuizGame(username)

    def handleEmailGameOpen(self, result, username):
        if result == "Yes":
            self.openEmailGame(username)

    def openLearningGame(self, username):
        errorMessage("openLearningGame")

    def openQuizGame(self, username):
        errorMessage("openQuizGame")

    def openEmailGame(self, username):
        errorMessage("openEmailGame")

    def logOut(self):
        if not self.loginWindow:
            self.loginWindow = loginScreen.LoginScreenUI()
        self.loginWindow.show()
        logger.info("Sikeres kijelentkezés!")
        logger.info("Bejelentkezési képernyő megnyitásra került!")
        self.close()

    def refreshWindow(self):
        self.imagePath = self.getImagePath(self.username)
        self.loadImage(self.imagePath)
