from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton

from src.main.python import loginScreen
from src.main.python.components.logger import *
from src.main.python import registerAccount


class RegisterSuccessUI(QMainWindow):
    def __init__(self):
        super(RegisterSuccessUI, self).__init__()
        loadUi("../resources/ui/registerSuccess.ui", self)

        self.toLoginScreenButton = self.findChild(QPushButton, "toLoginScreenButton")
        self.newRegisterButton = self.findChild(QPushButton, "newRegisterButton")

        self.loginWindow = None
        self.registerWindow = None
        self.isLoginClicked = False

        self.toLoginScreenButton.clicked.connect(self.openLoginScreen)
        self.newRegisterButton.clicked.connect(self.showRegisterScreen)

        self.isLoginClickedMethod()

    def openLoginScreen(self):
        if not self.loginWindow:
            self.loginWindow = loginScreen.LoginScreenUI()
        self.loginWindow.show()
        self.isLoginClicked = True
        logger.info("Bejelentkezési képernyő megnyitásra került!")
        self.hide()

    def showRegisterScreen(self):
        self.isLoginClicked = False
        self.hide()

    def isLoginClickedMethod(self):
        return self.isLoginClicked


def loginClicked():
    state = RegisterSuccessUI()
    print(state.isLoginClicked)
    return state.isLoginClicked
