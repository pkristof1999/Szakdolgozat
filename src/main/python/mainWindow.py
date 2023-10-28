import json

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QMainWindow, QMessageBox
from PyQt6.uic import loadUi

from src.main.python import settingsWindow
from src.main.python import loginScreen
from src.main.python.components.logger import *
from src.main.python.components.errorMessage import errorMessage


class MainWindowUI(QMainWindow):
    def __init__(self, username):
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

        self.loginWindow = None
        self.settingsWindow = None

        self.settingsButton.clicked.connect(self.openSettings)
        self.logOutButton.clicked.connect(self.logOut)
        self.exitButton.clicked.connect(self.exitApp)

        self.label = QLabel(self.profilePicture)

        self.imagePath = self.getImagePath(username)
        self.loadImage(self.imagePath)

    def getImagePath(self, username):
        dataPath = "../../../userdata/profiles/profiles.json"

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
        pixmap = QPixmap(imagePath)

        frameSize = self.profilePicture.size()
        pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                               QtCore.Qt.TransformationMode.SmoothTransformation)

        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(self.profilePicture.rect())
        self.label.setPixmap(pixmap)

    def openSettings(self):
        if not self.settingsWindow:
            self.settingsWindow = settingsWindow.SettingsWindowUI(self, self.username)
        self.settingsWindow.show()
        self.settingsWindow = None

    def logOut(self):
        if not self.loginWindow:
            self.loginWindow = loginScreen.LoginScreenUI()
        self.loginWindow.show()
        logger.info("Sikeres kijelentkezés!")
        logger.info("Bejelentkezési képernyő megnyitásra került!")
        self.hide()

    def exitApp(self):
        exit()

    def refreshWindow(self):
        self.imagePath = self.getImagePath(self.username)
        self.loadImage(self.imagePath)
