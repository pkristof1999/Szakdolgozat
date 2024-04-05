import os

from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton

from src.main.python.components.logger import logger


class AboutWindowUI(QMainWindow):
    def __init__(self, parent, basePath, theme = "default"):
        super(AboutWindowUI, self).__init__()

        self.parent = parent
        print(parent)
        self.basePath = basePath

        self.theme = theme
        loadUi(os.path.join(self.basePath, f"src/main/resources/ui/{self.theme}/{self.theme}AboutWindow.ui"), self)
        self.setWindowIcon(QIcon(os.path.join(self.basePath, "src/main/resources/icon/icon.ico")))

        self.setFixedSize(self.size())

        self.backButton = self.findChild(QPushButton, "backButton")

        self.backButton.clicked.connect(lambda: self.closeWindow(parent))

    def closeWindow(self, parent):
        logger.info("Visszalépés az üdvözlő képernyőre!")
        parent.show()
        self.hide()
