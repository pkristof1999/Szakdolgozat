from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal


class ResultsScreenUI(QMainWindow):
    finished = pyqtSignal(str)

    def __init__(self, question, theme="default"):
        super(ResultsScreenUI, self).__init__()
        loadUi(f"../resources/ui/{theme}/resultsScreen.ui", self)
        self.setWindowIcon(QIcon("../resources/icon/icon.ico"))

        self.setFixedSize(self.size())

        self.infoLabel = self.findChild(QLabel, "infoLabel")
        self.nextButton = self.findChild(QPushButton, "nextButton")

        self.infoLabel.setText(question.replace("  ", ""))
        self.infoLabel.setWordWrap(True)

        self.nextButton.clicked.connect(self.nextButtonClick)

    def nextButtonClick(self):
        self.finished.emit("Next")
        self.hide()
