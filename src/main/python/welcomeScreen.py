import json

import mainWindow
import loginScreen
import registerAccount

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton

from src.main.python.components.logger import *
from src.main.python.infoscreens import areYouSure
from src.main.python.components.errorMessage import errorMessage


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
            self.resultsDeletion(username)
            self.playAsGuest(username)

    def playAsGuest(self, username):
        if not self.appMainWindow:
            self.appMainWindow = mainWindow.MainWindowUI(username)
        self.appMainWindow.show()
        logger.info("Továbblépés a fő felületre.")
        self.close()

    def resultsDeletion(self, username):
        dataPath = "../../../userdata/profiles/guestProfile.json"

        try:
            with open(dataPath, 'r') as jsonFile:
                fileContents = json.load(jsonFile)

            if username in fileContents:
                fileContents[username]["LearnMedal"] = 1
                fileContents[username]["QuizMedal"] = 1
                fileContents[username]["EmailMedal"] = 1
                fileContents[username]["badge01"] = 1
                fileContents[username]["badge02"] = 1
                fileContents[username]["badge03"] = 1
                fileContents[username]["badge04"] = 1
                fileContents[username]["badge05"] = 1
                fileContents[username]["badge06"] = 1
                fileContents[username]["Score"] = 2000
                fileContents[username]["Theme"] = "default"

                with open(dataPath, 'w') as jsonFile:
                    json.dump(fileContents, jsonFile, indent=4)

        except Exception as e:
            errorMessage(f"Hiba: {e}")

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
