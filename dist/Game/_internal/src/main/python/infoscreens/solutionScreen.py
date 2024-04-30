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
        self.answerBox = self.findChild(QLabel, "answerBox")
        self.answerField = self.findChild(QLabel, "answerField")
        self.userAnswerField = self.findChild(QLabel, "userAnswerField")
        self.backButton = self.findChild(QPushButton, "backButton")
        self.previousButton = self.findChild(QPushButton, "previousButton")
        self.nextButton = self.findChild(QPushButton, "nextButton")

        self.defaultPreviousButtonStyle = self.previousButton.styleSheet()

        self.solutionWindow = None

        self.questionField.setWordWrap(True)
        self.answerField.setWordWrap(True)
        self.userAnswerField.setWordWrap(True)

        self.backButton.clicked.connect(lambda: self.backButtonClick(parent))
        self.previousButton.clicked.connect(self.previousButtonClick)
        self.nextButton.clicked.connect(lambda: self.nextButtonClick(greatGrandParent))

        self.rightAnswerStyle = """
                                    * {
                                        background-color: rgb(100, 220, 95);
                                        border: 2px solid rgb(20, 145, 15);
                                        border-radius: 10px;
                                        font-size: 12pt;
                                    }
                                    """

        self.wrongAnswerStyle = """
                                    * {
                                        background-color: rgb(240, 95, 85);
                                        border: 2px solid rgb(200, 45, 30);
                                        border-radius: 10px;
                                        font-size: 12pt;
                                    }
                                    """

        self.hideButton(self.previousButton)
        self.loadFirstQuestion()

        self.closeEvent = greatGrandParent.exitWindow

    def checkAnswer(self):
        tmpAnswerField = self.answerField.text().split(":")[1]
        tmpUserAnswerField = self.userAnswerField.text().split(":")[1]
        if tmpAnswerField == tmpUserAnswerField:
            self.answerBox.setStyleSheet(self.rightAnswerStyle)
        else:
            self.answerBox.setStyleSheet(self.wrongAnswerStyle)

    def loadFirstQuestion(self):
        self.questionField.setText(self.sortedArrayOfQuestions[0])
        self.answerField.setText("A helyes válasz: " + self.sortedArrayOfRightAnswers[0])
        self.userAnswerField.setText("A megadott válasz: " + self.arrayOfSolutions[0])
        self.checkAnswer()

    def previousButtonClick(self):
        if self.questionIndex > 0:
            self.questionIndex -= 1

        if self.questionIndex < len(self.arrayOfSolutions):
            self.questionField.setText(self.sortedArrayOfQuestions[self.questionIndex])
            self.answerField.setText("A helyes válasz: " + self.sortedArrayOfRightAnswers[self.questionIndex])
            self.userAnswerField.setText("A megadott válasz: " + self.arrayOfSolutions[self.questionIndex])
            self.checkAnswer()

        if self.questionIndex == 0:
            self.hideButton(self.previousButton)

        self.checkNextButtonState()

    def nextButtonClick(self, greatGrandParent):
        self.questionIndex += 1
        if self.questionIndex < len(self.arrayOfSolutions):
            self.questionField.setText(self.sortedArrayOfQuestions[self.questionIndex])
            self.answerField.setText("A helyes válasz: " + self.sortedArrayOfRightAnswers[self.questionIndex])
            self.userAnswerField.setText("A megadott válasz: " + self.arrayOfSolutions[self.questionIndex])
            self.checkAnswer()

        self.showButton(self.previousButton)

        if self.nextButtonExitState:
            self.hide()
            greatGrandParent.show()

        self.checkNextButtonState()

    def hideButton(self, button):
        button.setEnabled(False)
        button.setStyleSheet("""* {
                                    border: None;
                                    background-color: rgba(0, 0, 0, 0);
                                    color: rgba(0, 0, 0, 0);
                                }
                            """)

    def showButton(self, button):
        button.setEnabled(True)
        button.setStyleSheet(self.defaultPreviousButtonStyle)

    def backButtonClick(self, parent):
        self.hide()
        parent.show()

    def checkNextButtonState(self):
        if self.questionIndex == len(self.arrayOfSolutions) - 1:
            self.nextButton.setText("Kezdőképernyő")
            self.nextButtonExitState = True
        else:
            self.nextButton.setText("Következő")
            self.nextButtonExitState = False
