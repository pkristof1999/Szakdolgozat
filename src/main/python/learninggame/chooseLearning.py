from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QMainWindow
from PyQt6.uic import loadUi

from src.main.python.components.logger import *
from src.main.python.infoscreens.errorMessage import errorMessage
from src.main.python.learninggame import learnWindow


class ChooseLearningUI(QMainWindow):
    def __init__(self, basePath, username, parent, theme):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            self.username = username
            self.basePath = basePath

            super(ChooseLearningUI, self).__init__()

            self.theme = theme
            self.setWindowIcon(QIcon(os.path.join(self.basePath, "src/main/resources/icon/icon.ico")))
            loadUi(os.path.join(
                self.basePath, f"src/main/resources/ui/{self.theme}/{self.theme}ChooseLearning.ui"), self
            )

            self.setFixedSize(self.size())

            self.parent = parent

            self.viruses = self.findChild(QPushButton, "viruses")
            self.worms = self.findChild(QPushButton, "worms")
            self.trojans = self.findChild(QPushButton, "trojans")
            self.ransomwares = self.findChild(QPushButton, "ransomwares")
            self.spywares = self.findChild(QPushButton, "spywares")
            self.adwares = self.findChild(QPushButton, "adwares")
            self.rootkits = self.findChild(QPushButton, "rootkits")
            self.keyloggers = self.findChild(QPushButton, "keyloggers")
            self.backButton = self.findChild(QPushButton, "backButton")

            self.learnScreen = None

            self.viruses.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson = "Vírusok",
                                             nameOfData = "viruses"
                                             )
            )

            self.worms.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson = "Férgek",
                                             nameOfData="worms"
                                             )
            )

            self.trojans.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson = "Trójai Vírusok",
                                             nameOfData="trojans"
                                             )
            )

            self.ransomwares.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson = "Zsarolóvírusok",
                                             nameOfData="ransomwares"
                                             )
            )

            self.spywares.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson="Kémprogramok",
                                             nameOfData="spywares"
                                             )
            )

            self.adwares.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson="Reklámprogramok",
                                             nameOfData="adwares"
                                             )
            )

            self.rootkits.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson="Rootkitek",
                                             nameOfData="rootkits"
                                             )
            )

            self.keyloggers.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson="Billentyűnaplózó Programok",
                                             nameOfData="keyloggers"
                                             )
            )

            self.backButton.clicked.connect(self.close)

        except Exception as e:
            errorMessage(e)
            self.hide()

    def openLearnWindow(self, username, parent, typeOfLesson, nameOfData):
        if not self.learnScreen:
            self.learnScreen = learnWindow.LearnWindowUI(
                self.basePath, self, username, parent, typeOfLesson, nameOfData, self.theme
            )
        else:
            self.learnScreen = None
            self.learnScreen = learnWindow.LearnWindowUI(
                self.basePath, self, username, parent, typeOfLesson, nameOfData, self.theme
            )

        logger.info(f"{typeOfLesson} lecke megnyitása!")
        self.learnScreen.show()
        self.hide()
        self.parent.hide()
