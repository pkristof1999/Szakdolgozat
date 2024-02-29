from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel


class SolutionScreenForEmailUI(QMainWindow):
    def __init__(self, parent, grandParent, greatGrandParent, theme, arrayOfSolutions):
        super(SolutionScreenForEmailUI, self).__init__()

        self.theme = theme
        loadUi(f"src/main/resources/ui/{self.theme}/{self.theme}SolutionScreenForEmail.ui", self)
        self.setWindowIcon(QIcon("src/main/resources/icon/icon.ico"))

        self.setFixedSize(self.size())

        self.parent = parent
        self.grandParent = grandParent
        self.greatGrandParent = greatGrandParent
        self.arrayOfSolutions = arrayOfSolutions

        print(arrayOfSolutions)

        self.questionField = self.findChild(QLabel, "questionField")
        self.answerField = self.findChild(QLabel, "answerField")
        self.backButton = self.findChild(QPushButton, "backButton")
        self.previousButton = self.findChild(QPushButton, "previousButton")
        self.nextButton = self.findChild(QPushButton, "nextButton")

        self.solutionWindow = None

        # self.infoLabel.setWordWrap(True)

        self.backButton.clicked.connect(lambda: self.backButtonClick(parent))
        self.previousButton.clicked.connect(self.previousButtonClick)
        self.nextButton.clicked.connect(self.nextButtonClick)

        self.closeEvent = greatGrandParent.exitWindow

    def previousButtonClick(self):
        pass

    def nextButtonClick(self):
        pass

    def backButtonClick(self, parent):
        self.hide()
        parent.show()
