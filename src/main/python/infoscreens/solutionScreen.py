import os

from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel


class SolutionScreenUI(QMainWindow):
    def __init__(
            self, basePath, parent, grandParent, greatGrandParent, theme,
            arrayOfQuestions, arrayOfSolutions, gameMode = None
    ):
        super(SolutionScreenUI, self).__init__()

        self.theme = theme
        self.basePath = basePath

        loadUi(os.path.join(self.basePath, f"src/main/resources/ui/{self.theme}/{self.theme}SolutionScreen.ui"), self)
        self.setWindowIcon(QIcon(os.path.join(self.basePath, "src/main/resources/icon/icon.ico")))

        self.setFixedSize(self.size())

        self.parent = parent
        self.grandParent = grandParent
        self.greatGrandParent = greatGrandParent
        self.arrayOfQuestions = arrayOfQuestions
        self.arrayOfSolutions = arrayOfSolutions

        self.questionIndex = 0

        self.nextButtonExitState = False

        self.sortedArrayOfQuestions = []
        self.sortedArrayOfRightAnswers = []

        index = 0
        for i in self.arrayOfQuestions:
            index += 1
            if index <= len(arrayOfSolutions):
                self.sortedArrayOfQuestions.append(i["question"])
                if gameMode == "learnMode":
                    self.sortedArrayOfRightAnswers.append(i["goodAnswer"])
                else:
                    self.sortedArrayOfRightAnswers.append(i["rightAnswer"])

        self.questionField = self.findChild(QLabel, "questionField")
        self.answerField = self.findChild(QLabel, "answerField")
        self.backButton = self.findChild(QPushButton, "backButton")
        self.previousButton = self.findChild(QPushButton, "previousButton")
        self.nextButton = self.findChild(QPushButton, "nextButton")

        self.solutionWindow = None

        self.questionField.setWordWrap(True)
        self.answerField.setWordWrap(True)

        self.backButton.clicked.connect(lambda: self.backButtonClick(greatGrandParent))
        self.previousButton.clicked.connect(self.previousButtonClick)
        self.nextButton.clicked.connect(lambda: self.nextButtonClick(greatGrandParent))

        self.loadFirstQuestion()

        self.closeEvent = greatGrandParent.exitWindow

    def loadFirstQuestion(self):
        self.questionField.setText(self.sortedArrayOfQuestions[0])
        self.answerField.setText(f"""
        Helyes válasz a kérdésre: {self.sortedArrayOfRightAnswers[0]}
        A megadott válasz a kérdésre: {self.arrayOfSolutions[0]}
                                    """)

    def previousButtonClick(self):
        if self.questionIndex > 0:
            self.questionIndex -= 1

        if self.questionIndex < len(self.arrayOfSolutions):
            self.questionField.setText(self.sortedArrayOfQuestions[self.questionIndex])
            self.answerField.setText(f"""
            Helyes válasz a kérdésre: {self.sortedArrayOfRightAnswers[self.questionIndex]}
            A megadott válasz a kérdésre: {self.arrayOfSolutions[self.questionIndex]}
                                        """)

        self.checkNextButtonState()

    def nextButtonClick(self, greatGrandParent):
        self.questionIndex += 1
        if self.questionIndex < len(self.arrayOfSolutions):
            self.questionField.setText(self.sortedArrayOfQuestions[self.questionIndex])
            self.answerField.setText(f"""
            Helyes válasz a kérdésre: {self.sortedArrayOfRightAnswers[self.questionIndex]}
            A megadott válasz a kérdésre: {self.arrayOfSolutions[self.questionIndex]}
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
