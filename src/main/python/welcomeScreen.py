import loginScreen
import registerAccount

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton

from src.main.python.components.logger import *
from src.main.python.infoscreens import areYouSure


class WelcomeUI(QMainWindow):
    def __init__(self):
        super(WelcomeUI, self).__init__()
        loadUi(f"../resources/ui/default/welcomeScreen.ui", self)

        self.loginButton = self.findChild(QPushButton, "loginButton")
        self.registerButton = self.findChild(QPushButton, "registerButton")
        self.playAsGuestButton = self.findChild(QPushButton, "playAsGuestButton")

        self.registerWindow = None
        self.loginWindow = None
        self.questionWindow = None

        self.loginButton.clicked.connect(self.openLoginUI)
        self.registerButton.clicked.connect(self.openRegisterUI)

        self.playAsGuestButton.clicked.connect(
            lambda: self.openQuestionWindow("Vendégként nem mentődnek az eredmények! Folytatja?",
                                            self.playAsGuest
                                            )
        )

    def openQuestionWindow(self, question, handler, username = None):
        self.questionWindow = None
        if not self.questionWindow:
            self.questionWindow = areYouSure.AreYouSureUI(question)

        if username is not None:
            self.questionWindow.finished.connect(lambda result: handler(result, username))
        else:
            self.questionWindow.finished.connect(handler)

        self.questionWindow.show()

    def openLoginUI(self):
        if not self.loginWindow:
            self.loginWindow = loginScreen.LoginScreenUI()
        self.loginWindow.show()
        logger.info("Bejelentkezési képernyő megnyitásra került!")
        self.close()

    def openRegisterUI(self):
        if not self.registerWindow:
            self.registerWindow = registerAccount.RegisterAccountUI()
        self.registerWindow.show()
        logger.info("Regisztrációs képernyő megnyitásra került!")
        self.close()
