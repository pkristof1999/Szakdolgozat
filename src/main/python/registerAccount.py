import os
import shutil
import datetime

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLineEdit, QFrame, QFileDialog, QLabel, QMessageBox, QPushButton, QMainWindow
from PyQt6.uic import loadUi

from src.main.python import welcomeScreen
from src.main.python.components.logger import *
from src.main.python.infoscreens import registerSuccess
from src.main.python.components.createAccount import createAccount


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

    def openWelcomeUI(self):
        if not self.welcomeWindow:
            self.welcomeWindow = welcomeScreen.WelcomeUI()
        self.welcomeWindow.show()
        logger.info("Visszalépés az indítóképernyőre.")
        self.hide()

    def openRegisterSuccessUI(self):
        if not self.registerWindow:
            self.registerWindow = registerSuccess.RegisterSuccessUI()
        self.registerWindow.show()
        logger.info("Sikeres regisztráció ablak megnyitása.")

    def registerUser(self):
        username = self.inputUserName.text().strip()
        userAge = self.inputUserAge.text().strip()
        password1 = self.inputPwd1.text().strip()
        password2 = self.inputPwd2.text().strip()

        saveData = True

        errorDialog = QMessageBox(self)
        errorDialog.setWindowTitle("Hiba!")

        if len(username) == 0:
            logger.error("Nem adott meg felhasználónevet!")
            errorMessage = "Nem adott meg felhasználónevet!"
            errorDialog.setIcon(QMessageBox.Icon.Critical)
            errorDialog.setText(errorMessage)
            errorDialog.exec()
            saveData = False

        if len(userAge) == 0:
            logger.error("Nem adott meg életkort!")
            errorMessage = "Nem adott meg életkort!"
            errorDialog.setIcon(QMessageBox.Icon.Critical)
            errorDialog.setText(errorMessage)
            errorDialog.exec()
            saveData = False

        if convertibleToInt(userAge):
            userAge = int(userAge)
            if 1 > userAge or 150 < userAge:
                logger.error("Nem adható meg ilyen életkor!")
                errorMessage = "Nem adható meg ilyen életkor!"
                errorDialog.setIcon(QMessageBox.Icon.Critical)
                errorDialog.setText(errorMessage)
                errorDialog.exec()
                saveData = False

        if not convertibleToInt(userAge):
            logger.error("Nem egész szám a megadott életkor!")
            errorMessage = "Nem egész szám a megadott életkor!"
            errorDialog.setIcon(QMessageBox.Icon.Critical)
            errorDialog.setText(errorMessage)
            errorDialog.exec()
            saveData = False

        if len(password1) == 0 or len(password2) == 0:
            logger.error("Jelszó mező nincs kitöltve!")
            errorMessage = "Jelszó mező nincs kitöltve!"
            errorDialog.setIcon(QMessageBox.Icon.Critical)
            errorDialog.setText(errorMessage)
            errorDialog.exec()
            saveData = False

        if password1 != password2:
            logger.error("A jelszavak nem egyeznek!")
            errorMessage = "A jelszavak nem egyeznek!"
            errorDialog.setIcon(QMessageBox.Icon.Critical)
            errorDialog.setText(errorMessage)
            errorDialog.exec()
            saveData = False

        if saveData:
            if self.imagePath != "../resources/pictures/userDefault.png":
                currentTime = datetime.datetime.now().time()
                formattedTime = currentTime.strftime("%H%M%S")

                pictureDirectory = "../../../userdata/profiles/profilepicture"
                os.makedirs(pictureDirectory, exist_ok=True)

                shutil.copy(self.imagePath,
                            f"../../../userdata/profiles/profilepicture/avatar_{formattedTime}.png")
                newImagePath = f"../userdata/profiles/profilepicture/avatar_{formattedTime}.png"

                if createAccount(username, int(userAge), password2, newImagePath):
                    createAccount(username, int(userAge), password2, newImagePath)
                    logger.info("Sikeres regisztráció!")
                    self.openRegisterSuccessUI()
                    if registerSuccess.loginClicked():
                        self.hide()
                else:
                    logger.error("A megadott felhasználónév foglalt!")
                    errorMessage = "A megadott felhasználónév foglalt!"
                    errorDialog.setIcon(QMessageBox.Icon.Critical)
                    errorDialog.setText(errorMessage)
                    errorDialog.exec()

            else:
                if createAccount(username, int(userAge), password2, self.imagePath):
                    createAccount(username, int(userAge), password2, self.imagePath)
                    logger.warning("Profilkép nem került feltöltésre!")
                    logger.info("Sikeres regisztráció!")
                    self.openRegisterSuccessUI()
                    print(registerSuccess.loginClicked())
                    if registerSuccess.loginClicked():
                        self.hide()
                else:
                    logger.error("A megadott felhasználónév foglalt!")
                    errorMessage = "A megadott felhasználónév foglalt!"
                    errorDialog.setIcon(QMessageBox.Icon.Critical)
                    errorDialog.setText(errorMessage)
                    errorDialog.exec()


def convertibleToInt(variable):
    try:
        variable = int(variable)
        return True
    except ValueError:
        return False
