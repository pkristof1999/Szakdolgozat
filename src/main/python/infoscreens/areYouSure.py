from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal


class AreYouSureUI(QMainWindow):
    finished = pyqtSignal(str)

    def __init__(self, question, theme = "default"):
        super(AreYouSureUI, self).__init__()
        loadUi(f"../resources/ui/{theme}/areYouSure.ui", self)

        self.questionLabel = self.findChild(QLabel, "questionLabel")
        self.noButton = self.findChild(QPushButton, "noButton")
        self.yesButton = self.findChild(QPushButton, "yesButton")

        self.questionLabel.setText(question)

        self.noButton.clicked.connect(self.noButtonClick)
        self.yesButton.clicked.connect(self.yesButtonClick)

    def noButtonClick(self):
        self.finished.emit("No")
        self.close()

    def yesButtonClick(self):
        self.finished.emit("Yes")
        self.close()
