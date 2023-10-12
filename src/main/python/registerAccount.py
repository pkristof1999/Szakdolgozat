import shutil
import random

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLineEdit, QFrame, QFileDialog, QLabel, QMessageBox, QPushButton, QMainWindow
from PyQt6.uic import loadUi
from datetime import datetime

from src.main.python import welcomeScreen
from src.main.python.infoscreens import registerSuccess
from src.main.python.components.createAccount import createAccount
from src.main.python.components.isConvertible import convertibleToInt
from src.main.python.components import checkPwdStrenght
from src.main.python.components.logger import *


class RegisterAccountUI(QMainWindow):
    def __init__(self):
        super(RegisterAccountUI, self).__init__()
        loadUi("../resources/ui/registerAccount.ui", self)

        self.backButton = self.findChild(QPushButton, "backButton")
        self.registerButton = self.findChild(QPushButton, "registerButton")
        self.addPictureButton = self.findChild(QPushButton, "addPictureButton")
        self.removePictureButton = self.findChild(QPushButton, "removePictureButton")
        self.inputUserName = self.findChild(QLineEdit, "inputUserName")
        self.inputUserAge = self.findChild(QLineEdit, "inputUserAge")
        self.inputPwd1 = self.findChild(QLineEdit, "inputPwd1")
        self.inputPwd2 = self.findChild(QLineEdit, "inputPwd2")
        self.profilePicture = self.findChild(QFrame, "profilePicture")

        self.imagePath = "../resources/pictures/userDefault.png"
        self.label = QLabel(self.profilePicture)

        self.welcomeWindow = None
        self.registerWindow = None

        self.addPictureButton.clicked.connect(self.addPicture)
        self.removePictureButton.clicked.connect(self.loadDefaultImage)
        self.backButton.clicked.connect(self.openWelcomeUI)
        self.registerButton.clicked.connect(self.registerUser)

        self.inputPwd1.textChanged.connect(self.setPwd1Color)
        self.inputPwd2.textChanged.connect(self.setPwd2Color)

        self.loadDefaultImage()

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
                logger.info("Profilkép kiválasztásra került!")

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

    def setRegisterDataToDefault(self):
        self.loadDefaultImage()
        self.inputUserName.setText("")
        self.inputUserAge.setText("")
        self.inputPwd1.setText("")
        self.inputPwd2.setText("")
        self.inputPwd1.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.inputPwd2.setStyleSheet("background-color: rgb(255, 255, 255);")

    def registerUser(self):
        username = self.inputUserName.text().strip()
        userAge = self.inputUserAge.text().strip()
        password1 = self.inputPwd1.text().strip()
        password2 = self.inputPwd2.text().strip()

        chkPwd = checkPwdStrenght.calculateStrength(password1)

        saveData = True

        if len(username) == 0:
            self.errorMessage("Nem adott meg felhasználónevet!")
            saveData = False

        if len(userAge) == 0:
            self.errorMessage("Nem adott meg életkort!")
            saveData = False

        if convertibleToInt(userAge):
            userAge = int(userAge)
            if 1 > userAge or 150 < userAge:
                self.errorMessage("Nem adható meg ilyen életkor!")
                saveData = False

        if not convertibleToInt(userAge):
            self.errorMessage("Nem egész szám a megadott életkor!")
            saveData = False

        if len(password1) == 0 or len(password2) == 0:
            self.errorMessage("Jelszó mező nincs kitöltve!")
            saveData = False

        if password1 != password2:
            self.errorMessage("A jelszavak nem egyeznek!")
            saveData = False

        if chkPwd == 0:
            self.errorMessage("A jelszó nem megfelelő erősségű!")
            saveData = False

        if saveData:
            if self.imagePath != "../resources/pictures/userDefault.png":
                randomNumber = random.randint(1000, 9999)
                currentTime = datetime.now()
                formattedTime = currentTime.strftime("%Y%m%d_%H%M%S_") + f"{randomNumber}"

                pictureDirectory = "../../../userdata/profiles/profilepicture"
                os.makedirs(pictureDirectory, exist_ok=True)

                shutil.copy(self.imagePath,
                            f"../../../userdata/profiles/profilepicture/avatar_{formattedTime}.png")
                newImagePath = f"../userdata/profiles/profilepicture/avatar_{formattedTime}.png"

                if createAccount(username, int(userAge), password2, newImagePath):
                    createAccount(username, int(userAge), password2, newImagePath)
                    logger.info("Sikeres regisztráció!")
                    self.setRegisterDataToDefault()
                    self.openRegisterSuccessUI()
                else:
                    self.errorMessage("A megadott felhasználónév foglalt!")

            else:
                if createAccount(username, int(userAge), password2, self.imagePath):
                    createAccount(username, int(userAge), password2, self.imagePath)
                    logger.warning("Profilkép nem került feltöltésre!")
                    logger.info("Sikeres regisztráció!")
                    self.setRegisterDataToDefault()
                    self.openRegisterSuccessUI()
                else:
                    self.errorMessage("A megadott felhasználónév foglalt!")

    def setPwd1Color(self):
        password = self.inputPwd1.text().strip()
        chkPwd = checkPwdStrenght.calculateStrength(password)

        if chkPwd == 0:
            self.inputPwd1.setStyleSheet("background-color: rgb(255, 173, 173);")
        elif 0 < chkPwd < 5:
            self.inputPwd1.setStyleSheet("background-color: rgb(255, 203, 111);")
        elif chkPwd >= 5:
            self.inputPwd1.setStyleSheet("background-color: rgb(167, 255, 111);")

        self.setPwd2Color()

    def setPwd2Color(self):
        password1 = self.inputPwd1.text().strip()
        password2 = self.inputPwd2.text().strip()
        chkPwd = checkPwdStrenght.calculateStrength(password1)

        if password1 != password2 or chkPwd == 0:
            self.inputPwd2.setStyleSheet("background-color: rgb(255, 173, 173);")
        else:
            self.inputPwd2.setStyleSheet("background-color: rgb(167, 255, 111);")

    def openWelcomeUI(self):
        if not self.welcomeWindow:
            self.welcomeWindow = welcomeScreen.WelcomeUI()
        self.welcomeWindow.show()
        logger.info("Visszalépés az indítóképernyőre.")
        self.hide()

    def openRegisterSuccessUI(self):
        if not self.registerWindow:
            self.registerWindow = registerSuccess.RegisterSuccessUI(self)
        self.registerWindow.show()
        logger.info("Sikeres regisztráció ablak megnyitása.")

    def errorMessage(self, message):
        logger.error(message)
        errorDialog = QMessageBox(self)
        errorDialog.setWindowTitle("Hiba!")
        errorDialog.setIcon(QMessageBox.Icon.Critical)
        errorDialog.setText(message)
        errorDialog.exec()
