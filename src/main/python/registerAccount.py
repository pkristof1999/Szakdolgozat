import welcomeScreen

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt6.QtGui import QPixmap


class RegisterAccountUI(QMainWindow):
    def __init__(self):
        super(RegisterAccountUI, self).__init__()
        loadUi("../resources/ui/registerAccount.ui", self)

        self.backButton = self.findChild(QPushButton, "backButton")
        self.registerButton = self.findChild(QPushButton, "registerButton")
        self.inputUserName = self.findChild(QLineEdit, "inputUserName")
        self.inputUserAge = self.findChild(QLineEdit, "inputUserAge")
        self.inputPwd1 = self.findChild(QLineEdit, "inputPwd1")
        self.inputPwd2 = self.findChild(QLineEdit, "inputPwd2")

        self.welcomeWindow = None

        self.backButtonClick()
        self.registerButtonClick()

    def backButtonClick(self):
        self.backButton.clicked.connect(self.openWelcomeUI)

    def registerButtonClick(self):
        self.registerButton.clicked.connect(self.registerUser)

    def openWelcomeUI(self):
        if not self.welcomeWindow:
            self.welcomeWindow = welcomeScreen.WelcomeUI()
        self.welcomeWindow.show()
        self.hide()

    def registerUser(self):
        pass
