import json
import random
import shutil

import loginScreen

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QPushButton, QMainWindow, QComboBox, QLabel, QFileDialog, QLineEdit, QMessageBox
from PyQt6.uic import loadUi
from datetime import datetime

from src.main.python.components.logger import *
from src.main.python.components import clickableComboBox
from src.main.python.infoscreens import areYouSure
from src.main.python.components.checkPwdStrenght import *
from src.main.python.components.securePwd import *
from src.main.python.components.overwriteAccount import overwriteAccount as overWrite
from src.main.python.components.isConvertible import convertibleToInt
from src.main.python.components.errorMessage import errorMessage


class SettingsWindowUI(QMainWindow):
    def __init__(self, parent, username):
        super(SettingsWindowUI, self).__init__()
        loadUi("../resources/ui/default/settingsWindow.ui", self)

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
        dataPath = "../../../userdata/profiles/profiles.json"

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()
                    existingAccounts = json.loads(fileContents)
                    if "avatar" in existingAccounts[username]["ProfilePicturePath"]:
                        return "../../" + existingAccounts[username]["ProfilePicturePath"]
                    else:
                        return existingAccounts[username]["ProfilePicturePath"]

        except Exception as e:
            logger.info(f"Hiba: {e}")

    def loadImage(self, imagePath):
        pixmap = QPixmap(imagePath)

        frameSize = self.profilePicture.size()
        pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                               QtCore.Qt.TransformationMode.SmoothTransformation)

        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(self.profilePicture.rect())
        self.label.setPixmap(pixmap)

    def loadDefaultImage(self):
        pixmap = QPixmap("../resources/pictures/userDefault.png")

        frameSize = self.profilePicture.size()
        pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                               QtCore.Qt.TransformationMode.SmoothTransformation)

        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(self.profilePicture.rect())
        self.label.setPixmap(pixmap)
        self.imagePath = "../resources/pictures/userDefault.png"
        logger.info("Alap profilkép betöltésre került!")

    def loadUserAge(self, username):
        dataPath = "../../../userdata/profiles/profiles.json"

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()
                    existingAccounts = json.loads(fileContents)
                    storedUserAge = existingAccounts[username]["UserAge"]

        except Exception as e:
            logger.error(f"Hiba: {e}")

        self.changeUserAge.setText(str(storedUserAge))

    def openQuestionWindow(self, question, handler, username = None):
        self.questionWindow = None
        if not self.questionWindow:
            self.questionWindow = areYouSure.AreYouSureUI(question)

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
        self.close()

    def handleSaveAndCloseSettings(self, result, username):
        if result == "Yes":
            self.saveAndCloseSettings(username)

    def saveAndCloseSettings(self, username):
        saveData = True
        newPassword = False
        dataPath = "../../../userdata/profiles/profiles.json"

        userAge = self.changeUserAge.text().strip()
        oldPwd = self.oldPassword.text().strip()
        newPwd1 = self.newPassword1.text().strip()
        newPwd2 = self.newPassword2.text().strip()

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
            errorMessage("Nem adott meg életkort!")
            saveData = False

        if convertibleToInt(userAge):
            userAge = int(userAge)
            if 1 > userAge or 150 < userAge:
                errorMessage("Nem adható meg ilyen életkor!")
                saveData = False

        if not convertibleToInt(userAge):
            errorMessage("Nem egész szám a megadott életkor!")
            saveData = False

        if oldPwd == "" and newPwd1 == "" and newPwd2 == "":
            newPassword = False
            logger.info("Nem került új jelszó megadásra!")
        else:
            if oldPwd == "" and newPwd1 != "" and newPwd2 != "":
                errorMessage("Nem adta meg a régi jelszót!")
                saveData = False

            if oldPwd != "":
                if not checkPassword(oldPwd, storedPwd):
                    errorMessage("A régi jelszó nem egyezik!")
                    saveData = False
                elif oldPwd == newPwd1:
                    errorMessage("Nem adhatja meg újra a régi jelszót!")
                    saveData = False

                if calculateStrength(newPwd1) == 0:
                    errorMessage("A jelszó nem megfelelő erősségű!")
                    saveData = False

                if newPwd1 != newPwd2:
                    errorMessage("Az új jelszavak nem egyeznek!")
                    saveData = False

                newPassword = True

        if saveData:
            if self.imagePath != "../resources/pictures/userDefault.png" and self.imagePath != self.oldImage:
                randomNumber = random.randint(1000, 9999)
                currentTime = datetime.now()
                formattedTime = currentTime.strftime("%Y%m%d_%H%M%S_") + f"{randomNumber}"

                pictureDirectory = "../../../userdata/profiles/profilepicture"
                os.makedirs(pictureDirectory, exist_ok=True)

                shutil.copy(self.imagePath,
                            f"../../../userdata/profiles/profilepicture/avatar_{formattedTime}.png")

                try:
                    os.remove(self.oldImage)
                    logger.info("Régi profilkép törlésre került!")
                except OSError as e:
                    errorMessage(f"Hiba: {e}")

                newImagePath = f"../userdata/profiles/profilepicture/avatar_{formattedTime}.png"

                """Elég csak a jelszót vizsgálni, mert az titkosított,
                így nem lehet a beolvasottal egyszerűen felülírni."""
                if newPassword:
                    overWrite(username, userAge, newImagePath, newPwd1)
                else:
                    overWrite(username, userAge, newImagePath)
            elif self.imagePath == "../resources/pictures/userDefault.png" and self.imagePath != self.oldImage:

                try:
                    os.remove(self.oldImage)
                    logger.info("Régi profilkép törlésre került!")
                except OSError as e:
                    errorMessage(f"Hiba: {e}")

                if newPassword:
                    overWrite(username, userAge, self.imagePath, newPwd1)
                else:
                    overWrite(username, userAge, self.imagePath)
            else:
                if newPassword:
                    overWrite(username, userAge, storedPPath, newPwd1)
                else:
                    overWrite(username, userAge, storedPPath)

            self.parent.refreshWindow()
            self.close()

            logger.info("Adatok mentve!")

    def handleResultsDeletion(self, result, username):
        if result == "Yes":
            self.resultsDeletion(username)

    def resultsDeletion(self, username):
        dataPath = "../../../userdata/profiles/profiles.json"
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

    def handleProfileDeletion(self, result, username):
        if result == "Yes":
            self.userDeletion(username)

    def userDeletion(self, username):
        dataPath = "../../../userdata/profiles/profiles.json"
        try:
            with open(dataPath, 'r') as jsonFile:
                fileContents = json.load(jsonFile)

            if username in fileContents:
                profilePictureDeletion = fileContents[username]["ProfilePicturePath"]

                if profilePictureDeletion != "../resources/pictures/userDefault.png":
                    profilePictureDeletion = "../../" + profilePictureDeletion
                    try:
                        os.remove(profilePictureDeletion)
                        logger.info("Profilkép törlésre került!")
                    except OSError as e:
                        errorMessage(f"Hiba: {e}")

                del fileContents[username]

            with open(dataPath, 'w') as json_file:
                json.dump(fileContents, json_file, indent=4)

            logger.info("Felhasználó sikeresen törölve!")

            self.close()
            self.parent.close()
            self.openLoginUI()

        except Exception as e:
            errorMessage(f"Hiba: {e}")

    def openLoginUI(self):
        if not self.loginWindow:
            self.loginWindow = loginScreen.LoginScreenUI()
        self.loginWindow.show()
        logger.info("Bejelentkezési képernyő megnyitásra került!")
        self.hide()
