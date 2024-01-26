import json

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QPushButton, QMainWindow
from PyQt6.uic import loadUi

from src.main.python.components.logger import *
from src.main.python.infoscreens.errorMessage import errorMessage


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
            self.backButton = self.findChild(QPushButton, "backButton")
            self.nextButton = self.findChild(QPushButton, "nextButton")

            self.titleLabel.setText(typeOfLesson)
            self.learnContent = self.loadLearnContentIntoArray(typeOfLesson)

            self.currentPage = ""
            self.indexOfCurrentPage = 1

            self.numberOfDataPages = 0
            for i in self.learnContent:
                if "dataPage" in i:
                    self.numberOfDataPages += 1

            self.numberOfInteractiveQuestions = 0
            for i in self.learnContent["questions"]:
                if "question" in i:
                    self.numberOfInteractiveQuestions += 1

            print(self.numberOfDataPages)
            print(self.numberOfInteractiveQuestions)

            self.backButton.clicked.connect(self.backButtonClicked)
            self.nextButton.clicked.connect(self.nextButtonClicked)

            self.closeEvent = grandParent.exitWindow

            self.loadCurrentPage()

        except Exception as e:
            errorMessage(e)
            self.hide()

    def closeLearnWindow(self, parent, grandParent):
        # TODO
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

    def loadInteractiveQuestion(self):
        pass

    def nextButtonClicked(self):
        if self.indexOfCurrentPage < self.numberOfDataPages:
            self.indexOfCurrentPage += 1
            self.loadCurrentPage()

    def backButtonClicked(self):
        if self.indexOfCurrentPage == 1:
            self.closeLearnWindow(self.parent, self.grandParent)
        else:
            self.indexOfCurrentPage -= 1
            self.loadCurrentPage()
