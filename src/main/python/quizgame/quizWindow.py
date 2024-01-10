from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QPushButton, QMainWindow
from PyQt6.uic import loadUi

from src.main.python.infoscreens.errorMessage import errorMessage


class QuizWindowUI(QMainWindow):
    def __init__(self, parent, username, grandParent):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            self.username = username
            default = "default"

            super(QuizWindowUI, self).__init__()
            self.setWindowIcon(QIcon("../resources/icon/icon.ico"))
            loadUi(f"../resources/ui/{default}/learnWindow.ui", self)

            self.setFixedSize(self.size())

            self.parent = parent
            self.grandParent = grandParent

            self.questionField = self.findChild(QLabel, "questionField")
            self.answer1Button = self.findChild(QPushButton, "answer1Button")
            self.answer2Button = self.findChild(QPushButton, "answer2Button")
            self.answer3Button = self.findChild(QPushButton, "answer3Button")
            self.answer4Button = self.findChild(QPushButton, "answer4Button")
            self.backButton = self.findChild(QPushButton, "backButton")
            self.nextButton = self.findChild(QPushButton, "nextButton")

            self.backButton.clicked.connect(lambda: self.closeLearnWindow(parent, grandParent))

        except Exception as e:
            errorMessage(e)
            self.hide()

    def closeLearnWindow(self, parent, grandParent):
        parent.show()
        grandParent.show()
        parent.raise_()
        self.hide()
