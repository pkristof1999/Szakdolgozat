import json
import time
import random
import threading

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QPushButton, QMainWindow, QButtonGroup, QFrame
from PyQt6.uic import loadUi

from src.main.python.components.logger import *
from src.main.python.infoscreens import resultsScreen
from src.main.python.infoscreens.errorMessage import errorMessage


class EmailWindowUI(QMainWindow):
    def __init__(self, username, parent):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            self.username = username
            default = "default"

            super(EmailWindowUI, self).__init__()
            self.setWindowIcon(QIcon("../resources/icon/icon.ico"))
            loadUi(f"../resources/ui/{default}/emailWindow.ui", self)

            self.setFixedSize(self.size())

            self.parent = parent

            self.email1Button = self.findChild(QPushButton, "email1Button")
            self.email2Button = self.findChild(QPushButton, "email2Button")
            self.email3Button = self.findChild(QPushButton, "email3Button")
            self.email4Button = self.findChild(QPushButton, "email4Button")
            self.email5Button = self.findChild(QPushButton, "email5Button")
            self.email6Button = self.findChild(QPushButton, "email6Button")
            self.email7Button = self.findChild(QPushButton, "email7Button")
            self.email8Button = self.findChild(QPushButton, "email8Button")
            self.email9Button = self.findChild(QPushButton, "email9Button")
            self.email10Button = self.findChild(QPushButton, "email10Button")
            self.maliciousButton = self.findChild(QPushButton, "maliciousButton")
            self.genuineButton = self.findChild(QPushButton, "genuineButton")
            self.backButton = self.findChild(QPushButton, "backButton")
            self.checkButton = self.findChild(QPushButton, "checkButton")
            self.emailFrame = self.findChild(QFrame, "emailFrame")

            self.emailBank = []
            self.emailIndex = 0
            self.previousEmails = []

            self.backButton.clicked.connect(self.closeEmailWindow)

            self.closeEvent = lambda event: parent.exitWindow(event)

            self.loadSubjects()

        except Exception as e:
            errorMessage(e)
            self.hide()

    def loadEmailsIntoArray(self):
        try:
            with open("../resources/emaildata/emaildata.json", "r") as jsonFile:
                emailBank = json.load(jsonFile)

            shuffledEmails = list(emailBank.values())
            random.shuffle(shuffledEmails)

            return shuffledEmails

        except Exception as e:
            errorMessage(e)

    def loadSubjects(self):
        self.emailBank = self.loadEmailsIntoArray()

        for i in range(10):
            buttonName = f"email{i + 1}Button"
            button = getattr(self, buttonName, None)

            button.setText(self.emailBank[i]["subject"])

    def closeEmailWindow(self):
        self.hide()
        self.parent.show()
