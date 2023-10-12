from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton

from src.main.python import loginScreen
from src.main.python import registerAccount
from src.main.python.components.logger import *


class RegisterSuccessUI(QMainWindow):
    def __init__(self):
        super(RegisterSuccessUI, self).__init__()
        loadUi("../resources/ui/default/registerSuccess.ui", self)

        self.toLoginScreenButton = self.findChild(QPushButton, "toLoginScreenButton")
        self.newRegisterButton = self.findChild(QPushButton, "newRegisterButton")

        self.loginWindow = None
        self.registerWindow = None

        self.toLoginScreenButton.clicked.connect(self.openLoginScreen)
        self.newRegisterButton.clicked.connect(self.showRegisterScreen)

    def openLoginScreen(self):
        if not self.loginWindow:
            self.loginWindow = loginScreen.LoginScreenUI()
        self.loginWindow.show()
        logger.info("Bejelentkezési képernyő megnyitásra került!")
        self.hide()

    def showRegisterScreen(self):
        if not self.registerWindow:
            self.registerWindow = registerAccount.RegisterAccountUI()
        self.registerWindow.show()
        self.hide()
