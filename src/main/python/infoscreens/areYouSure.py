from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal


class AreYouSureUI(QMainWindow):
    finished = pyqtSignal(str)

    def __init__(self, question, theme = "default"):
        super(AreYouSureUI, self).__init__()

        self.theme = theme
        loadUi(f"src/main/resources/ui/{self.theme}/{self.theme}AreYouSure.ui", self)
        self.setWindowIcon(QIcon("src/main/resources/icon/icon.ico"))

        self.setFixedSize(self.size())

        self.questionLabel = self.findChild(QLabel, "questionLabel")
        self.noButton = self.findChild(QPushButton, "noButton")
        self.yesButton = self.findChild(QPushButton, "yesButton")

        self.questionLabel.setText(question)

        self.noButton.clicked.connect(self.noButtonClick)
        self.yesButton.clicked.connect(self.yesButtonClick)

    def noButtonClick(self):
        self.finished.emit("No")
        self.hide()

    def yesButtonClick(self):
        self.finished.emit("Yes")
        self.hide()
