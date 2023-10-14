import json

import welcomeScreen
import mainWindow

from PyQt6 import QtCore
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QComboBox, QMessageBox

from src.main.python.components.logger import *
from src.main.python.components.securePwd import checkPassword


class LoginScreenUI(QMainWindow):
    def __init__(self):
        super(LoginScreenUI, self).__init__()
        loadUi("../resources/ui/default/loginScreen.ui", self)

        self.userNameBox = self.findChild(QComboBox, "userNameBox")
        self.inputPwd = self.findChild(QLineEdit, "inputPwd")
        self.backButton = self.findChild(QPushButton, "backButton")
        self.loginButton = self.findChild(QPushButton, "loginButton")

        """Ez csak azért kell ide, mert máshol nem tudtam középre igazítani a QComboBox tartalmát.
           This is here because I couldn't align the QComboBox's content to center elsewhere."""
        self.userNameBox.setEditable(True)
        lineEdit = self.userNameBox.lineEdit()
        lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        lineEdit.setReadOnly(True)

        self.userNameBox.setStyleSheet("""
            * {
                background-color: white;
                border: 2px solid #8f8f91;
                border-radius: 10px;
                color: grey;
                box-shadow: none;
            }
            
            *::drop-down {
                border: none;
                box-shadow: none;
                right: 8px;
            }
            
            *::down-arrow {
                image: url("../resources/pictures/Arrow.png");
                width: 16px;
                height: 16px;
                box-shadow: none;
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

                    if not fileContents.strip():
                        self.userNameBox.addItem("Regisztráljon!")
                    else:
                        existingAccounts = json.loads(fileContents)
                        usernames = list(existingAccounts.keys())
                        self.userNameBox.addItems(usernames)

            else:
                self.userNameBox.addItem("Regisztráljon!")

        except Exception as e:
            print("Hiba: ", e)

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
            print("Hiba: ", e)

        if self.userNameBox.currentText() == "Regisztráljon!":
            logger.error("Sikertelen bejelentkezés!")
            errorDialog = QMessageBox(self)
            errorDialog.setWindowTitle("Hiba!")
            errorMessage = "Nincs regisztrált felhasználó!"
            errorDialog.setIcon(QMessageBox.Icon.Critical)
            errorDialog.setText(errorMessage)
            errorDialog.exec()
        else:
            if checkPassword(inputPassword, storedPassword):
                logger.info("Sikeres bejelentkezés!")
                self.openMainUI(username)
            else:
                logger.error("Sikertelen bejelentkezés!")
                errorDialog = QMessageBox(self)
                errorDialog.setWindowTitle("Hiba!")
                errorMessage = "A megadott jelszó hibás!"
                errorDialog.setIcon(QMessageBox.Icon.Critical)
                errorDialog.setText(errorMessage)
                errorDialog.exec()

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
