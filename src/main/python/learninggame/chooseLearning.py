import json

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QMainWindow
from PyQt6.uic import loadUi

from src.main.python import resultsWindow
from src.main.python import settingsWindow
from src.main.python import guestSettingsWindow
from src.main.python import loginScreen
from src.main.python.learninggame import learnWindow
from src.main.python.components.logger import *
from src.main.python.infoscreens.errorMessage import errorMessage
from src.main.python.infoscreens import gameModeInfo


class ChooseLearningUI(QMainWindow):
    def __init__(self, username, parent):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            self.username = username
            default = "default"

            super(ChooseLearningUI, self).__init__()
            self.setWindowIcon(QIcon("../resources/icon/icon.ico"))
            loadUi(f"../resources/ui/{default}/chooseLearning.ui", self)

            self.setFixedSize(self.size())

            self.parent = parent

            self.selfReplicating = self.findChild(QPushButton, "selfReplicating")
            self.deceptive = self.findChild(QPushButton, "deceptive")
            self.nuisance = self.findChild(QPushButton, "nuisance")
            self.concealing = self.findChild(QPushButton, "concealing")
            self.informationTheft = self.findChild(QPushButton, "informationTheft")
            self.networkBased = self.findChild(QPushButton, "networkBased")
            self.deliveryMechanism = self.findChild(QPushButton, "deliveryMechanism")
            self.evading = self.findChild(QPushButton, "evading")
            self.psychologicalBased = self.findChild(QPushButton, "psychologicalBased")
            self.otherTargeted = self.findChild(QPushButton, "otherTargeted")
            self.backButton = self.findChild(QPushButton, "backButton")

            self.learnScreen = None

            self.selfReplicating.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson = "Teszt"
                                             )
            )

            self.backButton.clicked.connect(self.close)

        except Exception as e:
            errorMessage(e)
            self.close()

    def openLearnWindow(self, username, parent, typeOfLesson):
        if not self.learnScreen:
            self.learnScreen = learnWindow.LearnWindowUI(self, username, parent, typeOfLesson)
        self.learnScreen.show()
        self.close()
        self.parent.close()
