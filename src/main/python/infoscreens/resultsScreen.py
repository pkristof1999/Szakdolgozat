import os

from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel

from src.main.python.infoscreens import solutionScreen
from src.main.python.infoscreens import solutionScreenForEmail
from src.main.python.infoscreens.errorMessage import errorMessage


class ResultsScreenUI(QMainWindow):
    try:
        def __init__(
                self, basePath, info, parent, grandParent, theme,
                arrayOfQuestions, arrayOfSolutions, typeOfGameMode = None
        ):
            super(ResultsScreenUI, self).__init__()

            self.theme = theme
            self.basePath = basePath

            loadUi(os.path.join(
                self.basePath, f"src/main/resources/ui/{self.theme}/{self.theme}ResultsScreen.ui"), self
            )
            self.setWindowIcon(QIcon(os.path.join(self.basePath, "src/main/resources/icon/icon.ico")))

            self.setFixedSize(self.size())
            self.parent = parent
            self.grandParent = grandParent
            self.arrayOfQuestions = arrayOfQuestions
            self.arrayOfSolutions = arrayOfSolutions
            self.typeOfGameMode = typeOfGameMode
            self.pathToQuestions = (
                os.path.join(self.basePath, "src/main/resources/quiz/questions.json")) \
                if self.typeOfGameMode == "quizGame" \
                else os.path.join(self.basePath, "src/main/resources/emaildata/emaildata.json") \
                if self.typeOfGameMode == "emailGame" \
                else os.path.join(self.basePath, "src/main/resources/learningdata/lessons.json")
            self.infoLabel = self.findChild(QLabel, "infoLabel")
            self.nextButton = self.findChild(QPushButton, "nextButton")
            self.solutionButton = self.findChild(QPushButton, "solutionButton")

            self.solutionWindow = None

            self.infoLabel.setText(info.replace("  ", ""))
            self.infoLabel.setWordWrap(True)
            self.nextButton.clicked.connect(self.nextButtonClick)
            self.solutionButton.clicked.connect(lambda: self.openSolutions(parent, grandParent, typeOfGameMode))
            self.closeEvent = grandParent.exitWindow

        def nextButtonClick(self):
            self.hide()
            self.grandParent.show()

        def openSolutions(self, parent, grandParent, typeOfGameMode):
            if not self.solutionWindow:
                if typeOfGameMode == "emailMode":
                    self.solutionWindow = solutionScreenForEmail.SolutionScreenForEmailUI(
                        self.basePath, self, parent, grandParent, self.theme,
                        self.arrayOfQuestions, self.arrayOfSolutions
                    )
                else:
                    self.solutionWindow = solutionScreen.SolutionScreenUI(
                        self.basePath, self, parent, grandParent, self.theme,
                        self.arrayOfQuestions, self.arrayOfSolutions, typeOfGameMode
                    )

            self.solutionWindow.show()
            self.hide()

    except Exception as e:
        errorMessage(e)
