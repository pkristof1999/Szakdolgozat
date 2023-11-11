import json

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QPushButton, QMainWindow, QComboBox, QLabel
from PyQt6.uic import loadUi

from src.main.python.components.logger import *
from src.main.python.components import clickableComboBox
from src.main.python.infoscreens import areYouSure
from src.main.python.components.errorMessage import errorMessage


class GuestSettingsWindowUI(QMainWindow):
    def __init__(self, parent, username):
        super(GuestSettingsWindowUI, self).__init__()
        loadUi("../resources/ui/default/guestSettingsWindow.ui", self)

        self.parent = parent

        self.profilePicture = self.findChild(QFrame, "profilePicture")
        self.restoreDefaultResultsButton = self.findChild(QPushButton, "restoreDefaultResultsButton")
        self.changeThemeBox = self.findChild(QComboBox, "changeThemeBox")
        self.abortButton = self.findChild(QPushButton, "abortButton")
        self.saveAndCloseButton = self.findChild(QPushButton, "saveAndCloseButton")

        self.questionWindow = None
        self.loginWindow = None

        """Ez csak azért kell ide, mert máshol nem tudtam középre igazítani a QComboBox tartalmát.
           This is here because I couldn't align the QComboBox's content to center elsewhere."""
        clickableLineEdit = clickableComboBox.ClickableLineEdit(self.changeThemeBox)

        self.changeThemeBox.setLineEdit(clickableLineEdit)
        clickableLineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        clickableLineEdit.setReadOnly(True)

        self.changeThemeBox.setStyleSheet("""
                    * {
                        background-color: white;
                        border: 2px solid #8f8f91;
                        border-radius: 10px;
                        color: grey;
                    }

                    *::drop-down {
                        border: thin solid grey;
                        right: 8px;
                    }

                    *::down-arrow {
                        image: url("../resources/pictures/Arrow.png");
                        width: 16px;
                        height: 16px;
                    }""")

        self.restoreDefaultResultsButton.clicked.connect(
            lambda: self.openQuestionWindow("Biztosan törli az eredményeit?"
                                            "\nEhhez nem kell a mentés gomb!",
                                            self.handleResultsDeletion,
                                            username
                                            )
        )

        self.abortButton.clicked.connect(self.abortAndCloseSettings)

        self.saveAndCloseButton.clicked.connect(
            lambda: self.openQuestionWindow("Biztosan menti\na módosításokat?",
                                            self.handleSaveAndCloseSettings,
                                            username
                                            )
        )

        self.label = QLabel(self.profilePicture)
        self.loadImage()
        self.loadThemes()

    def loadImage(self):
        pixmap = QPixmap("../resources/pictures/userDefault.png")

        frameSize = self.profilePicture.size()
        pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                               QtCore.Qt.TransformationMode.SmoothTransformation)

        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(self.profilePicture.rect())
        self.label.setPixmap(pixmap)

    def loadThemes(self):
        dataPath = "../resources/ui/themes.json"

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()

                    if not fileContents.strip() or fileContents.strip() == "{}":
                        self.changeThemeBox.addItem("Alap Téma")
                    else:
                        existingAccounts = json.loads(fileContents)
                        themes = existingAccounts.get("Themes", {})
                        theme_names = list(themes.values())
                        self.changeThemeBox.addItems(theme_names)

            else:
                self.changeThemeBox.addItem("Alap Téma")

        except Exception as e:
            errorMessage(f"Hiba: {e}")

    def openQuestionWindow(self, question, handler, username = None):
        self.questionWindow = None
        if not self.questionWindow:
            self.questionWindow = areYouSure.AreYouSureUI(question)

        if username is not None:
            self.questionWindow.finished.connect(lambda result: handler(result, username))
        else:
            self.questionWindow.finished.connect(handler)

        self.questionWindow.show()

    def abortAndCloseSettings(self):
        self.close()

    def handleSaveAndCloseSettings(self, result, username):
        if result == "Yes":
            self.saveAndCloseSettings(username)

    def saveAndCloseSettings(self, username):
        dataPath = "../../../userdata/profiles/guestProfile.json"

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()
                    existingAccounts = json.loads(fileContents)

        except Exception as e:
            errorMessage(f"Hiba: {e}")

        errorMessage("TODO: téma mentése")

        #TODO: téma mentése

    def handleResultsDeletion(self, result, username):
        if result == "Yes":
            self.resultsDeletion(username)

    def resultsDeletion(self, username):
        dataPath = "../../../userdata/profiles/guestProfile.json"
        try:
            with open(dataPath, 'r') as jsonFile:
                fileContents = json.load(jsonFile)

            if username in fileContents:
                fileContents[username]["LearnMedal"] = 0
                fileContents[username]["QuizMedal"] = 0
                fileContents[username]["EmailMedal"] = 0
                fileContents[username]["badge01"] = 0
                fileContents[username]["badge02"] = 0
                fileContents[username]["badge03"] = 0
                fileContents[username]["badge04"] = 0
                fileContents[username]["badge05"] = 0
                fileContents[username]["badge06"] = 0
                fileContents[username]["Score"] = 0

                with open(dataPath, 'w') as jsonFile:
                    json.dump(fileContents, jsonFile, indent=4)

        except Exception as e:
            errorMessage(f"Hiba: {e}")
