import welcomeScreen

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton


class LoginScreenUI(QMainWindow):
    def __init__(self):
        super(LoginScreenUI, self).__init__()
        loadUi("../resources/ui/loginScreen.ui", self)

        self.backButton = self.findChild(QPushButton, "backButton")
        self.welcomeWindow = None

        self.backButtonClick()

    def backButtonClick(self):
        self.backButton.clicked.connect(self.openWelcomeUI)

    def openWelcomeUI(self):
        if not self.welcomeWindow:
            self.welcomeWindow = welcomeScreen.WelcomeUI()
        self.welcomeWindow.show()
        self.hide()
