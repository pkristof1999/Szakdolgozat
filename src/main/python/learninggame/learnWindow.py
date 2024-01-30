import json
import threading
import time

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QPushButton, QMainWindow
from PyQt6.uic import loadUi

from src.main.python.components.logger import *
from src.main.python.infoscreens import resultsScreen
from src.main.python.infoscreens.errorMessage import errorMessage
from src.main.python.learninggame import learningWindowQuestion


class LearnWindowUI(QMainWindow):
    def __init__(self, parent, username, grandParent, typeOfLesson, nameOfData):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            self.username = username
            self.typeOfLesson = typeOfLesson
            self.nameOfData = nameOfData
            self.currentLesson = ""
            default = "default"

            lessonMapping = {
                "Önsokszorosító kártevők": "lesson1",
                "Megtévesztő kártevők": "lesson2",
                "Zavaró kártevők": "lesson3",
                "Rejtőzködő kártevők": "lesson4",
                "Adatlopó kártevők": "lesson5",
                "Hálózati kártevők": "lesson6",
                "Terjedésre specializált kártevők": "lesson7",
                "Észleléselkerülő kártevők": "lesson8",
                "Pszichológiai kártevők": "lesson9",
                "Egyéb célpontú kártevők": "lesson10",
            }

            self.currentLesson = lessonMapping.get(typeOfLesson, "")

            super(LearnWindowUI, self).__init__()
            self.setWindowIcon(QIcon("../resources/icon/icon.ico"))
            loadUi(f"../resources/ui/{default}/learnWindow.ui", self)

            self.setFixedSize(self.size())

            self.parent = parent
            self.grandParent = grandParent

            self.titleLabel = self.findChild(QLabel, "titleLabel")
            self.contentLabel = self.findChild(QLabel, "contentLabel")
            self.exitButton = self.findChild(QPushButton, "exitButton")
            self.backButton = self.findChild(QPushButton, "backButton")
            self.nextButton = self.findChild(QPushButton, "nextButton")

            self.titleLabel.setText(typeOfLesson)
            self.learnContent = self.loadLearnContentIntoArray(typeOfLesson)

            self.info = ""

            self.questionWindow = None
            self.resultsWindow = None

            self.terminateTimerThread = threading.Event()
            self.timerThread = None
            self.timeSpent = 0

            self.startEmailTimer(self.timeSpent)

            self.currentPage = ""
            self.indexOfCurrentPage = 1

            self.numberOfDataPages = 0
            for i in self.learnContent:
                if "dataPage" in i:
                    self.numberOfDataPages += 1

            self.numberOfInteractiveQuestions = 0
            self.arrayOfQuestions = []
            self.arrayOfAnswers = []
            self.numberOfGivenAnswers = 0
            self.numberOfGoodAnswers = 0

            for i in self.learnContent["questions"]:
                if "questions" in i:
                    self.numberOfInteractiveQuestions += 1
                    self.arrayOfQuestions.append(self.learnContent["questions"][i])

            self.exitButton.clicked.connect(self.exitButtonClicked)
            self.backButton.clicked.connect(self.backButtonClicked)
            self.nextButton.clicked.connect(self.nextButtonClicked)

            self.closeEvent = lambda event: grandParent.exitWindow(event, self.timerThread)

            self.loadCurrentPage()

        except Exception as e:
            errorMessage(e)
            self.hide()

    def startEmailTimer(self, seconds):
        self.terminateTimerThread.clear()
        self.timerThread = threading.Thread(target=self.timerThreadCounter, args=(seconds,))
        self.timerThread.start()

    def timerThreadCounter(self, seconds):
        times = 0
        while True:
            time.sleep(0.1)
            times += 1
            if times == 10:
                seconds += 1
                times = 0

            if self.terminateTimerThread.is_set():
                self.timeSpent = seconds
                break

    def loadLearnContentIntoArray(self, typeOfLesson):
        try:
            lessons = {}
            with open("../resources/learningdata/lessons.json", "r") as jsonFile:
                fileContents = jsonFile.read()
                if fileContents.strip():
                    lessons = json.loads(fileContents)

            return lessons[typeOfLesson]

        except Exception as e:
            errorMessage(e)

    def loadCurrentPage(self):
        pathToDataPage = ""
        dataPageKey = f"dataPage{self.indexOfCurrentPage}Path"

        for i in range(self.numberOfDataPages + 1):
            if i == self.indexOfCurrentPage:
                pathToDataPage = self.learnContent[dataPageKey]

        try:
            with open(pathToDataPage, 'r', encoding='utf-8') as htmlFile:
                htmlContent = htmlFile.read()

            self.contentLabel.setText(htmlContent)

        except Exception as e:
            errorMessage(e)

    def nextButtonClicked(self):
        if not self.questionWindow:
            self.questionWindow = learningWindowQuestion.LearningWindowQuestionUI(
                self.username, self, self.typeOfLesson
            )
        else:
            self.questionWindow = None
            self.questionWindow = learningWindowQuestion.LearningWindowQuestionUI(
                self.username, self, self.typeOfLesson
            )

        self.questionWindow.finished.connect(lambda result: self.handleNextPage(result))

        self.questionWindow.show()

    def handleNextPage(self, result):
        if result == "Next" and self.indexOfCurrentPage == self.numberOfDataPages:
            self.showResults()
        elif result == "Next":
            self.loadNextPage()

    def loadNextPage(self):
        if self.indexOfCurrentPage < self.numberOfDataPages:
            self.indexOfCurrentPage += 1
            self.loadCurrentPage()

    def showResults(self):
        self.resultsWindow = None
        self.saveResults()

        if not self.resultsWindow:
            self.resultsWindow = resultsScreen.ResultsScreenUI(self.info, self.parent, self.grandParent, "default")

        self.resultsWindow.show()
        QTimer.singleShot(100, lambda: self.hide())

    def saveResults(self):
        self.terminateTimerThread.set()

        if self.timerThread and self.timerThread.is_alive():
            self.timerThread.join()

        if self.timerThread is not None:
            while True:
                if not self.timerThread.is_alive():
                    break

        self.timerThread = None

        minutes, seconds = divmod(self.timeSpent, 60)

        for i in range(len(self.arrayOfAnswers)):
            if self.arrayOfAnswers[i] == self.arrayOfQuestions[i]["goodAnswer"]:
                self.numberOfGoodAnswers += 1

        try:
            if self.username == "Vendég":
                dataPath = "../../../userdata/profiles/guestProfile.json"
            else:
                dataPath = "../../../userdata/profiles/profiles.json"

            with open(dataPath, 'r') as jsonFile:
                fileContents = json.load(jsonFile)

            percent = int(self.numberOfGoodAnswers / self.numberOfInteractiveQuestions * 100)

            if self.timeSpent <= 3600:
                self.info = f"""
                            A helyes válaszok száma: {self.numberOfInteractiveQuestions}/{self.numberOfGoodAnswers}({percent}%)
                            A leckével töltött idő: {minutes:02d}:{seconds:02d}"""

                fileContents[self.username]["completedLessonInLearn"][self.currentLesson] = 1

            else:
                self.info = f"""
                            A helyes válaszok száma: {self.numberOfInteractiveQuestions}/{self.numberOfGoodAnswers} ({percent}%)
                            A leckével töltött töltött idő: Több, mint egy óra"""

                fileContents[self.username]["completedLessonInLearn"][self.currentLesson] = 1

            if self.numberOfGoodAnswers == len(self.arrayOfAnswers):
                self.info += """
                            Minden válaszod helyes volt!"""

                fileContents[self.username]["goodAnswersInLearn"][self.currentLesson] = 1

                if self.timeSpent <= 300:
                    self.info += """
                                Teljesítetted a leckét 05:00-n belül!
                            """

                    fileContents[self.username]["timeSpentInLearn"][self.currentLesson] = 1

            with open(dataPath, 'w') as jsonFile:
                json.dump(fileContents, jsonFile, indent=4)

        except Exception as e:
            errorMessage(e)

    def addToArrayOfAnswers(self, answer):
        self.arrayOfAnswers.append(answer)
        self.numberOfGivenAnswers += 1
        logger.info(f"Válaszok listája: {self.arrayOfAnswers}")

    def removeFromArrayOfAnswers(self):
        if self.arrayOfAnswers and self.arrayOfAnswers[-1]:
            self.arrayOfAnswers.pop()
            self.numberOfGivenAnswers -= 1
            logger.info(f"Válaszok listája: {self.arrayOfAnswers}")

    def backButtonClicked(self):
        if self.indexOfCurrentPage != 1:
            self.indexOfCurrentPage -= 1
            self.removeFromArrayOfAnswers()
            self.loadCurrentPage()

    def exitButtonClicked(self):
        self.closeLearnWindow(self.parent, self.grandParent)

    def closeLearnWindow(self, parent, grandParent):
        self.terminateTimerThread.set()

        if self.timerThread and self.timerThread.is_alive():
            self.timerThread.join()

        self.timerThread = None

        parent.show()
        grandParent.show()
        parent.raise_()
        self.hide()
        logger.info("Tanulós játémód bezárása!")
