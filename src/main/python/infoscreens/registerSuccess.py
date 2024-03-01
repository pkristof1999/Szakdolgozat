from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton

from src.main.python import loginScreen
from src.main.python import registerAccount
from src.main.python.components.logger import *


class RegisterSuccessUI(QMainWindow):
    def __init__(self, basePath):
        super(RegisterSuccessUI, self).__init__()

        self.basePath = basePath

        loadUi(os.path.join(self.basePath, "src/main/resources/ui/default/defaultRegisterSuccess.ui"), self)
        self.setWindowIcon(QIcon(os.path.join(self.basePath, "src/main/resources/icon/icon.ico")))

        self.setFixedSize(self.size())

        self.toLoginScreenButton = self.findChild(QPushButton, "toLoginScreenButton")
        self.newRegisterButton = self.findChild(QPushButton, "newRegisterButton")

        self.loginWindow = None
        self.registerWindow = None

        self.toLoginScreenButton.clicked.connect(self.openLoginScreen)
        self.newRegisterButton.clicked.connect(self.showRegisterScreen)

    def openLoginScreen(self):
        if not self.loginWindow:
            self.loginWindow = loginScreen.LoginScreenUI(self.basePath)
        self.loginWindow.show()
        logger.info("Bejelentkezési képernyő megnyitásra került!")
        self.hide()

    def showRegisterScreen(self):
        if not self.registerWindow:
            self.registerWindow = registerAccount.RegisterAccountUI(self.basePath)
        self.registerWindow.show()
        self.hide()
