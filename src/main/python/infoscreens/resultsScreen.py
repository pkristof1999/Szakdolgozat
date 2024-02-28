from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel


class ResultsScreenUI(QMainWindow):

    def __init__(self, info, parent, grandParent, theme):
        super(ResultsScreenUI, self).__init__()

        self.theme = theme
        loadUi(f"src/main/resources/ui/{self.theme}/{self.theme}ResultsScreen.ui", self)
        self.setWindowIcon(QIcon("src/main/resources/icon/icon.ico"))

        self.setFixedSize(self.size())

        self.parent = parent
        self.grandParent = grandParent

        self.infoLabel = self.findChild(QLabel, "infoLabel")
        self.nextButton = self.findChild(QPushButton, "nextButton")

        self.infoLabel.setText(info.replace("  ", ""))
        self.infoLabel.setWordWrap(True)

        self.nextButton.clicked.connect(self.nextButtonClick)

        self.closeEvent = grandParent.exitWindow

    def nextButtonClick(self):
        self.hide()
        self.grandParent.show()
