import json
import time
import random
import threading

from PyQt6 import QtCore
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QLabel, QPushButton, QMainWindow, QFrame
from PyQt6.uic import loadUi

from src.main.python.components.logger import *
from src.main.python.infoscreens import resultsScreen
from src.main.python.infoscreens.errorMessage import errorMessage


class EmailWindowUI(QMainWindow):
    def __init__(self, username, parent, theme):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            self.username = username

            super(EmailWindowUI, self).__init__()

            self.theme = theme
            self.setWindowIcon(QIcon("../resources/icon/icon.ico"))
            loadUi(f"../resources/ui/{self.theme}/{self.theme}EmailWindow.ui", self)

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
            self.subjectLabel = self.findChild(QLabel, "subjectLabel")
            self.emailFrame = self.findChild(QFrame, "emailFrame")
            self.horizontalLine1 = self.findChild(QFrame, "horizontalLine1")
            self.horizontalLine2 = self.findChild(QFrame, "horizontalLine2")

            self.resultsWindow = None

            self.subjectLabel.setText("")
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

            self.selectedButton = ""
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

            self.selectedEmail1IsMalicious = False
            self.selectedEmail2IsMalicious = False
            self.selectedEmail3IsMalicious = False
            self.selectedEmail4IsMalicious = False
            self.selectedEmail5IsMalicious = False
            self.selectedEmail6IsMalicious = False
            self.selectedEmail7IsMalicious = False
            self.selectedEmail8IsMalicious = False
            self.selectedEmail9IsMalicious = False
            self.selectedEmail10IsMalicious = False

            self.email1IsDone = False
            self.email2IsDone = False
            self.email3IsDone = False
            self.email4IsDone = False
            self.email5IsDone = False
            self.email6IsDone = False
            self.email7IsDone = False
            self.email8IsDone = False
            self.email9IsDone = False
            self.email10IsDone = False

            self.label = QLabel(self.emailFrame)

            self.emailBank = []
            self.emailIndex = 0
            self.previousEmails = []
            self.pointsEarned = 0

            self.terminateTimerThread = threading.Event()
            self.timerThread = None
            self.timeSpent = 0

            self.startEmailTimer(self.timeSpent)

            self.backButton.clicked.connect(self.closeEmailWindow)

            self.closeEvent = lambda event: parent.exitWindow(event, self.timerThread)

            self.answerButtonStyleSheet = self.maliciousButton.styleSheet()

            self.loadSubjects()
            self.loadDefaults()

            self.email1Button.clicked.connect(lambda:
                                              self.loadNextEmail(
                                                  self.email1Button, self.email1ID, self.email1Path))

            self.email2Button.clicked.connect(lambda:
                                              self.loadNextEmail(
                                                  self.email2Button, self.email2ID, self.email2Path))

            self.email3Button.clicked.connect(lambda:
                                              self.loadNextEmail(
                                                  self.email3Button, self.email3ID, self.email3Path))

            self.email4Button.clicked.connect(lambda:
                                              self.loadNextEmail(
                                                  self.email4Button, self.email4ID, self.email4Path))

            self.email5Button.clicked.connect(lambda:
                                              self.loadNextEmail(
                                                  self.email5Button, self.email5ID, self.email5Path))

            self.email6Button.clicked.connect(lambda:
                                              self.loadNextEmail(
                                                  self.email6Button, self.email6ID, self.email6Path))

            self.email7Button.clicked.connect(lambda:
                                              self.loadNextEmail(
                                                  self.email7Button, self.email7ID, self.email7Path))

            self.email8Button.clicked.connect(lambda:
                                              self.loadNextEmail(
                                                  self.email8Button, self.email8ID, self.email8Path))

            self.email9Button.clicked.connect(lambda:
                                              self.loadNextEmail(
                                                  self.email9Button, self.email9ID, self.email9Path))

            self.email10Button.clicked.connect(lambda:
                                               self.loadNextEmail(
                                                   self.email10Button, self.email10ID, self.email10Path))

            self.checkButton.clicked.connect(self.checkResults)

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
            # button.setText(f"{self.emailBank[i]['subject']} - {self.emailBank[i]['isMalicious']}")
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

        backgroundColor = "rgb(20, 20, 20)" if self.theme == "highContrast" else "white"
        textColor = "rgb(20, 20, 20)" if self.theme == "highContrast" else "white"

        if isHidden == "hidden":
            style = f"""                  
                        * {{
                            border: None;
                            background-color: {backgroundColor};
                            color: {textColor};
                        }}
                    """

            self.maliciousButtonHiddenState = True
            self.genuineButtonHiddenState = True

        elif isHidden == "present":
            style = self.answerButtonStyleSheet

            self.maliciousButtonHiddenState = False
            self.genuineButtonHiddenState = False

            self.maliciousButton.clicked.connect(lambda: self.chooseEmailType(self.selectedEmailID, False))
            self.genuineButton.clicked.connect(lambda: self.chooseEmailType(self.selectedEmailID, True))

        self.maliciousButton.setStyleSheet(style)
        self.genuineButton.setStyleSheet(style)
        self.horizontalLine1.setStyleSheet(style)
        self.horizontalLine2.setStyleSheet(style)


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

    def loadNextEmail(self, button, ID, path):
        self.selectedButton = button
        self.selectedEmailID = ID
        self.buttonBehaviour("present")
        self.loadImage(path)

        self.subjectLabel.setText(button.text())

        for i in self.emailBank:
            if i["ID"] == ID:
                logger.info(f"{button.text()} kiválasztva.")

    def chooseEmailType(self, ID, isMalicious):
        firstGreenStyle = """
                             * {
                                background-color: rgb(167, 255, 111);
                                border-radius: 0;
                                border-top-left-radius: 10px;
                                border-top-right-radius: 10px;
                                color: grey;
                             }
                             
                             *:hover {
                                 background-color: yellow;
                             }
                          """
        lastGreenStyle = """
                             * {
                                background-color: rgb(167, 255, 111);
                                border-radius: 0;
                                border-bottom-left-radius: 10px;
                                border-bottom-right-radius: 10px;
                                color: grey;
                             }
                             
                             *:hover {
                                 background-color: yellow;
                             }
                          """
        firstRedStyle = """
                           * {
                              background-color: rgb(255, 173, 173);
                              border-radius: 0;
                              border-top-left-radius: 10px;
                              border-top-right-radius: 10px;
                              color: grey;
                           }
                           *:hover {
                               background-color: yellow;
                           }
                          """
        lastRedStyle = """
                             * {
                                background-color: rgb(255, 173, 173);
                                border-radius: 0;
                                border-bottom-left-radius: 10px;
                                border-bottom-right-radius: 10px;
                                color: grey;
                             }
                             
                             *:hover {
                                 background-color: yellow;
                             }
                          """
        greenStyle = """                  
                    * {
                        background-color: rgb(167, 255, 111);
                        border-radius: 0;
                        color: grey;
                    }
                    
                    *:hover {
                        background-color: yellow;
                    }
                """
        redStyle = """                  
                    * {
                        background-color: rgb(255, 173, 173);
                        border-radius: 0;
                        color: grey;
                    }
                    
                    *:hover {
                        background-color: yellow;
                    }
                """

        textOfSelectedButton = self.selectedButton.text()
        if "\u2714" not in textOfSelectedButton:
            textOfSelectedButton += "\u2714"
            self.selectedButton.setText(textOfSelectedButton)

        textOfSelectedButton = ""

        if isMalicious:
            if self.selectedButton == self.email1Button:
                self.selectedButton.setStyleSheet(firstGreenStyle)
            elif self.selectedButton == self.email10Button:
                self.selectedButton.setStyleSheet(lastGreenStyle)
            else:
                self.selectedButton.setStyleSheet(greenStyle)
        else:
            if self.selectedButton == self.email1Button:
                self.selectedButton.setStyleSheet(firstRedStyle)
            elif self.selectedButton == self.email10Button:
                self.selectedButton.setStyleSheet(lastRedStyle)
            else:
                self.selectedButton.setStyleSheet(redStyle)

        for i in range(10):
            selectMalicious = f"selectedEmail{i + 1}IsMalicious"
            done = f"email{i + 1}IsDone"

            if self.emailBank[i]["ID"] == ID:
                setattr(self, done, True)
                setattr(self, selectMalicious, isMalicious)

    def checkResults(self):
        canProceed = False

        for i in range(10):
            done = f"email{i + 1}IsDone"
            IsDone = getattr(self, done)
            if not IsDone:
                errorMessage("Nem döntöttél minden Emailről!")
                canProceed = False
                break
            else:
                canProceed = True

        if canProceed:
            self.terminateTimerThread.set()

            if self.timerThread and self.timerThread.is_alive():
                self.timerThread.join()

            if self.timerThread is not None:
                while True:
                    if not self.timerThread.is_alive():
                        break

            self.timerThread = None
            self.resultsWindow = None

            badge1 = False
            badge2 = False
            numberOfRightAnswers = 0

            for i in range(10):
                getEmailMaliciousName = f"email{i + 1}IsMalicious"
                givenEmailMaliciousName = f"selectedEmail{i + 1}IsMalicious"

                getEmailMalicious = getattr(self, getEmailMaliciousName)
                givenEmailMalicious = getattr(self, givenEmailMaliciousName)

                if getEmailMalicious != givenEmailMalicious:
                    numberOfRightAnswers += 1

            minutes, seconds = divmod(self.timeSpent, 60)

            if self.timeSpent <= 3600:
                info = f"""
                            A helyes válaszok száma: 10/{numberOfRightAnswers} ({int(numberOfRightAnswers / 10 * 100)}%)
                            Email móddal töltött idő: {minutes:02d}:{seconds:02d}
                            Kitűzőt szereztél teljesítésre! Értéke: 100 pont*"""
            else:
                info = f"""
                            A helyes válaszok száma: 10/{numberOfRightAnswers} ({int(numberOfRightAnswers / 10 * 100)}%)
                            Email móddal töltött idő: Több, mint egy óra
                            Kitűzőt szereztél teljesítésre! Értéke: 100 pont*"""

            if numberOfRightAnswers == 10:
                info += """
                            Minden válaszod helyes volt!
                            Kitűzőt szereztél pontosságra! Értéke: 250 pont*"""
                badge1 = True

                if self.timeSpent <= 60:
                    info += """
                                Teljesítetted az email módot 01:00-n belül!
                                Kitűzőt szereztél sebességre! Értéke: 1000 pont*
                            """
                    badge2 = True

            info += """
                        * Csak akkor kerül beszámításra, ha eddig nem volt meg!
                    """

            self.saveResults(badge1, badge2)

            if not self.resultsWindow:
                self.resultsWindow = resultsScreen.ResultsScreenUI(info, self, self.parent, self.theme)

            self.resultsWindow.show()
            self.hide()

    def startEmailTimer(self, seconds):
        self.terminateTimerThread.clear()
        self.timerThread = threading.Thread(target=self.timerThreadCounter, args=(seconds,))
        self.timerThread.start()

    def timerThreadCounter(self, seconds):
        times = 0
        while True:
            time.sleep(0.1)
            times += 1
            if times == 10:
                seconds += 1
                times = 0

            if self.terminateTimerThread.is_set():
                self.timeSpent = seconds
                break

    def saveResults(self, badge1, badge2):
        try:
            if self.username == "Vendég":
                dataPath = "../../../userdata/profiles/guestProfile.json"
            else:
                dataPath = "../../../userdata/profiles/profiles.json"

            with open(dataPath, 'r') as jsonFile:
                fileContents = json.load(jsonFile)

            if self.username in fileContents:
                if badge1 and badge2:
                    if fileContents[self.username]["EmailMedal"] == 0 and \
                            fileContents[self.username]["badge05"] == 0 and \
                            fileContents[self.username]["badge06"] == 0:
                        self.pointsEarned = 1350
                        fileContents[self.username]["Score"] += self.pointsEarned
                    elif fileContents[self.username]["EmailMedal"] == 1 and \
                            fileContents[self.username]["badge05"] == 0 and \
                            fileContents[self.username]["badge06"] == 0:
                        self.pointsEarned = 1250
                        fileContents[self.username]["Score"] += self.pointsEarned
                    elif fileContents[self.username]["EmailMedal"] == 1 and \
                            fileContents[self.username]["badge05"] == 1 and \
                            fileContents[self.username]["badge06"] == 0:
                        self.pointsEarned = 1000
                        fileContents[self.username]["Score"] += self.pointsEarned

                    fileContents[self.username]["EmailMedal"] = 1
                    fileContents[self.username]["badge05"] = 1
                    fileContents[self.username]["badge06"] = 1
                elif badge1:
                    if fileContents[self.username]["EmailMedal"] == 0 and \
                            fileContents[self.username]["badge05"] == 0:
                        self.pointsEarned = 350
                        fileContents[self.username]["Score"] += self.pointsEarned
                    elif fileContents[self.username]["EmailMedal"] == 1 and \
                            fileContents[self.username]["badge05"] == 0:
                        self.pointsEarned = 250
                        fileContents[self.username]["Score"] += self.pointsEarned

                    fileContents[self.username]["EmailMedal"] = 1
                    fileContents[self.username]["badge05"] = 1
                else:
                    if fileContents[self.username]["EmailMedal"] == 0:
                        self.pointsEarned = 100
                        fileContents[self.username]["Score"] += self.pointsEarned
                    fileContents[self.username]["EmailMedal"] = 1

            with open(dataPath, 'w') as jsonFile:
                json.dump(fileContents, jsonFile, indent=4)

        except Exception as e:
            errorMessage(f"Hiba: {e}")

    def closeEmailWindow(self):
        self.terminateTimerThread.set()

        if self.timerThread and self.timerThread.is_alive():
            self.timerThread.join()

        self.timerThread = None

        self.parent.show()
        self.hide()
        logger.info("Email játékmód bezárása!")
