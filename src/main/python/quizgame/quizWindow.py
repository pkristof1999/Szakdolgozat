import json
import random

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

            self.questionBank = []
            self.questionIndex = 0
            self.previousQuestions = []

            self.loadFirstQuestion()

            self.answerButtonGroup.buttonClicked.connect(self.handleAnswerSelection)

            self.nextButton.clicked.connect(self.nextQuestion)
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

    def loadQuestionsIntoArray(self):
        try:
            with open("../resources/quiz/questions.json", "r") as jsonFile:
                questionBank = json.load(jsonFile)

            shuffledQuestions = list(questionBank.values())
            random.shuffle(shuffledQuestions)

            return shuffledQuestions

        except Exception as e:
            errorMessage(e)

    def loadFirstQuestion(self):
        self.questionBank = self.loadQuestionsIntoArray()
        firstQuestion = self.questionBank[0]

        self.questionField.setText(firstQuestion["question"])
        self.answer1Button.setText(firstQuestion["answer1"])
        self.answer2Button.setText(firstQuestion["answer2"])
        self.answer3Button.setText(firstQuestion["answer3"])
        self.answer4Button.setText(firstQuestion["answer4"])

    def nextQuestion(self):
        self.questionIndex += 1
        if self.questionIndex < 10:
            print(self.questionIndex)
            nextQuestion = self.questionBank[self.questionIndex]

            self.questionField.setText(nextQuestion["question"])
            self.answer1Button.setText(nextQuestion["answer1"])
            self.answer2Button.setText(nextQuestion["answer2"])
            self.answer3Button.setText(nextQuestion["answer3"])
            self.answer4Button.setText(nextQuestion["answer4"])
        else:
            errorMessage("Nincs több kérdés :(")

    def closeQuizWindow(self, parent):
        parent.show()
        self.hide()
        logger.info("Kvíz játékmód bezárása!")
