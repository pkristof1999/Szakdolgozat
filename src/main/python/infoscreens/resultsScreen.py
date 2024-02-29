from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel

from src.main.python.infoscreens import solutionScreen


class ResultsScreenUI(QMainWindow):

    def __init__(self, info, parent, grandParent, theme, arrayOfSolutions = None, typeOfGameMode = None):
        super(ResultsScreenUI, self).__init__()

        self.theme = theme
        loadUi(f"src/main/resources/ui/{self.theme}/{self.theme}ResultsScreen.ui", self)
        self.setWindowIcon(QIcon("src/main/resources/icon/icon.ico"))

        self.setFixedSize(self.size())

        self.parent = parent
        self.grandParent = grandParent
        self.arrayOfSolutions = arrayOfSolutions
        self.typeOfGameMode = typeOfGameMode

        self.pathToQuestions = "src/main/resources/quiz/questions.json" if self.typeOfGameMode == "quizGame" \
            else "src/main/resources/emaildata/emaildata.json" if self.typeOfGameMode == "emailGame" \
            else "src/main/resources/learningdata/lessons.json"

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
            if typeOfGameMode == "emailGame":
                pass
            else:
                self.solutionWindow = solutionScreen.SolutionScreenUI(
                    self, parent, grandParent, self.theme, self.arrayOfSolutions
                )

        self.solutionWindow.show()
        self.hide()

