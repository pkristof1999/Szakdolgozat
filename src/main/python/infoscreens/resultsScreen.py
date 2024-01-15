from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel


class ResultsScreenUI(QMainWindow):

    def __init__(self, info, grandParent, theme="default"):
        super(ResultsScreenUI, self).__init__()
        loadUi(f"../resources/ui/{theme}/resultsScreen.ui", self)
        self.setWindowIcon(QIcon("../resources/icon/icon.ico"))

        self.setFixedSize(self.size())

        self.grandParent = grandParent

        self.infoLabel = self.findChild(QLabel, "infoLabel")
        self.nextButton = self.findChild(QPushButton, "nextButton")

        self.infoLabel.setText(info.replace("  ", ""))
        self.infoLabel.setWordWrap(True)

        self.nextButton.clicked.connect(self.nextButtonClick)

        self.closeEvent = grandParent.exitWindow

    def nextButtonClick(self):
        self.grandParent.show()
        self.hide()