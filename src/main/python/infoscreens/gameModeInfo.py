from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal


class GameModeInfoUI(QMainWindow):
    finished = pyqtSignal(str)

    def __init__(self, question, theme = "default"):
        super(GameModeInfoUI, self).__init__()
        loadUi(f"../resources/ui/{theme}/gameModeInfo.ui", self)
        self.setWindowIcon(QIcon("../../resources/icon/icon.ico"))

        self.infoLabel = self.findChild(QLabel, "infoLabel")
        self.backButton = self.findChild(QPushButton, "backButton")
        self.nextButton = self.findChild(QPushButton, "nextButton")

        self.infoLabel.setText(question)

        self.backButton.clicked.connect(self.backButtonClick)
        self.nextButton.clicked.connect(self.nextButtonClick)

    def backButtonClick(self):
        self.finished.emit("No")
        self.close()

    def nextButtonClick(self):
        self.finished.emit("Yes")
        self.close()
