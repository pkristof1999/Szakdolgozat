from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QPushButton, QMainWindow, QLabel, QComboBox
from PyQt6.uic import loadUi

from src.main.python.components import clickableComboBox
from src.main.python.components.resultsDeletion import resultsDeletion
from src.main.python.components.translateTheme import translateTheme
from src.main.python.infoscreens import areYouSure
from src.main.python.components.errorMessage import errorMessage
from src.main.python.components.overwriteAccount import *


class GuestSettingsWindowUI(QMainWindow):
    def __init__(self, parent, username):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            super(GuestSettingsWindowUI, self).__init__()
            loadUi("../resources/ui/default/guestSettingsWindow.ui", self)

            self.parent = parent

            self.profilePicture = self.findChild(QFrame, "profilePicture")
            self.restoreDefaultResultsButton = self.findChild(QPushButton, "restoreDefaultResultsButton")

            """Ha ezt a sort törlöm, nem működik a témaválasztás valamiért..."""
            self.deleteUserProfileButton = self.findChild(QPushButton, "deleteUserProfileButton")

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

        except Exception as e:
            errorMessage(e)
            self.parent.close()
            self.close()

    def loadImage(self):
        try:
            pixmap = QPixmap("../resources/pictures/userDefault.png")

            if not os.path.exists("../resources/pictures/userDefault.png"):
                raise Exception("A megadott kép nem található!")

            frameSize = self.profilePicture.size()
            pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                   QtCore.Qt.TransformationMode.SmoothTransformation)

            self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.label.setGeometry(self.profilePicture.rect())
            self.label.setPixmap(pixmap)

        except Exception as e:
            logger.error(f"Hiba: {e}")

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
        theme = translateTheme(self.changeThemeBox.currentText())
        overWriteGuestAccount(username, theme)

        self.parent.refreshWindow()
        self.close()

        logger.info("Adatok mentve!")

    def handleResultsDeletion(self, result, username):
        if result == "Yes":
            resultsDeletion(username, "../../../userdata/profiles/guestProfile.json")
