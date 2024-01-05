from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QSizePolicy

from src.main.python import mainWindow, loginScreen, registerAccount
from src.main.python.components.logger import *
from src.main.python.components.resultsDeletion import resultsDeletion
from src.main.python.infoscreens import areYouSure


class WelcomeUI(QMainWindow):
    def __init__(self):
        super(WelcomeUI, self).__init__()
        loadUi(f"../resources/ui/default/welcomeScreen.ui", self)
        self.setWindowIcon(QIcon("../resources/icon/icon.ico"))

        self.setFixedSize(self.size())

        self.loginButton = self.findChild(QPushButton, "loginButton")
        self.registerButton = self.findChild(QPushButton, "registerButton")
        self.playAsGuestButton = self.findChild(QPushButton, "playAsGuestButton")

        self.registerWindow = None
        self.loginWindow = None
        self.questionWindow = None
        self.appMainWindow = None

        self.loginButton.clicked.connect(self.openLoginUI)
        self.registerButton.clicked.connect(self.openRegisterUI)

        self.playAsGuestButton.clicked.connect(
            lambda: self.openQuestionWindow("Vendégként nem mentődnek\naz eredmények!\nFolytatja?",
                                            self.handlePlayAsGuest,
                                            "Vendég"
                                            )
        )

    def openQuestionWindow(self, question, handler, username=None):
        self.questionWindow = None
        if not self.questionWindow:
            self.questionWindow = areYouSure.AreYouSureUI(question)

        if username is not None:
            self.questionWindow.finished.connect(lambda result: handler(result, username))
        else:
            self.questionWindow.finished.connect(handler)

        self.questionWindow.show()

    def handlePlayAsGuest(self, result, username):
        if result == "Yes":
            resultsDeletion(username, "../../../userdata/profiles/guestProfile.json")
            self.playAsGuest(username)

    def playAsGuest(self, username):
        if not self.appMainWindow:
            self.appMainWindow = mainWindow.MainWindowUI(username)
        self.appMainWindow.show()
        logger.info("Továbblépés a fő felületre.")
        self.hide()

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
