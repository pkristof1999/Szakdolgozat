from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QPushButton, QMainWindow, QButtonGroup
from PyQt6.uic import loadUi

from src.main.python.components.logger import *
from src.main.python.infoscreens.errorMessage import errorMessage


class LearningWindowQuestionUI(QMainWindow):
    finished = pyqtSignal(str)

    def __init__(self, username, parent):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            self.username = username
            default = "default"

            super(LearningWindowQuestionUI, self).__init__()
            self.setWindowIcon(QIcon("../resources/icon/icon.ico"))
            loadUi(f"../resources/ui/{default}/learningWindowQuestion.ui", self)

            self.setFixedSize(self.size())

            self.parent = parent

            self.questionField = self.findChild(QLabel, "questionField")
            self.answer1Button = self.findChild(QPushButton, "answer1Button")
            self.answer2Button = self.findChild(QPushButton, "answer2Button")
            self.answer3Button = self.findChild(QPushButton, "answer3Button")
            self.backButton = self.findChild(QPushButton, "backButton")
            self.nextButton = self.findChild(QPushButton, "nextButton")

            self.resultsWindow = None

            self.answerButtonGroup = QButtonGroup(self)
            self.answerButtonGroup.setExclusive(False)
            self.answerButtonGroup.addButton(self.answer1Button)
            self.answerButtonGroup.addButton(self.answer2Button)
            self.answerButtonGroup.addButton(self.answer3Button)

            self.answerButtonGroup.buttonClicked.connect(self.handleAnswerSelection)

            self.nextButton.clicked.connect(self.acceptAnswer)
            self.backButton.clicked.connect(self.declineAnswer)

        except Exception as e:
            errorMessage(e)
            self.hide()

    def handleAnswerSelection(self, selectedButton):
        for button in self.answerButtonGroup.buttons():
            if button is not selectedButton:
                button.setChecked(False)
                button.setStyleSheet("""
                                     * {
                                         background-color: white;
                                         color: grey;
                                     }

                                     *:hover {
                                         background-color: rgb(120, 120, 220);
                                         color: white;
                                     }
                                     """)

        if selectedButton.isChecked():
            logger.info(f"{selectedButton.text()} megjelölve válaszként.")
            selectedButton.setStyleSheet("""
                                             * {
                                                 background-color: rgb(120, 120, 220);
                                                 color: white;
                                             }
                                             """
                                         )

    def declineAnswer(self):
        self.finished.emit("Back")
        self.parent.show()
        self.hide()

    def acceptAnswer(self):
        if self.answer1Button.isChecked() or \
                self.answer2Button.isChecked() or \
                self.answer3Button.isChecked():
            self.finished.emit("Next")
            self.parent.show()
            self.hide()
        else:
            errorMessage("Nem választott választ!")
