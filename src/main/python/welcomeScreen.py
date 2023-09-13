import registerAccount
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton


class WelcomeUI(QMainWindow):
    def __init__(self):
        super(WelcomeUI, self).__init__()
        self.thisWindow = WelcomeUI

        loadUi("../resources/ui/welcomeScreen.ui", self)

        self.loginButton = self.findChild(QPushButton, "loginButton")
        """self.loginWindow = loginAccount.LoginAccountUI"""

        self.registerButton = self.findChild(QPushButton, "registerButton")
        self.registerWindow = registerAccount.RegisterAccountUI()

    """def loginButtonClick(self):
        self.loginButton.clicked.connect(self.openLoginUI)"""

    def registerButtonClick(self):
        self.registerButton.clicked.connect(self.openRegisterUI)

    """def openLoginUI(self):
        self.loginWindow.show()
        self.thisWindow.hide(self)"""

    def openRegisterUI(self):
        self.registerWindow.show()
        self.thisWindow.hide(self)
