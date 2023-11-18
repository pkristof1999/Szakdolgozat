import shutil
import random

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLineEdit, QFrame, QFileDialog, QLabel, QPushButton, QMainWindow
from PyQt6.uic import loadUi
from datetime import datetime

from src.main.python import welcomeScreen
from src.main.python.infoscreens import registerSuccess
from src.main.python.components.createAccount import createAccount
from src.main.python.components.isConvertible import convertibleToInt
from src.main.python.components import checkPwdStrenght
from src.main.python.components.logger import *
from src.main.python.components.errorMessage import errorMessage


class RegisterAccountUI(QMainWindow):
    def __init__(self):
        super(RegisterAccountUI, self).__init__()
        loadUi("../resources/ui/default/registerAccount.ui", self)

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
            pixmap = QPixmap("../resources/pictures/userDefault.png")

            if not os.path.exists("../resources/pictures/userDefault.png"):
                raise Exception("A megadott kép nem található!")

            frameSize = self.profilePicture.size()
            pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                   QtCore.Qt.TransformationMode.SmoothTransformation)

            self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.label.setGeometry(self.profilePicture.rect())
            self.label.setPixmap(pixmap)
            logger.info("Alap profilkép betöltésre került!")

        except Exception as e:
            logger.error(f"Hiba: {e}")

    def registerUser(self):
        message = ""

        username = self.inputUserName.text().strip()
        userAge = self.inputUserAge.text().strip()
        password1 = self.inputPwd1.text().strip()
        password2 = self.inputPwd2.text().strip()

        chkPwd = checkPwdStrenght.calculateStrength(password1)

        saveData = True

        if username == "Vendég":
            if message == "":
                message = message + "Ezt a felhasználónevet nem lehet választani!"
            else:
                message = message + "\nEzt a felhasználónevet nem lehet választani!"
            saveData = False

        if len(username) == 0:
            if message == "":
                message = message + "Nem adott meg felhasználónevet!"
            else:
                message = message + "\nNem adott meg felhasználónevet!"
            saveData = False

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

        if len(password1) == 0 or len(password2) == 0:
            if message == "":
                message = message + "Jelszó mező nincs kitöltve!"
            else:
                message = message + "\nJelszó mező nincs kitöltve!"
            saveData = False

        if password1 != password2:
            if message == "":
                message = message + "A jelszavak nem egyeznek!"
            else:
                message = message + "\nA jelszavak nem egyeznek!"
            saveData = False

        if chkPwd == 0:
            if message == "":
                message = message + "A jelszó nem megfelelő erősségű!"
            else:
                message = message + "\nA jelszó nem megfelelő erősségű!"
            saveData = False

        if message != "":
            errorMessage(message)

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
                    self.openRegisterSuccessUI()
                else:
                    errorMessage("A megadott felhasználónév foglalt!")

            else:
                if createAccount(username, int(userAge), password2, self.imagePath):
                    createAccount(username, int(userAge), password2, self.imagePath)
                    logger.warning("Profilkép nem került feltöltésre!")
                    logger.info("Sikeres regisztráció!")
                    self.openRegisterSuccessUI()
                else:
                    errorMessage("A megadott felhasználónév foglalt!")

    def setPwd1Color(self):
        password = self.inputPwd1.text().strip()
        chkPwd = checkPwdStrenght.calculateStrength(password)

        if chkPwd == 0:
            self.inputPwd1.setStyleSheet(checkPwdStrenght.changeColor("red"))
        elif 0 < chkPwd < 5:
            self.inputPwd1.setStyleSheet(checkPwdStrenght.changeColor("orange"))
        elif chkPwd >= 5:
            self.inputPwd1.setStyleSheet(checkPwdStrenght.changeColor("green"))

        self.setPwd2Color()

    def setPwd2Color(self):
        password1 = self.inputPwd1.text().strip()
        password2 = self.inputPwd2.text().strip()
        chkPwd = checkPwdStrenght.calculateStrength(password1)

        if password1 != password2 or chkPwd == 0:
            self.inputPwd2.setStyleSheet(checkPwdStrenght.changeColor("red"))
        else:
            self.inputPwd2.setStyleSheet(checkPwdStrenght.changeColor("green"))

    def openWelcomeUI(self):
        if not self.welcomeWindow:
            self.welcomeWindow = welcomeScreen.WelcomeUI()
        self.welcomeWindow.show()
        logger.info("Visszalépés az indítóképernyőre.")
        self.close()

    def openRegisterSuccessUI(self):
        if not self.registerWindow:
            self.registerWindow = registerSuccess.RegisterSuccessUI()
        self.registerWindow.show()
        logger.info("Sikeres regisztráció ablak megnyitása.")
        self.close()
