import json

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QPushButton, QMainWindow, QComboBox, QLabel, QFileDialog, QLineEdit, QMessageBox
from PyQt6.uic import loadUi

from src.main.python.components.logger import *
from src.main.python.components import clickableComboBox
from src.main.python.infoscreens import areYouSure
from src.main.python.components.checkPwdStrenght import *
from src.main.python.components.securePwd import *
from src.main.python.components.overwriteAccount import overwriteAccount as overWrite


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
            lambda: self.openQuestionWindow("Biztosan lecseréli\na profilképét?",
                                            self.handleProfilePictureChange
                                            )
        )
        self.deleteProfilePictureButton.clicked.connect(
            lambda: self.openQuestionWindow("Biztos benne, hogy törli\na profilképet?",
                                            self.handleProfilePictureDeletion
                                            )
        )

        self.newPassword1.textChanged.connect(self.changeNewPassword1)
        self.newPassword2.textChanged.connect(self.changeNewPassword2)

        self.abortButton.clicked.connect(self.abortAndCloseSettings)
        self.saveAndCloseButton.clicked.connect(lambda : self.saveAndCloseSettings(username))

        self.imagePath = self.getImagePath(username)
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

    def openQuestionWindow(self, question, handler):
        self.questionWindow = None
        if not self.questionWindow:
            self.questionWindow = areYouSure.AreYouSureUI(question)

        self.questionWindow.finished.connect(handler)
        self.questionWindow.show()

    def handleProfilePictureDeletion(self, result):
        if result == "Yes":
            self.loadDefaultImage()

    def handleProfilePictureChange(self, result):
        if result == "Yes":
            self.addPicture()

    """def checkOldPassword(self, username):
        dataPath = "../../userdata/profiles/profiles.json"

        oldPassword = self.oldPassword.text().strip()

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r') as jsonFile:
                    fileContents = jsonFile.read()
                    existingAccounts = json.loads(fileContents)
                    storedPassword = existingAccounts[username]["Password"]

        except Exception as e:
            self.errorMessage(f"Hiba: {e}")

        if checkPassword(oldPassword, storedPassword):
            return True
        else:
            return False"""

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

    def saveAndCloseSettings(self, username):
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

        except Exception as e:
            self.errorMessage(f"Hiba: {e}")

        saveData = True

        if oldPwd == "" and newPwd1 != "" and newPwd2 != "":
            self.errorMessage("Nem adta meg a régi jelszót!")
            saveData = False

        if oldPwd != "":
            if not checkPassword(oldPwd, storedPwd):
                print(checkPassword(oldPwd, storedPwd))
                self.errorMessage("A régi jelszó nem egyezik!")
                saveData = False

            if calculateStrength(newPwd1) == 0:
                self.errorMessage("A jelszó nem megfelelő erősségű!")
                saveData = False

            if newPwd1 != newPwd2:
                self.errorMessage("Az új jelszavak nem egyeznek!")
                saveData = False

        if saveData:
            self.errorMessage("Sikeres mentés :)")
            overWrite(username, userAge, newPwd1, newProfilePicturePath)

            self.close()
            self.parent.repaint()

    def errorMessage(self, message):
        logger.error(message)
        errorDialog = QMessageBox(self)
        errorDialog.setWindowTitle("Hiba!")
        errorDialog.setIcon(QMessageBox.Icon.Critical)
        errorDialog.setText(message)
        errorDialog.exec()
