from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QFrame, QPushButton, QMainWindow, QLabel, QComboBox
from PyQt6.uic import loadUi

from src.main.python.components import clickableComboBox
from src.main.python.components.resultsDeletion import resultsDeletion
from src.main.python.components.translateTheme import translateTheme
from src.main.python.infoscreens import areYouSure
from src.main.python.infoscreens.errorMessage import errorMessage
from src.main.python.components.overwriteAccount import *


class GuestSettingsWindowUI(QMainWindow):
    def __init__(self, parent, username, theme):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            super(GuestSettingsWindowUI, self).__init__()

            self.theme = theme
            loadUi(f"../resources/ui/{self.theme}/{self.theme}GuestSettingsWindow.ui", self)
            self.setWindowIcon(QIcon("../resources/icon/icon.ico"))

            self.setFixedSize(self.size())

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

            dropDownColor = "rgb(255, 255, 255)" if self.theme == "default" \
                else "rgb(70, 70, 100)" if self.theme == "dark" \
                else "rgb(50, 50, 50)" if self.theme == "highContrast" \
                else "#FF9C00" if self.theme == "yellow" \
                else "rgb(50, 150, 50)" if self.theme == "green" \
                else "white"

            dropDownTextColor = "grey" if self.theme == "default" \
                else "whitesmoke" if self.theme == "dark" \
                else "white" if self.theme == "highContrast" or self.theme == "yellow" or self.theme == "green" \
                else "#8f8f91"

            dropDownBorderColor = "yellow" if self.theme == "highContrast" else "#8f8f91"

            dropDownHoverTextColor = "yellow" if self.theme == "highContrast" \
                else "#8f8f91" if self.theme == "yellow" \
                else "whitesmoke"

            dropDownBackgroundColor = "rgb(20, 20, 20)" if self.theme == "highContrast" \
                else "#FFF200" if self.theme == "yellow" \
                else "rgb(80, 220, 80)" if self.theme == "green" \
                else "#8f8f91"

            self.changeThemeBox.setStyleSheet(f"""
                                                * {{
                                                    background-color: {dropDownColor};
                                                    border: 2px solid {dropDownBorderColor};
                                                    border-radius: 0;
                                                    color: {dropDownTextColor};
                                                }}

                                                *::drop-down {{
                                                    border: thin solid grey;
                                                    right: 8px;
                                                }}
                                                
                                                *::item {{
                                                    color: {dropDownTextColor};
                                                    background-color: rgba(0, 0, 0, 0);
                                                }}
                                                
                                                *::item:hover {{
                                                    color: {dropDownHoverTextColor};
                                                    background-color: {dropDownBackgroundColor};
                                                }}

                                                *::down-arrow {{
                                                    image: url("../resources/pictures/Arrow.png");
                                                    width: 16px;
                                                    height: 16px;
                                                }}
                                                """
                                              )

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
            self.loadThemes(username)

        except Exception as e:
            errorMessage(e)
            self.parent.hide()
            self.hide()

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

    def loadThemes(self, username):
        themeDataPath = "../resources/ui/themes.json"
        dataPath = "../../../userdata/profiles/guestProfile.json"

        selectedTheme = ""

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()

                userData = json.loads(fileContents.strip(username))
                userTheme = userData[username]["Theme"]

                selectedTheme = translateTheme(userTheme, False)

            if os.path.exists(themeDataPath):
                with open(themeDataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()

                    if not fileContents.strip() or fileContents.strip() == "{}":
                        self.changeThemeBox.addItem("Alap Téma")
                    else:
                        existingAccounts = json.loads(fileContents)
                        themes = existingAccounts.get("Themes", {})
                        themeNames = list(themes.values())
                        self.changeThemeBox.addItems(themeNames)
                        self.changeThemeBox.setCurrentText(selectedTheme)

            else:
                self.changeThemeBox.addItem("Hiba")

        except Exception as e:
            errorMessage(f"Hiba: {e}")

    def loadCurrentTheme(self, username):
        dataPath = "../../../userdata/profiles/guestProfile.json"

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()

                userData = json.loads(fileContents.strip(username))
                userTheme = userData[username]["Theme"]

                return userTheme

        except Exception as e:
            errorMessage(f"Hiba: {e}")

    def openQuestionWindow(self, question, handler, username = None):
        self.questionWindow = None
        if not self.questionWindow:
            self.questionWindow = areYouSure.AreYouSureUI(question, self.theme)

        if username is not None:
            self.questionWindow.finished.connect(lambda result: handler(result, username))
        else:
            self.questionWindow.finished.connect(handler)

        self.questionWindow.show()

    def abortAndCloseSettings(self):
        self.hide()

    def handleSaveAndCloseSettings(self, result, username):
        if result == "Yes":
            self.saveAndCloseSettings(username)

    def saveAndCloseSettings(self, username):
        theme = translateTheme(self.changeThemeBox.currentText(), True)
        overWriteGuestAccount(username, theme)

        self.parent.refreshWindow()
        self.hide()

        logger.info("Adatok mentve!")

    def handleResultsDeletion(self, result, username):
        if result == "Yes":
            resultsDeletion(username, "../../../userdata/profiles/guestProfile.json")
