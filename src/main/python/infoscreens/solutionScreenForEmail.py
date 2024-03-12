import os

from PyQt6 import QtCore
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QFrame

from src.main.python.components.logger import *


class SolutionScreenForEmailUI(QMainWindow):
    def __init__(self, basePath, parent, grandParent, greatGrandParent, theme, arrayOfQuestions, arrayOfSolutions):
        super(SolutionScreenForEmailUI, self).__init__()

        self.theme = theme
        self.basePath = basePath

        loadUi(os.path.join(
            self.basePath, f"src/main/resources/ui/{self.theme}/{self.theme}SolutionScreenForEmail.ui"), self
        )
        self.setWindowIcon(QIcon(os.path.join(self.basePath, "src/main/resources/icon/icon.ico")))

        self.setFixedSize(self.size())

        self.parent = parent
        self.grandParent = grandParent
        self.greatGrandParent = greatGrandParent
        self.arrayOfQuestions = arrayOfQuestions
        self.arrayOfSolutions = arrayOfSolutions

        self.questionIndex = 0

        self.nextButtonExitState = False

        self.sortedArrayOfEmails = []
        self.sortedArrayOfRightAnswers = []
        self.sortedArrayOfReasons = []

        index = 0
        for i in self.arrayOfQuestions:
            index += 1
            if index <= len(arrayOfSolutions):
                self.sortedArrayOfEmails.append(i["pathToEmail"])
                self.sortedArrayOfRightAnswers.append(i["isMalicious"])
                self.sortedArrayOfReasons.append(i["reason"])

        self.emailFrame = self.findChild(QFrame, "emailFrame")
        self.answerField = self.findChild(QLabel, "answerField")
        self.backButton = self.findChild(QPushButton, "backButton")
        self.previousButton = self.findChild(QPushButton, "previousButton")
        self.nextButton = self.findChild(QPushButton, "nextButton")

        self.solutionWindow = None
        self.label = QLabel(self.emailFrame)

        self.backButton.clicked.connect(lambda: self.backButtonClick(greatGrandParent))
        self.previousButton.clicked.connect(self.previousButtonClick)
        self.nextButton.clicked.connect(lambda: self.nextButtonClick(greatGrandParent))

        self.loadFirstQuestion()

        self.closeEvent = greatGrandParent.exitWindow

    def loadFirstQuestion(self):
        self.loadImage(os.path.join(self.basePath, self.sortedArrayOfEmails[0]))
        self.answerField.setText(f"""
        Milyen jellegű az e-mail?: {self.translateRightAnswers(self.sortedArrayOfRightAnswers[0])}
        A megadott válasz a kérdésre: {self.translateSolutions(self.arrayOfSolutions[0])}
        Az indoklás: {self.sortedArrayOfReasons[0]}
                                    """)

    def translateRightAnswers(self, answer):
        return "Hiteles" if not answer else "Káros"

    def translateSolutions(self, solution):
        return "Hiteles" if solution else "Káros"

    def previousButtonClick(self):
        if self.questionIndex > 0:
            self.questionIndex -= 1

        self.loadImage(os.path.join(self.basePath, self.sortedArrayOfEmails[self.questionIndex]))
        self.answerField.setText(f"""
        Milyen jellegű az e-mail?: {self.translateRightAnswers(self.sortedArrayOfRightAnswers[self.questionIndex])}
        A megadott válasz a kérdésre: {self.translateSolutions(self.arrayOfSolutions[self.questionIndex])}
        Az indoklás: {self.sortedArrayOfReasons[0]}
                                    """)

        self.checkNextButtonState()

    def nextButtonClick(self, greatGrandParent):
        self.questionIndex += 1
        if self.questionIndex < len(self.arrayOfSolutions):
            self.loadImage(os.path.join(self.basePath, self.sortedArrayOfEmails[self.questionIndex]))
            self.answerField.setText(f"""
            Milyen jellegű az e-mail?: {self.translateRightAnswers(self.sortedArrayOfRightAnswers[self.questionIndex])}
            A megadott válasz a kérdésre: {self.translateSolutions(self.arrayOfSolutions[self.questionIndex])}
            Az indoklás: {self.sortedArrayOfReasons[0]}
                                        """)

        if self.nextButtonExitState:
            self.hide()
            greatGrandParent.show()

        self.checkNextButtonState()

    def backButtonClick(self, greatGrandParent):
        self.hide()
        greatGrandParent.show()

    def checkNextButtonState(self):
        if self.questionIndex == len(self.arrayOfSolutions) - 1:
            self.nextButton.setText("Kezdőképernyő")
            self.nextButtonExitState = True
        else:
            self.nextButton.setText("Következő")
            self.nextButtonExitState = False

    def loadImage(self, imagePath):
        try:
            pixmap = QPixmap(imagePath)

            if not os.path.exists(imagePath):
                raise Exception("A megadott kép nem található!")

            frameSize = self.emailFrame.size()
            pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                   QtCore.Qt.TransformationMode.SmoothTransformation)

            self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.label.setGeometry(self.emailFrame.rect())
            self.label.setPixmap(pixmap)

        except Exception as e:
            logger.error(f"Hiba: {e}")
