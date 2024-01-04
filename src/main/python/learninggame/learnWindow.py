import json

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QMainWindow
from PyQt6.uic import loadUi

from src.main.python import resultsWindow
from src.main.python import settingsWindow
from src.main.python import guestSettingsWindow
from src.main.python import loginScreen
from src.main.python.components.logger import *
from src.main.python.infoscreens.errorMessage import errorMessage
from src.main.python.infoscreens import gameModeInfo


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

            self.backButton.clicked.connect(lambda: self.closeLearnWindow(parent, grandParent))

        except Exception as e:
            errorMessage(e)
            self.close()

    def closeLearnWindow(self, parent, grandParent):
        grandParent.show()
        parent.show()
        self.close()
