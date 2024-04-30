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
        self.answerBox = self.findChild(QLabel, "answerBox")
        self.answerField = self.findChild(QLabel, "answerField")
        self.userAnswerField = self.findChild(QLabel, "userAnswerField")
        self.backButton = self.findChild(QPushButton, "backButton")
        self.previousButton = self.findChild(QPushButton, "previousButton")
        self.nextButton = self.findChild(QPushButton, "nextButton")

        self.defaultPreviousButtonStyle = self.previousButton.styleSheet()

        self.solutionWindow = None
        self.label = QLabel(self.emailFrame)

        self.answerField.setWordWrap(True)

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
        tmpAnswerField = self.answerField.text().split("?")[1]
        tmpUserAnswerField = self.userAnswerField.text().split(":")[1]
        if "Hiteles" in tmpAnswerField and "Hiteles" in tmpUserAnswerField or \
            "Káros" in tmpAnswerField and "Káros" in tmpUserAnswerField:
            self.answerBox.setStyleSheet(self.rightAnswerStyle)
        else:
            self.answerBox.setStyleSheet(self.wrongAnswerStyle)

    def loadFirstQuestion(self):
        self.loadImage(os.path.join(self.basePath, self.sortedArrayOfEmails[0]))
        self.answerField.setText("Milyen jellegű az e-mail? " +
                                 self.translateRightAnswers(self.sortedArrayOfRightAnswers[0]) + "\n" +
                                 "Az indoklás: " + self.sortedArrayOfReasons[0])
        self.userAnswerField.setText("Megadott válasz: " +
                                     self.translateSolutions(self.arrayOfSolutions[0]))

        self.checkAnswer()

    def translateRightAnswers(self, answer):
        return "Hiteles" if not answer else "Káros"

    def translateSolutions(self, solution):
        return "Hiteles" if solution else "Káros"

    def previousButtonClick(self):
        if self.questionIndex > 0:
            self.questionIndex -= 1

        self.loadImage(os.path.join(self.basePath, self.sortedArrayOfEmails[self.questionIndex]))
        self.answerField.setText("Milyen jellegű az e-mail? " +
                                 self.translateRightAnswers(self.sortedArrayOfRightAnswers[self.questionIndex]) + "\n" +
                                 "Az indoklás: " + self.sortedArrayOfReasons[self.questionIndex])
        self.userAnswerField.setText("Megadott válasz: " +
                                     self.translateSolutions(self.arrayOfSolutions[self.questionIndex]))

        self.checkAnswer()

        if self.questionIndex == 0:
            self.hideButton(self.previousButton)

        self.checkNextButtonState()

    def nextButtonClick(self, greatGrandParent):
        self.questionIndex += 1
        if self.questionIndex < len(self.arrayOfSolutions):
            self.loadImage(os.path.join(self.basePath, self.sortedArrayOfEmails[self.questionIndex]))
            self.answerField.setText("Milyen jellegű az e-mail? " +
                                     self.translateRightAnswers(self.sortedArrayOfRightAnswers[self.questionIndex]) + "\n" +
                                     "Az indoklás: " + self.sortedArrayOfReasons[self.questionIndex])
            self.userAnswerField.setText("Megadott válasz: " +
                                         self.translateSolutions(self.arrayOfSolutions[self.questionIndex]))

            self.checkAnswer()

        self.showButton(self.previousButton)

        if self.nextButtonExitState:
            self.hide()
            greatGrandParent.show()

        self.checkNextButtonState()

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
