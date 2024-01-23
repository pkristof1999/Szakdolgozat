import json

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QPushButton, QMainWindow
from PyQt6.uic import loadUi

from src.main.python.components.logger import *
from src.main.python.infoscreens.errorMessage import errorMessage


class LearnWindowUI(QMainWindow):
    def __init__(self, parent, username, grandParent, typeOfLesson):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            self.username = username
            self.typeOfLesson = typeOfLesson
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
            self.contentLabel.setText(self.learnContent["data"])

            self.backButton.clicked.connect(lambda: self.closeLearnWindow(parent, grandParent))

            self.closeEvent = grandParent.exitWindow

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
