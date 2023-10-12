import os
import json

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLineEdit, QFrame, QFileDialog, QLabel, QMessageBox, QPushButton, QMainWindow
from PyQt6.uic import loadUi

from src.main.python import loginScreen
from src.main.python.components.logger import *


class MainWindowUI(QMainWindow):
    def __init__(self, username):
        super(MainWindowUI, self).__init__()
        loadUi("../resources/ui/mainWindow.ui", self)

        self.username = username

        self.profilePicture = self.findChild(QFrame, "profilePicture")
        self.profileButton = self.findChild(QPushButton, "profileButton")
        self.resultsButton = self.findChild(QPushButton, "resultsButton")
        self.settingsButton = self.findChild(QPushButton, "settingsButton")
        self.logOutButton = self.findChild(QPushButton, "logOutButton")
        self.exitButton = self.findChild(QPushButton, "exitButton")

        self.learningGameButton = self.findChild(QPushButton, "learningGameButton")
        self.quizGameButton = self.findChild(QPushButton, "quizGameButton")
        self.emailGameButton = self.findChild(QPushButton, "emailGameButton")

        self.loginWindow = None

        self.logOutButton.clicked.connect(self.logOut)
        self.exitButton.clicked.connect(self.exitApp)

        self.imagePath = self.getImagePath(username)
        self.label = QLabel(self.profilePicture)

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
            print("Hiba: ", e)

    def loadImage(self, imagePath):
        print(imagePath)
        pixmap = QPixmap(imagePath)

        frameSize = self.profilePicture.size()
        pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                               QtCore.Qt.TransformationMode.SmoothTransformation)

        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(self.profilePicture.rect())
        self.label.setPixmap(pixmap)

    def logOut(self):
        if not self.loginWindow:
            self.loginWindow = loginScreen.LoginScreenUI()
        self.loginWindow.show()
        logger.info("Sikeres kijelentkezés!")
        logger.info("Bejelentkezési képernyő megnyitásra került!")
        self.hide()

    def exitApp(self):
        exit()
