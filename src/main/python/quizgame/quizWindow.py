from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QPushButton, QMainWindow, QButtonGroup
from PyQt6.uic import loadUi

from src.main.python.components.logger import *
from src.main.python.infoscreens.errorMessage import errorMessage


class QuizWindowUI(QMainWindow):
    def __init__(self, username, parent):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            self.username = username
            default = "default"

            super(QuizWindowUI, self).__init__()
            self.setWindowIcon(QIcon("../resources/icon/icon.ico"))
            loadUi(f"../resources/ui/{default}/quizScreen.ui", self)

            self.setFixedSize(self.size())

            self.parent = parent

            self.questionField = self.findChild(QLabel, "questionField")
            self.answer1Button = self.findChild(QPushButton, "answer1Button")
            self.answer2Button = self.findChild(QPushButton, "answer2Button")
            self.answer3Button = self.findChild(QPushButton, "answer3Button")
            self.answer4Button = self.findChild(QPushButton, "answer4Button")
            self.backButton = self.findChild(QPushButton, "backButton")
            self.nextButton = self.findChild(QPushButton, "nextButton")

            self.answerButtonGroup = QButtonGroup(self)
            self.answerButtonGroup.addButton(self.answer1Button)
            self.answerButtonGroup.addButton(self.answer2Button)
            self.answerButtonGroup.addButton(self.answer3Button)
            self.answerButtonGroup.addButton(self.answer4Button)

            self.answerButtonGroup.buttonClicked.connect(self.handleAnswerSelection)

            self.backButton.clicked.connect(lambda: self.closeQuizWindow(parent))

            self.closeEvent = parent.exitWindow

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
            selectedButton.setStyleSheet("""
                                         * {
                                             background-color: rgb(120, 120, 220);
	                                         color: white;
                                         }
                                         """
                                         )

    def closeQuizWindow(self, parent):
        parent.show()
        self.hide()
        logger.info("Kvíz játékmód bezárása!")
