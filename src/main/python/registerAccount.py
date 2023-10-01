import shutil
import datetime

from PyQt6 import QtCore
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QFrame, QFileDialog, QLabel, QMessageBox
from PyQt6.QtGui import QPixmap

import welcomeScreen
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

    def openWelcomeUI(self):
        if not self.welcomeWindow:
            self.welcomeWindow = welcomeScreen.WelcomeUI()
        self.welcomeWindow.show()
        self.hide()

    def registerUser(self):
        username = self.inputUserName.text().strip()
        userAge = self.inputUserAge.text().strip()
        password1 = self.inputPwd1.text().strip()
        password2 = self.inputPwd2.text().strip()

        saveData = True

        errorDialog = QMessageBox(self)
        errorDialog.setWindowTitle("Hiba!")

        if len(username) == 0:
            errorMessage = "Nem adott meg felhasználónevet!"
            errorDialog.setIcon(QMessageBox.Icon.Critical)
            errorDialog.setText(errorMessage)
            errorDialog.exec()
            saveData = False
        elif len(userAge) == 0:
            errorMessage = "Nem adott meg életkort!"
            errorDialog.setIcon(QMessageBox.Icon.Critical)
            errorDialog.setText(errorMessage)
            errorDialog.exec()
            saveData = False
        elif len(password1) == 0 and len(password2) == 0 or password1 != password2:
            errorMessage = "A megadott jelszó hiányzik, vagy nem egyezik!"
            errorDialog.setIcon(QMessageBox.Icon.Critical)
            errorDialog.setText(errorMessage)
            errorDialog.exec()
            saveData = False
        else:
            saveData = True

        if saveData:
            if self.imagePath != "../resources/pictures/userDefault.png":
                currentTime = datetime.datetime.now().time()
                formattedTime = currentTime.strftime("%H%M%S")
                shutil.copy(self.imagePath,
                            f"../../../userdata/profiles/profilepicture/avatar_{formattedTime}.png")
                newImagePath = f"../userdata/profiles/profilepicture/avatar_{formattedTime}.png"

                if createAccount(username, userAge, password2, newImagePath):
                    createAccount(username, userAge, password2, newImagePath)
                else:
                    errorMessage = "A megadott felhasználónév foglalt!"
                    errorDialog.setIcon(QMessageBox.Icon.Critical)
                    errorDialog.setText(errorMessage)
                    errorDialog.exec()

            else:
                if createAccount(username, userAge, password2, self.imagePath):
                    createAccount(username, userAge, password2, self.imagePath)
                else:
                    errorMessage = "A megadott felhasználónév foglalt!"
                    errorDialog.setIcon(QMessageBox.Icon.Critical)
                    errorDialog.setText(errorMessage)
                    errorDialog.exec()
