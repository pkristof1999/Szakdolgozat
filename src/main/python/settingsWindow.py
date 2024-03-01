import json
import random
import shutil

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QFrame, QPushButton, QMainWindow, QComboBox, QLabel, QFileDialog, QLineEdit
from PyQt6.uic import loadUi
from datetime import datetime

from src.main.python import loginScreen
from src.main.python.components.logger import *
from src.main.python.components import clickableComboBox
from src.main.python.components.resultsDeletion import resultsDeletion
from src.main.python.infoscreens import areYouSure
from src.main.python.components.checkPwdStrenght import *
from src.main.python.components.securePwd import *
from src.main.python.components.overwriteAccount import overwriteAccount as overWrite
from src.main.python.components.isConvertible import convertibleToInt
from src.main.python.components.translateTheme import translateTheme
from src.main.python.infoscreens.errorMessage import errorMessage


class SettingsWindowUI(QMainWindow):
    def __init__(self, basePath, parent, username, theme):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            self.basePath = basePath

            super(SettingsWindowUI, self).__init__()

            self.theme = theme
            loadUi(os.path.join(
                self.basePath, f"src/main/resources/ui/{self.theme}/{self.theme}SettingsWindow.ui"), self
            )
            self.setWindowIcon(QIcon(os.path.join(self.basePath, "src/main/resources/icon/icon.ico")))

            self.setFixedSize(self.size())

            self.parent = parent

            self.profilePicture = self.findChild(QFrame, "profilePicture")
            self.changeProfilePictureButton = self.findChild(QPushButton, "changeProfilePictureButton")
            self.deleteProfilePictureButton = self.findChild(QPushButton, "deleteProfilePictureButton")
            self.changeUserAge = self.findChild(QLineEdit, "changeUserAge")
            self.oldPassword = self.findChild(QLineEdit, "oldPassword")
            self.newPassword1 = self.findChild(QLineEdit, "newPassword1")
            self.newPassword2 = self.findChild(QLineEdit, "newPassword2")
            self.restoreDefaultResultsButton = self.findChild(QPushButton, "restoreDefaultResultsButton")
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
                                                    image: url({
                                                os.path.join(self.basePath, "src/main/resources/pictures/Arrow.png"
                                                             )});
                                                    width: 16px;
                                                    height: 16px;
                                                }}
                                                """
                                              )

            self.changeProfilePictureButton.clicked.connect(
                lambda: self.openQuestionWindow("Biztosan lecseréli a profilképét?",
                                                self.handleProfilePictureChange
                                                )
            )
            self.deleteProfilePictureButton.clicked.connect(
                lambda: self.openQuestionWindow("Biztos benne, hogy törli\na profilképét?",
                                                self.handleProfilePictureDeletion
                                                )
            )
            self.restoreDefaultResultsButton.clicked.connect(
                lambda: self.openQuestionWindow("Biztosan törli az eredményeit?"
                                                "\nEhhez nem kell a mentés gomb!",
                                                self.handleResultsDeletion,
                                                username
                                                )
            )
            self.deleteUserProfileButton.clicked.connect(
                lambda: self.openQuestionWindow("Biztosan törli\na felhasználói profilját?"
                                                "\nEhhez nem kell a mentés gomb!",
                                                self.handleProfileDeletion,
                                                username
                                                )
            )

            self.newPassword1.textChanged.connect(self.changeNewPassword1)
            self.newPassword2.textChanged.connect(self.changeNewPassword2)

            self.abortButton.clicked.connect(self.abortAndCloseSettings)

            self.saveAndCloseButton.clicked.connect(
                lambda: self.openQuestionWindow("Biztosan menti\na módosításokat?",
                                                self.handleSaveAndCloseSettings,
                                                username
                                                )
            )

            self.imagePath = self.getImagePath(username)
            self.oldImage = self.imagePath
            self.label = QLabel(self.profilePicture)

            self.loadImage(self.imagePath)
            self.loadUserAge(username)
            self.loadThemes(username)

        except Exception as e:
            errorMessage(e)
            self.parent.hide()
            self.hide()

    def addPicture(self):
        fileDialog = QFileDialog(self)
        fileDialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        fileDialog.setViewMode(QFileDialog.ViewMode.List)
        fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if fileDialog.exec() == QFileDialog.DialogCode.Accepted:
            selectedFiles = fileDialog.selectedFiles()
            if selectedFiles:
                self.imagePath = selectedFiles[0]
                self.loadImage(self.imagePath)
                logger.info("Új profilkép kiválasztásra került!")

    def getImagePath(self, username):
        dataPath = os.path.join(self.basePath, "userdata/profiles/profiles.json")

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()
                    existingAccounts = json.loads(fileContents)

                    return os.path.join(self.basePath, existingAccounts[username]["ProfilePicturePath"])

        except Exception as e:
            logger.info(f"Hiba: {e}")

    def loadImage(self, imagePath):
        try:
            pixmap = QPixmap(imagePath)

            if not os.path.exists(imagePath):
                raise Exception("A megadott kép nem található!")

            frameSize = self.profilePicture.size()
            pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                   QtCore.Qt.TransformationMode.SmoothTransformation)

            self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.label.setGeometry(self.profilePicture.rect())
            self.label.setPixmap(pixmap)

        except Exception as e:
            logger.error(f"Hiba: {e}")

    def loadDefaultImage(self):
        try:
            pixmap = QPixmap(os.path.join(self.basePath, "src/main/resources/pictures/userDefault.png"))

            if not os.path.exists(os.path.join(self.basePath, "src/main/resources/pictures/userDefault.png")):
                raise Exception("A megadott kép nem található!")

            frameSize = self.profilePicture.size()
            pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                   QtCore.Qt.TransformationMode.SmoothTransformation)

            self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.label.setGeometry(self.profilePicture.rect())
            self.label.setPixmap(pixmap)
            self.imagePath = os.path.join(self.basePath, "src/main/resources/pictures/userDefault.png")
            logger.info("Alap profilkép betöltésre került!")

        except Exception as e:
            logger.error(f"Hiba: {e}")

    def loadUserAge(self, username):
        dataPath = os.path.join(self.basePath, "userdata/profiles/profiles.json")

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()
                    existingAccounts = json.loads(fileContents)
                    storedUserAge = existingAccounts[username]["UserAge"]

        except Exception as e:
            logger.error(f"Hiba: {e}")

        self.changeUserAge.setText(str(storedUserAge))

    def loadThemes(self, username):
        themeDataPath = os.path.join(self.basePath, "src/main/resources/ui/themes.json")
        dataPath = os.path.join(self.basePath, "userdata/profiles/profiles.json")

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

    def openQuestionWindow(self, question, handler, username=None):
        self.questionWindow = None
        if not self.questionWindow:
            self.questionWindow = areYouSure.AreYouSureUI(self.basePath, question, self.theme)

        if username is not None:
            self.questionWindow.finished.connect(lambda result: handler(result, username))
        else:
            self.questionWindow.finished.connect(handler)

        self.questionWindow.show()

    def handleProfilePictureDeletion(self, result):
        if result == "Yes":
            self.loadDefaultImage()

    def handleProfilePictureChange(self, result):
        if result == "Yes":
            self.addPicture()

    def changeNewPassword1(self):
        password = self.newPassword1.text().strip()
        chkPwd = calculateStrength(password)

        if chkPwd == 0:
            self.newPassword1.setStyleSheet(changeColor("red"))
        elif 0 < chkPwd < 5:
            self.newPassword1.setStyleSheet(changeColor("orange"))
        elif chkPwd >= 5:
            self.newPassword1.setStyleSheet(changeColor("green"))

        self.changeNewPassword2()

    def changeNewPassword2(self):
        password1 = self.newPassword1.text().strip()
        password2 = self.newPassword2.text().strip()
        chkPwd = calculateStrength(password1)

        if password1 != password2 or chkPwd == 0:
            self.newPassword2.setStyleSheet(changeColor("red"))
        else:
            self.newPassword2.setStyleSheet(changeColor("green"))

    def abortAndCloseSettings(self):
        self.hide()

    def handleSaveAndCloseSettings(self, result, username):
        if result == "Yes":
            self.saveAndCloseSettings(username)

    def saveAndCloseSettings(self, username):
        message = ""

        saveData = True
        newPassword = False
        dataPath = os.path.join(self.basePath, "userdata/profiles/profiles.json")

        userAge = self.changeUserAge.text().strip()
        oldPwd = self.oldPassword.text().strip()
        newPwd1 = self.newPassword1.text().strip()
        newPwd2 = self.newPassword2.text().strip()
        theme = translateTheme(self.changeThemeBox.currentText(), True)

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()
                    existingAccounts = json.loads(fileContents)
                    storedPwd = existingAccounts[username]["Password"]
                    storedPPath = existingAccounts[username]["ProfilePicturePath"]

        except Exception as e:
            errorMessage(f"Hiba: {e}")

        if len(userAge) == 0:
            if message == "":
                message = message + "Nem adott meg életkort!"
            else:
                message = message + "\nNem adott meg életkort!"
            saveData = False

        if convertibleToInt(userAge):
            userAge = int(userAge)
            if 1 > userAge or 150 < userAge:
                if message == "":
                    message = message + "Nem adható meg ilyen életkor!"
                else:
                    message = message + "\nNem adható meg ilyen életkor!"
                saveData = False

        if not convertibleToInt(userAge):
            if message == "":
                message = message + "Nem egész szám a megadott életkor!"
            else:
                message = message + "\nNem egész szám a megadott életkor!"
            saveData = False

        if oldPwd == "" and newPwd1 == "" and newPwd2 == "":
            newPassword = False
            logger.info("Nem került új jelszó megadásra!")
        else:
            if oldPwd == "" and newPwd1 != "" or oldPwd == "" and newPwd2 != "":
                if message == "":
                    message = message + "Nem adta meg a régi jelszót!"
                else:
                    message = message + "\nNem adta meg a régi jelszót!"
                saveData = False

            if oldPwd != "":
                if not checkPassword(oldPwd, storedPwd):
                    if message == "":
                        message = message + "A régi jelszó nem egyezik!"
                    else:
                        message = message + "\nA régi jelszó nem egyezik!"
                    saveData = False
                elif oldPwd == newPwd1:
                    if message == "":
                        message = message + "Nem adhatja meg újra a régi jelszót!"
                    else:
                        message = message + "\nNem adhatja meg újra a régi jelszót!"
                    saveData = False

                if calculateStrength(newPwd1) == 0:
                    if message == "":
                        message = message + "A jelszó nem megfelelő erősségű!"
                    else:
                        message = message + "\nA jelszó nem megfelelő erősségű!"
                    saveData = False

                if newPwd1 != newPwd2:
                    if message == "":
                        message = message + "Az új jelszavak nem egyeznek!"
                    else:
                        message = message + "\nAz új jelszavak nem egyeznek!"
                    saveData = False

            newPassword = True

        if message != "":
            errorMessage(message)

        if saveData:
            tmpOldImage = self.oldImage
            if "src" in tmpOldImage:
                tmpOldImage = tmpOldImage.split("src", 1)
                defaultImage = tmpOldImage[1]
                defaultImage = "src" + defaultImage
            else:
                tmpOldImage = tmpOldImage.split("userdata", 1)
                defaultImage = tmpOldImage[1]
                defaultImage = "userdata" + defaultImage

            if self.imagePath != os.path.join(self.basePath, "src/main/resources/pictures/userDefault.png") \
                    and self.imagePath != self.oldImage:
                randomNumber = random.randint(1000, 9999)
                currentTime = datetime.now()
                formattedTime = currentTime.strftime("%Y%m%d_%H%M%S_") + f"{randomNumber}"

                pictureDirectory = os.path.join(self.basePath, "userdata/profiles/profilepicture")
                os.makedirs(pictureDirectory, exist_ok=True)

                shutil.copy(self.imagePath,
                            os.path.join(self.basePath,
                                         f"userdata/profiles/profilepicture/avatar_{formattedTime}.png")
                            )

                try:
                    if not defaultImage == "src/main/resources/pictures/userDefault.png":
                        os.remove(self.oldImage)
                        logger.info("Régi profilkép törlésre került!")

                except OSError as e:
                    errorMessage(f"Hiba: {e}")

                newImagePath = os.path.join(
                    self.basePath, f"userdata/profiles/profilepicture/avatar_{formattedTime}.png"
                )

                """Elég csak a jelszót vizsgálni, mert az titkosított,
                így nem lehet a beolvasottal egyszerűen felülírni."""
                if newPassword:
                    overWrite(self.basePath, username, userAge, newImagePath, theme, newPwd1)
                else:
                    overWrite(self.basePath, username, userAge, newImagePath, theme)

            elif self.imagePath == os.path.join(self.basePath, "src/main/resources/pictures/userDefault.png") \
                    and self.imagePath != self.oldImage:

                try:
                    if not defaultImage == "src/main/resources/pictures/userDefault.png":
                        os.remove(self.oldImage)
                        logger.info("Régi profilkép törlésre került!")

                except OSError as e:
                    errorMessage(f"Hiba: {e}")

                if newPassword:
                    overWrite(self.basePath, username, userAge, self.imagePath, theme, newPwd1)
                else:
                    overWrite(self.basePath, username, userAge, self.imagePath, theme)
            else:
                if newPassword:
                    overWrite(self.basePath, username, userAge, storedPPath, theme, newPwd1)
                else:
                    overWrite(self.basePath, username, userAge, storedPPath, theme)

            self.parent.refreshWindow()
            self.hide()

            logger.info("Adatok mentve!")

    def handleResultsDeletion(self, result, username):
        if result == "Yes":
            resultsDeletion(username, os.path.join(self.basePath, "userdata/profiles/profiles.json"))

    def handleProfileDeletion(self, result, username):
        if result == "Yes":
            self.userDeletion(username)

    def userDeletion(self, username):
        dataPath = os.path.join(self.basePath, "userdata/profiles/profiles.json")
        try:
            with open(dataPath, 'r') as jsonFile:
                fileContents = json.load(jsonFile)

            if username in fileContents:
                profilePictureDeletion = fileContents[username]["ProfilePicturePath"]

                if profilePictureDeletion != "src/main/resources/pictures/userDefault.png":
                    try:
                        os.remove(os.path.join(self.basePath, profilePictureDeletion))
                        logger.info("Profilkép törlésre került!")
                    except OSError as e:
                        errorMessage(f"Hiba: {e}")

                del fileContents[username]

            with open(dataPath, 'w') as json_file:
                json.dump(fileContents, json_file, indent=4)

            logger.info("Felhasználó sikeresen törölve!")

            self.hide()
            self.parent.hide()
            self.openLoginUI()

        except Exception as e:
            errorMessage(f"Hiba: {e}")

    def openLoginUI(self):
        if not self.loginWindow:
            self.loginWindow = loginScreen.LoginScreenUI(self.basePath)
        self.loginWindow.show()
        logger.info("Bejelentkezési képernyő megnyitásra került!")
        self.hide()
