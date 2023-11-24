from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QFrame, QStyle, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt

from src.main.python.components.logger import *


class GameModeInfoUI(QMainWindow):
    finished = pyqtSignal(str)

    def __init__(self, question, theme = "default"):
        super(GameModeInfoUI, self).__init__()
        loadUi(f"../resources/ui/{theme}/gameModeInfo.ui", self)
        self.setWindowIcon(QIcon("../resources/icon/icon.ico"))

        self.setFixedSize(self.size())

        self.infoFrame = self.findChild(QFrame, "infoFrame")
        self.infoLabel = self.findChild(QLabel, "infoLabel")
        self.backButton = self.findChild(QPushButton, "backButton")
        self.nextButton = self.findChild(QPushButton, "nextButton")

        self.label = QLabel(self.infoFrame)

        self.infoLabel.setText(question)

        self.backButton.clicked.connect(self.backButtonClick)
        self.nextButton.clicked.connect(self.nextButtonClick)

        self.loadInfoIcon()

    def loadInfoIcon(self):
        try:
            infoIcon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
            pixmap = infoIcon.pixmap(infoIcon.availableSizes()[1])
            self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.label.setGeometry(self.infoFrame.rect())
            self.label.setPixmap(pixmap)

        except Exception as e:
            logger.error(f"Hiba: {e}")

    def backButtonClick(self):
        self.finished.emit("No")
        self.close()

    def nextButtonClick(self):
        self.finished.emit("Yes")
        self.close()
