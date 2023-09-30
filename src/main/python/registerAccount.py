import welcomeScreen

from PyQt6 import QtCore
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QFrame, QFileDialog, QLabel, QMessageBox
from PyQt6.QtGui import QPixmap

from components.createAccount import createAccount


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
            selected_files = fileDialog.selectedFiles()
            if selected_files:
                self.imagePath = selected_files[0]
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

        saveData = False

        error_dialog = QMessageBox(self)
        error_dialog.setWindowTitle("Hiba!")

        if username == "":
            error_message = "Nem adott meg felhasználónevet!"
            error_dialog.setIcon(QMessageBox.Icon.Critical)
            error_dialog.setText(error_message)
            error_dialog.exec()
            saveData = False
        elif userAge == "":
            error_message = "Nem adott meg életkort!"
            error_dialog.setIcon(QMessageBox.Icon.Critical)
            error_dialog.setText(error_message)
            error_dialog.exec()
            saveData = False
        elif password1 == "" and password2 == "":
            error_message = "Nem adott meg jelszót!"
            error_dialog.setIcon(QMessageBox.Icon.Critical)
            error_dialog.setText(error_message)
            error_dialog.exec()
            saveData = False
        else:
            saveData = True

        if password1 != password2:
            error_message = "A megadott jelszavak nem egyeznek!"
            error_dialog.setIcon(QMessageBox.Icon.Critical)
            error_dialog.setText(error_message)
            error_dialog.exec()
            saveData = False
        else:
            saveData = True

        if saveData:
            createAccount(username, userAge, password2, self.imagePath)
