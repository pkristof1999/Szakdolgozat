import loginScreen

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton


class MainWindowUI(QMainWindow):
    def __init__(self):
        super(MainWindowUI, self).__init__()
        loadUi("../resources/ui/mainWindow.ui", self)

        self.backButton = self.findChild(QPushButton, "backButton")
