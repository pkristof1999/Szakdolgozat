from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel


class AreYouSureUI(QMainWindow):
    def __init__(self, question):
        super(AreYouSureUI, self).__init__()
        loadUi("../resources/ui/default/areYouSure.ui", self)

        self.questionLabel = self.findChild(QLabel, "questionLabel")
        self.noButton = self.findChild(QPushButton, "noButton")
        self.yesButton = self.findChild(QPushButton, "yesButton")

        self.questionLabel.setText(question)

        self.noButton.clicked.connect(self.noButtonClick)
        self.yesButton.clicked.connect(self.yesButtonClick)

    def noButtonClick(self):
        self.close()

    def yesButtonClick(self):
        self.close()
