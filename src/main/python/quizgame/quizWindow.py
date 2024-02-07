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
    def __init__(self, username, parent, theme):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            self.username = username

            super(QuizWindowUI, self).__init__()

            self.theme = theme
            self.setWindowIcon(QIcon("../resources/icon/icon.ico"))
            loadUi(f"../resources/ui/{self.theme}/quizScreen.ui", self)

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
            self.pointsEarned = 0

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
            self.timerThreadCompleted = False
            self.timerThread = None
            self.isTimesUp = False
            self.countdown = 30

            self.terminateQuizThread = threading.Event()
            self.quizTimerThread = None
            self.timeSpent = 0

            self.startCountdown(self.countdown)
            self.startQuizTimer(self.timeSpent)

            self.loadFirstQuestion()

            self.answerButtonGroup.buttonClicked.connect(self.handleAnswerSelection)

            self.nextButton.clicked.connect(self.nextQuestion)
            self.backButton.clicked.connect(lambda: self.closeQuizWindow(parent))

            self.closeEvent = lambda event: parent.exitWindow(event, self.timerThread, self.quizTimerThread)

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
                self.answer4Button.isChecked() or \
                self.isTimesUp:

            self.questionIndex += 1
            if self.questionIndex < 10:
                for button in self.answerButtonGroup.buttons():
                    if button.isChecked():
                        logger.info(f"{button.text()} sikeresen leadva válaszként!")
                        if button.text() == self.questionBank[self.questionIndex]["rightAnswer"]:
                            self.goodAnswers += 1

                nextQuestion = self.questionBank[self.questionIndex]

                self.questionField.setText(nextQuestion["question"])
                self.answer1Button.setText(nextQuestion["answer1"])
                self.answer2Button.setText(nextQuestion["answer2"])
                self.answer3Button.setText(nextQuestion["answer3"])
                self.answer4Button.setText(nextQuestion["answer4"])

                if not self.isTimesUp:
                    if self.timerThread and self.timerThread.is_alive():
                        self.terminateThread.set()
                        self.timerThread.join()

                self.isTimesUp = False
                self.startCountdown(30)
            else:
                for button in self.answerButtonGroup.buttons():
                    if button.isChecked():
                        logger.info(f"{button.text()} sikeresen leadva válaszként!")
                        if button.text() == self.questionBank[self.questionIndex]["rightAnswer"]:
                            self.goodAnswers += 1

                self.resultsWindow = None

                if self.timerThread is not None:
                    if self.timerThread and self.timerThread.is_alive():
                        self.terminateThread.set()
                        self.timerThread.join()

                if self.quizTimerThread is not None:
                    if self.quizTimerThread and self.quizTimerThread.is_alive():
                        self.terminateQuizThread.set()
                        self.quizTimerThread.join()

                while True:
                    if not self.timerThread.is_alive() and not self.quizTimerThread.is_alive():
                        self.timerThread = None
                        self.quizTimerThread = None
                        break

                badge1 = False
                badge2 = False

                minutes, seconds = divmod(self.timeSpent, 60)

                if self.timeSpent <= 3600:
                    info = f"""
                                A helyes válaszok száma: 10/{self.goodAnswers} ({int(self.goodAnswers / 10 * 100)}%)
                                Kvízzel töltött idő: {minutes:02d}:{seconds:02d}
                                Kitűzőt szereztél teljesítésre! Értéke: 100 pont*"""
                else:
                    info = f"""
                                A helyes válaszok száma: 10/{self.goodAnswers} ({int(self.goodAnswers / 10 * 100)}%)
                                Kvízzel töltött idő: Több, mint egy óra
                                Kitűzőt szereztél teljesítésre! Értéke: 100 pont*"""

                if self.goodAnswers == 10:
                    info += """
                                Minden válaszod helyes volt!
                                Kitűzőt szereztél pontosságra! Értéke: 250 pont*"""
                    badge1 = True

                    if self.timeSpent <= 120:
                        info += """
                                    Teljesítetted a kvízt 02:00-n belül!
                                    Kitűzőt szereztél sebességre! Értéke: 1000 pont*
                                """
                        badge2 = True

                info += """
                            * Csak akkor kerül beszámításra, ha eddig nem volt meg!
                        """

                self.saveResults(badge1, badge2)

                if not self.resultsWindow:
                    self.resultsWindow = resultsScreen.ResultsScreenUI(info, self, self.parent, "default")

                self.resultsWindow.show()
                self.hide()
        else:
            errorMessage("Nem választott választ!")

        self.setButtonsUnchecked()

    def startCountdown(self, seconds):
        self.terminateThread.clear()
        self.timerThread = threading.Thread(target=self.timeCountdown, args=(seconds,))
        self.timerThread.start()

    def startQuizTimer(self, seconds):
        self.terminateQuizThread.clear()
        self.quizTimerThread = threading.Thread(target=self.quizTimer, args=(seconds,))
        self.quizTimerThread.start()

    def timeCountdown(self, seconds):
        times = 0
        while seconds >= 0:
            if seconds >= 10:
                self.timerLabel.setText(f"00:{seconds}")
            else:
                self.timerLabel.setText(f"00:0{seconds}")

            if seconds == 0:
                time.sleep(1)
                self.isTimesUp = True
                self.terminateThread.set()

            if self.terminateThread.is_set():
                break

            time.sleep(0.1)
            times += 1
            if times == 10:
                seconds -= 1
                times = 0

        if self.isTimesUp:
            if self.questionIndex < 9:
                self.nextQuestion()
            else:
                for button in self.answerButtonGroup.buttons():
                    if button.isChecked():
                        button.setStyleSheet("""
                                                * {
                                                    background-color: #ff0000;
                                                }
                                             """)
                    else:
                        button.setStyleSheet("""
                                                * {
                                                    background-color: #dadadd;
                                                    color: grey;
                                                }
                                             """)

                    button.setEnabled(False)
                    self.timerLabel.setText("Lejárt!")

    def quizTimer(self, seconds):
        times = 0
        while True:
            time.sleep(0.1)
            times += 1
            if times == 10:
                seconds += 1
                times = 0

            if self.isTimesUp:
                self.terminateThread.set()
                self.timerThread.join()

            if self.terminateQuizThread.is_set():
                self.timeSpent = seconds
                break

    def saveResults(self, badge1, badge2):
        try:
            if self.username == "Vendég":
                dataPath = "../../../userdata/profiles/guestProfile.json"
            else:
                dataPath = "../../../userdata/profiles/profiles.json"

            with open(dataPath, 'r') as jsonFile:
                fileContents = json.load(jsonFile)

            if self.username in fileContents:
                if badge1 and badge2:
                    if fileContents[self.username]["QuizMedal"] == 0 and \
                            fileContents[self.username]["badge03"] == 0 and \
                            fileContents[self.username]["badge04"] == 0:
                        self.pointsEarned = 1350
                        fileContents[self.username]["Score"] += self.pointsEarned
                    elif fileContents[self.username]["QuizMedal"] == 1 and \
                            fileContents[self.username]["badge03"] == 0 and \
                            fileContents[self.username]["badge04"] == 0:
                        self.pointsEarned = 1250
                        fileContents[self.username]["Score"] += self.pointsEarned
                    elif fileContents[self.username]["QuizMedal"] == 1 and \
                            fileContents[self.username]["badge03"] == 1 and \
                            fileContents[self.username]["badge04"] == 0:
                        self.pointsEarned = 1000
                        fileContents[self.username]["Score"] += self.pointsEarned

                    fileContents[self.username]["QuizMedal"] = 1
                    fileContents[self.username]["badge03"] = 1
                    fileContents[self.username]["badge04"] = 1
                elif badge1:
                    if fileContents[self.username]["QuizMedal"] == 0 and \
                            fileContents[self.username]["badge03"] == 0:
                        self.pointsEarned = 350
                        fileContents[self.username]["Score"] += self.pointsEarned
                    elif fileContents[self.username]["QuizMedal"] == 1 and \
                            fileContents[self.username]["badge03"] == 0:
                        self.pointsEarned = 250
                        fileContents[self.username]["Score"] += self.pointsEarned

                    fileContents[self.username]["QuizMedal"] = 1
                    fileContents[self.username]["badge03"] = 1
                else:
                    if fileContents[self.username]["QuizMedal"] == 0:
                        self.pointsEarned = 100
                        fileContents[self.username]["Score"] += self.pointsEarned
                    fileContents[self.username]["QuizMedal"] = 1

            with open(dataPath, 'w') as jsonFile:
                json.dump(fileContents, jsonFile, indent=4)

        except Exception as e:
            errorMessage(f"Hiba: {e}")

    def closeQuizWindow(self, parent):
        self.terminateThread.set()
        self.terminateQuizThread.set()

        if self.timerThread and self.timerThread.is_alive():
            self.timerThread.join()

        if self.quizTimerThread and self.quizTimerThread.is_alive():
            self.quizTimerThread.join()

        self.timerThread = None
        self.quizTimerThread = None
        parent.show()
        self.hide()
        logger.info("Kvíz játékmód bezárása!")
