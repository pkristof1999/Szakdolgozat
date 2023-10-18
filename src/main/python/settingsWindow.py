from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QFrame, QPushButton, QComboBox


class SettingsWindowUI(QMainWindow):
    def __init__(self, parent):
        super(SettingsWindowUI, self).__init__()
        loadUi("../resources/ui/default/settingsWindow.ui", self)

        self.parent = parent

        self.profilePicture = self.findChild(QFrame, "profilePicture")
        self.changeProfilePictureButton = self.findChild(QPushButton, "changeProfilePictureButton")
        self.deleteProfilePictureButton = self.findChild(QPushButton, "deleteProfilePictureButton")
        self.changeUserAgeButton = self.findChild(QPushButton, "changeUserAgeButton")
        self.changePasswordButton = self.findChild(QPushButton, "changePasswordButton")
        self.restoreDefaultResultsButton = self.findChild(QPushButton, "restoreDefaultResultsButton")
        self.deleteUserProfileButton = self.findChild(QPushButton, "deleteUserProfileButton")
        self.changeTheme = self.findChild(QComboBox, "changeTheme")
        self.closeButton = self.findChild(QPushButton, "closeButton")

        self.closeButton.clicked.connect(self.close())
