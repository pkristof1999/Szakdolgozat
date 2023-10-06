import sys

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication

from src.main.python import loginScreen


class MainWindowUI(QMainWindow):
    def __init__(self):
        super(MainWindowUI, self).__init__()
        loadUi("../resources/ui/mainWindow.ui", self)

        self.profileButton = self.findChild(QPushButton, "profileButton")
        self.resultsButton = self.findChild(QPushButton, "resultsButton")
        self.settingsButton = self.findChild(QPushButton, "settingsButton")
        self.logOutButton = self.findChild(QPushButton, "logOutButton")
        self.exitButton = self.findChild(QPushButton, "exitButton")

        self.learningGameButton = self.findChild(QPushButton, "learningGameButton")
        self.quizGameButton = self.findChild(QPushButton, "quizGameButton")
        self.emailGameButton = self.findChild(QPushButton, "emailGameButton")

        self.loginWindow = None

        self.logOutButton.clicked.connect(self.logOut)
        self.exitButton.clicked.connect(self.exitApp)

    def logOut(self):
        if not self.loginWindow:
            self.loginWindow = loginScreen.LoginScreenUI()
        self.loginWindow.show()
        # logger.info("Bejelentkezési képernyő megnyitásra került!")
        self.close()

    def exitApp(self):
        exit()
