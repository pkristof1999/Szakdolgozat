import loginScreen
import registerAccount

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton

from src.main.python.components.logger import *


class WelcomeUI(QMainWindow):
    def __init__(self):
        super(WelcomeUI, self).__init__()
        loadUi("../resources/ui/welcomeScreen.ui", self)

        self.loginButton = self.findChild(QPushButton, "loginButton")
        self.registerButton = self.findChild(QPushButton, "registerButton")

        self.registerWindow = None
        self.loginWindow = None

        self.loginButton.clicked.connect(self.openLoginUI)
        self.registerButton.clicked.connect(self.openRegisterUI)

    def openLoginUI(self):
        if not self.loginWindow:
            self.loginWindow = loginScreen.LoginScreenUI()
        self.loginWindow.show()
        logger.info("Bejelentkezési képernyő megnyitásra került!")
        self.hide()

    def openRegisterUI(self):
        if not self.registerWindow:
            self.registerWindow = registerAccount.RegisterAccountUI()
        self.registerWindow.show()
        logger.info("Regisztrációs képernyő megnyitásra került!")
        self.hide()
