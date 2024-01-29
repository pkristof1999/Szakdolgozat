import json

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
            default = "default"

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

            self.questionWindow = None
            self.resultsWindow = None

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

            for i in self.learnContent["questions"]:
                if "questions" in i:
                    self.numberOfInteractiveQuestions += 1
                    self.arrayOfQuestions.append(self.learnContent["questions"][i])

            print(self.arrayOfQuestions)
            print(self.numberOfDataPages)
            print(self.numberOfInteractiveQuestions)

            self.exitButton.clicked.connect(self.exitButtonClicked)
            self.backButton.clicked.connect(self.backButtonClicked)
            self.nextButton.clicked.connect(self.nextButtonClicked)

            self.closeEvent = grandParent.exitWindow

            self.loadCurrentPage()

        except Exception as e:
            errorMessage(e)
            self.hide()

    def closeLearnWindow(self, parent, grandParent):
        parent.show()
        grandParent.show()
        parent.raise_()
        self.hide()
        logger.info("Tanulós játémód bezárása!")

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
        self.saveResults()
        self.resultsWindow = None
        info = "Utolsó kérdés"
        if not self.resultsWindow:
            self.resultsWindow = resultsScreen.ResultsScreenUI(info, self.parent, self.grandParent, "default")

        self.resultsWindow.show()
        QTimer.singleShot(100, lambda: self.hide())

    def saveResults(self):
        # TODO
        pass

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
