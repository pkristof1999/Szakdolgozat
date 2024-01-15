import json
import time
import random
import threading

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QPushButton, QMainWindow, QButtonGroup
from PyQt6.uic import loadUi

from src.main.python.components.logger import *
from src.main.python.infoscreens import resultsScreen
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
            self.timerLabel = self.findChild(QLabel, "timerLabel")
            self.backButton = self.findChild(QPushButton, "backButton")
            self.nextButton = self.findChild(QPushButton, "nextButton")

            self.resultsWindow = None

            self.answerButtonGroup = QButtonGroup(self)
            self.answerButtonGroup.setExclusive(False)
            self.answerButtonGroup.addButton(self.answer1Button)
            self.answerButtonGroup.addButton(self.answer2Button)
            self.answerButtonGroup.addButton(self.answer3Button)
            self.answerButtonGroup.addButton(self.answer4Button)

            self.questionBank = []
            self.questionIndex = 0
            self.previousQuestions = []

            self.goodAnswers = 0

            self.terminateThread = threading.Event()
            self.timerThread = None
            self.countdown = 30

            self.startCountdown(self.countdown)

            self.loadFirstQuestion()

            self.answerButtonGroup.buttonClicked.connect(self.handleAnswerSelection)

            self.nextButton.clicked.connect(self.nextQuestion)
            self.backButton.clicked.connect(lambda: self.closeQuizWindow(parent))

            if self.closeEvent:
                self.terminateThread.set()
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
            logger.info(f"{selectedButton.text()} megjelölve válaszként.")
            selectedButton.setStyleSheet("""
                                         * {
                                             background-color: rgb(120, 120, 220);
	                                         color: white;
                                         }
                                         """
                                         )

    def setButtonsUnchecked(self):
        for button in self.answerButtonGroup.buttons():
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
        if self.answer1Button.isChecked() or \
                self.answer2Button.isChecked() or \
                self.answer3Button.isChecked() or \
                self.answer4Button.isChecked():

            self.questionIndex += 1
            if self.questionIndex <= 10:
                if self.questionIndex < 10:
                    for button in self.answerButtonGroup.buttons():
                        if button.isChecked():
                            logger.info(f"{button.text()} sikeresen leadva válaszként!")
                            if button.text() == self.questionBank[self.questionIndex]["rightAnswer"]:
                                self.goodAnswers += 1
                                print(self.goodAnswers)

                    nextQuestion = self.questionBank[self.questionIndex]

                    self.questionField.setText(nextQuestion["question"])
                    self.answer1Button.setText(nextQuestion["answer1"])
                    self.answer2Button.setText(nextQuestion["answer2"])
                    self.answer3Button.setText(nextQuestion["answer3"])
                    self.answer4Button.setText(nextQuestion["answer4"])
                else:
                    for button in self.answerButtonGroup.buttons():
                        if button.isChecked():
                            logger.info(f"{button.text()} sikeresen leadva válaszként!")
                            if button.text() == self.questionBank[self.questionIndex]["rightAnswer"]:
                                self.goodAnswers += 1
                                print(self.goodAnswers, "asd")
            else:
                self.resultsWindow = None
                info = str(self.goodAnswers)
                if not self.resultsWindow:
                    self.resultsWindow = resultsScreen.ResultsScreenUI(info, self.parent, "default")

                self.hide()
                self.resultsWindow.show()
        else:
            errorMessage("Nem választott választ!")

        self.setButtonsUnchecked()

    def startCountdown(self, seconds):
        self.timerThread = threading.Thread(target=self.timeCountdown, args=(seconds,))
        self.timerThread.start()

    def timeCountdown(self, seconds):
        while seconds >= 0:
            if seconds >= 10:
                self.timerLabel.setText(f"00:{seconds}")
            else:
                self.timerLabel.setText(f"00:0{seconds}")

            if seconds <= 10 and seconds > 5:
                self.timerLabel.setStyleSheet("""
                                            * {
                                                background-color: rgb(255, 203, 111);
                                                color: grey;
                                            }
                                         """)
            elif seconds <= 5:
                self.timerLabel.setStyleSheet("""
                                                 * {
                                                     background-color: rgb(255, 173, 173);
                                                     color: grey;
                                                 }
                                              """)

            if self.terminateThread.is_set():
                break

            time.sleep(1)
            seconds -= 1

    def closeQuizWindow(self, parent):
        self.terminateThread.set()

        if self.timerThread and self.timerThread.is_alive():
            self.timerThread.join()

        self.timerThread = None
        parent.show()
        self.hide()
        logger.info("Kvíz játékmód bezárása!")

