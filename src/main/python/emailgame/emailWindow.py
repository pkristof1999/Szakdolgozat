import json
import time
import random
import threading

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QLine
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QLabel, QPushButton, QMainWindow, QButtonGroup, QFrame, QLineEdit
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
            self.horizontalLine = self.findChild(QFrame, "horizontalLine")

            self.maliciousButtonHiddenState = False
            self.genuineButtonHiddenState = False

            self.email1ID = ""
            self.email2ID = ""
            self.email3ID = ""
            self.email4ID = ""
            self.email5ID = ""
            self.email6ID = ""
            self.email7ID = ""
            self.email8ID = ""
            self.email9ID = ""
            self.email10ID = ""

            self.selectedEmailID = ""

            self.email1Path = ""
            self.email2Path = ""
            self.email3Path = ""
            self.email4Path = ""
            self.email5Path = ""
            self.email6Path = ""
            self.email7Path = ""
            self.email8Path = ""
            self.email9Path = ""
            self.email10Path = ""

            self.email1IsMalicious = False
            self.email2IsMalicious = False
            self.email3IsMalicious = False
            self.email4IsMalicious = False
            self.email5IsMalicious = False
            self.email6IsMalicious = False
            self.email7IsMalicious = False
            self.email8IsMalicious = False
            self.email9IsMalicious = False
            self.email10IsMalicious = False

            self.label = QLabel(self.emailFrame)

            self.emailBank = []
            self.emailIndex = 0
            self.previousEmails = []

            self.backButton.clicked.connect(self.closeEmailWindow)

            self.closeEvent = lambda event: parent.exitWindow(event)

            self.loadSubjects()
            self.loadDefaults()

            self.email1Button.clicked.connect(lambda: self.loadNextEmail(self.email1ID, self.email1Path))
            self.email2Button.clicked.connect(lambda: self.loadNextEmail(self.email2ID, self.email2Path))
            self.email3Button.clicked.connect(lambda: self.loadNextEmail(self.email3ID, self.email3Path))
            self.email4Button.clicked.connect(lambda: self.loadNextEmail(self.email4ID, self.email4Path))
            self.email5Button.clicked.connect(lambda: self.loadNextEmail(self.email5ID, self.email5Path))
            self.email6Button.clicked.connect(lambda: self.loadNextEmail(self.email6ID, self.email6Path))
            self.email7Button.clicked.connect(lambda: self.loadNextEmail(self.email7ID, self.email7Path))
            self.email8Button.clicked.connect(lambda: self.loadNextEmail(self.email8ID, self.email8Path))
            self.email9Button.clicked.connect(lambda: self.loadNextEmail(self.email9ID, self.email9Path))
            self.email10Button.clicked.connect(lambda: self.loadNextEmail(self.email10ID, self.email10Path))

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
            buttonID = f"email{i + 1}ID"
            emailPath = f"email{i + 1}Path"
            emailIsMalicious = f"email{i + 1}IsMalicious"
            button = getattr(self, buttonName, None)

            button.setText(self.emailBank[i]["subject"])
            setattr(self, buttonID, self.emailBank[i]["ID"])
            setattr(self, emailPath, self.emailBank[i]["pathToEmail"])
            if self.emailBank[i]["isMalicious"]:
                setattr(self, emailIsMalicious, True)

    def loadDefaults(self):
        self.buttonBehaviour("hidden")
        self.loadImage("../resources/emaildata/emails/default_email_icon.png")
        logger.info("Email mód betöltve!")

    def buttonBehaviour(self, isHidden=None):
        style = ""

        if isHidden == "hidden":
            style = """                  
                        * {
                            border: None;
                            background-color: white;
                            color: white;
                        }
                    """

            self.maliciousButtonHiddenState = True
            self.genuineButtonHiddenState = True

        elif isHidden == "present":
            style = """                  
                        * {
                            background-color: white;
                            color: grey;
                        }
                        
                        *:hover {
                            background-color: rgb(120, 120, 220);
	                        color: white;
                        }
                    """

            self.maliciousButtonHiddenState = False
            self.genuineButtonHiddenState = False

        self.maliciousButton.setStyleSheet(style)
        self.genuineButton.setStyleSheet(style)
        self.horizontalLine.setStyleSheet(style)

    def loadImage(self, imagePath):
        try:
            pixmap = QPixmap(imagePath)

            if not os.path.exists(imagePath):
                raise Exception("A megadott kép nem található!")

            frameSize = self.emailFrame.size()
            pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                   QtCore.Qt.TransformationMode.SmoothTransformation)

            self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.label.setGeometry(self.emailFrame.rect())
            self.label.setPixmap(pixmap)

        except Exception as e:
            logger.error(f"Hiba: {e}")

    def loadNextEmail(self, ID, path):
        self.selectedEmailID = ID
        self.buttonBehaviour("present")
        self.loadImage(path)



    def closeEmailWindow(self):
        self.hide()
        self.parent.show()
