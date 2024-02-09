import json

from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QComboBox

from src.main.python import mainWindow, welcomeScreen
from src.main.python.components.logger import *
from src.main.python.components import clickableComboBox
from src.main.python.components.securePwd import checkPassword
from src.main.python.infoscreens.errorMessage import errorMessage


class LoginScreenUI(QMainWindow):
    def __init__(self):
        super(LoginScreenUI, self).__init__()
        loadUi("../resources/ui/default/defaultLoginScreen.ui", self)
        self.setWindowIcon(QIcon("../resources/icon/icon.ico"))

        self.setFixedSize(self.size())

        self.userNameBox = self.findChild(QComboBox, "userNameBox")
        self.inputPwd = self.findChild(QLineEdit, "inputPwd")
        self.backButton = self.findChild(QPushButton, "backButton")
        self.loginButton = self.findChild(QPushButton, "loginButton")

        """Ez csak azért kell ide, mert máshol nem tudtam középre igazítani a QComboBox tartalmát.
           This is here because I couldn't align the QComboBox's content to center elsewhere."""
        clickableLineEdit = clickableComboBox.ClickableLineEdit(self.userNameBox)

        self.userNameBox.setLineEdit(clickableLineEdit)
        clickableLineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        clickableLineEdit.setReadOnly(True)

        self.userNameBox.setStyleSheet("""
            * {
                background-color: white;
                border: 2px solid #8f8f91;
                border-radius: 10px;
                color: grey;
            }
            
            *::drop-down {
                border: thin solid grey;
                border-radius: 0px;
                right: 8px;
            }
            
            *::down-arrow {
                image: url("../resources/pictures/Arrow.png");
                width: 16px;
                height: 16px;
            }""")

        self.welcomeWindow = None
        self.appMainWindow = None
        self.loginSuccess = False

        self.backButton.clicked.connect(self.openWelcomeUI)
        self.loginButton.clicked.connect(self.authenticateUser)

        self.loadUserNames()

    def loadUserNames(self):
        dataPath = "../../../userdata/profiles/profiles.json"

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()

                    if not fileContents.strip() or fileContents.strip() == "{}":
                        self.userNameBox.addItem("Regisztráljon!")
                    else:
                        existingAccounts = json.loads(fileContents)
                        usernames = list(existingAccounts.keys())
                        self.userNameBox.addItems(usernames)

            else:
                self.userNameBox.addItem("Regisztráljon!")

        except Exception as e:
            errorMessage(f"Hiba: {e}")

    def authenticateUser(self):
        dataPath = "../../../userdata/profiles/profiles.json"

        username = self.userNameBox.currentText()
        inputPassword = self.inputPwd.text().strip()

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()
                    existingAccounts = json.loads(fileContents)
                    storedPassword = existingAccounts[username]["Password"]

        except Exception as e:
            errorMessage(f"Hiba: {e}")

        if self.userNameBox.currentText() == "Regisztráljon!":
            errorMessage("Nincs regisztrált felhasználó!")
        else:
            if checkPassword(inputPassword, storedPassword):
                logger.info("Sikeres bejelentkezés!")
                self.openMainUI(username)
            else:
                errorMessage("A megadott jelszó hibás!")

    def openMainUI(self, username):
        if not self.appMainWindow:
            self.appMainWindow = mainWindow.MainWindowUI(username)
        self.appMainWindow.show()
        logger.info("Továbblépés a fő felületre.")
        self.hide()

    def openWelcomeUI(self):
        if not self.welcomeWindow:
            self.welcomeWindow = welcomeScreen.WelcomeUI()
        self.welcomeWindow.show()
        logger.info("Visszalépés az indítóképernyőre.")
        self.hide()
