import json

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QPushButton, QMainWindow, QComboBox, QLabel
from PyQt6.uic import loadUi

from src.main.python.components.logger import *


class SettingsWindowUI(QMainWindow):
    def __init__(self, parent, username):
        super(SettingsWindowUI, self).__init__()
        loadUi("../resources/ui/default/settingsWindow.ui", self)

        self.parent = parent
        self.username = username

        self.profilePicture = self.findChild(QFrame, "profilePicture")
        self.changeProfilePictureButton = self.findChild(QPushButton, "changeProfilePictureButton")
        self.deleteProfilePictureButton = self.findChild(QPushButton, "deleteProfilePictureButton")
        self.changeUserAgeButton = self.findChild(QPushButton, "changeUserAgeButton")
        self.changePasswordButton = self.findChild(QPushButton, "changePasswordButton")
        self.restoreDefaultResultsButton = self.findChild(QPushButton, "restoreDefaultResultsButton")
        self.deleteUserProfileButton = self.findChild(QPushButton, "deleteUserProfileButton")
        self.changeTheme = self.findChild(QComboBox, "changeTheme")
        self.abortButton = self.findChild(QPushButton, "abortButton")
        self.saveAndCloseButton = self.findChild(QPushButton, "saveAndCloseButton")

        self.abortButton.clicked.connect(self.abortAndCloseSettings)
        self.saveAndCloseButton.clicked.connect(self.saveAndCloseSettings)

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
            logger.info(f"Hiba: {e}")

    def loadImage(self, imagePath):
        pixmap = QPixmap(imagePath)

        frameSize = self.profilePicture.size()
        pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                               QtCore.Qt.TransformationMode.SmoothTransformation)

        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(self.profilePicture.rect())
        self.label.setPixmap(pixmap)

    def abortAndCloseSettings(self):
        self.close()

    def saveAndCloseSettings(self):
        self.close()
        self.parent.repaint()
        # TODO
