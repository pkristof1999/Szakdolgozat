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

            self.backButton = self.findChild(QPushButton, "backButton")

            self.backButton.clicked.connect(self.close)

        except Exception as e:
            errorMessage(e)
            self.close()
