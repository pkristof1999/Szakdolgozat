import json

from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton

from src.main.python import mainWindow, loginScreen, registerAccount
from src.main.python.components.logger import *
from src.main.python.components.resultsDeletion import resultsDeletion
from src.main.python.infoscreens import areYouSure, aboutWindow
from src.main.python.infoscreens.errorMessage import errorMessage


class WelcomeUI(QMainWindow):
    try:
        def __init__(self, basePath):
            super(WelcomeUI, self).__init__()
            self.basePath = basePath

            loadUi(os.path.join(self.basePath, "src/main/resources/ui/default/defaultWelcomeScreen.ui"), self)
            self.setWindowIcon(QIcon(os.path.join(self.basePath, f"src/main/resources/icon/icon.ico")))

            self.setFixedSize(self.size())

            self.loginButton = self.findChild(QPushButton, "loginButton")
            self.registerButton = self.findChild(QPushButton, "registerButton")
            self.playAsGuestButton = self.findChild(QPushButton, "playAsGuestButton")
            self.aboutButton = self.findChild(QPushButton, "aboutButton")

            self.registerWindow = None
            self.loginWindow = None
            self.questionWindow = None
            self.appMainWindow = None
            self.aboutScreen = None

            self.loginButton.clicked.connect(self.openLoginUI)
            self.registerButton.clicked.connect(self.openRegisterUI)
            self.aboutButton.clicked.connect(self.aboutWindow)

            self.playAsGuestButton.clicked.connect(
                lambda: self.openQuestionWindow("Vendégként nem mentődnek\naz eredmények!\nFolytatja?",
                                                self.handlePlayAsGuest,
                                                "Vendég"
                                                )
            )

        def openQuestionWindow(self, question, handler, username=None):
            self.questionWindow = None
            if not self.questionWindow:
                self.questionWindow = areYouSure.AreYouSureUI(self.basePath, question)

            if username is not None:
                self.questionWindow.finished.connect(lambda result: handler(result, username))
            else:
                self.questionWindow.finished.connect(handler)

            self.questionWindow.show()

        def handlePlayAsGuest(self, result, username):
            if result == "Yes":
                resultsDeletion(username, os.path.join(self.basePath, f"userdata/profiles/guestProfile.json"))
                self.playAsGuest(username)

        def playAsGuest(self, username):
            path = os.path.join(self.basePath, f"userdata/profiles/guestProfile.json")

            try:
                existingAccounts = {}

                if os.path.exists(path):
                    with open(path, 'r', encoding = "UTF-8") as jsonFile:
                        fileContents = jsonFile.read()
                        if fileContents.strip():
                            existingAccounts = json.loads(fileContents)

                existingAccounts[username]["Theme"] = "default"

                with open(path, 'w', encoding = "UTF-8") as jsonFile:
                    json.dump(existingAccounts, jsonFile, indent=4)

            except Exception as e:
                logger.info(f"Hiba: {e}")
                return False

            if not self.appMainWindow:
                self.appMainWindow = mainWindow.MainWindowUI(self.basePath, username)
            self.appMainWindow.show()
            logger.info("Továbblépés a fő felületre.")
            self.hide()

        def openLoginUI(self):
            if not self.loginWindow:
                self.loginWindow = loginScreen.LoginScreenUI(self.basePath)
            self.loginWindow.show()
            logger.info("Bejelentkezési képernyő megnyitásra került!")
            self.hide()

        def openRegisterUI(self):
            if not self.registerWindow:
                self.registerWindow = registerAccount.RegisterAccountUI(self.basePath)
            self.registerWindow.show()
            logger.info("Regisztrációs képernyő megnyitásra került!")
            self.hide()

        def aboutWindow(self):
            if not self.aboutScreen:
                self.aboutScreen = aboutWindow.AboutWindowUI(self, self.basePath)
            self.aboutScreen.show()
            logger.info("Névjegy képernyő megnyitásra került!")
            self.hide()

    except Exception as e:
        errorMessage(e)
