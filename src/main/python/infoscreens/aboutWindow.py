import os

from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QTextBrowser

from src.main.python.components.logger import logger
from src.main.python.infoscreens.errorMessage import errorMessage


class AboutWindowUI(QMainWindow):
    def __init__(self, parent, basePath, theme = "default"):
        super(AboutWindowUI, self).__init__()

        self.parent = parent
        self.basePath = basePath

        self.theme = theme
        loadUi(os.path.join(self.basePath, f"src/main/resources/ui/{self.theme}/{self.theme}AboutWindow.ui"), self)
        self.setWindowIcon(QIcon(os.path.join(self.basePath, "src/main/resources/icon/icon.ico")))

        self.setFixedSize(self.size())

        self.contentBrowser = self.findChild(QTextBrowser, "contentBrowser")
        self.backButton = self.findChild(QPushButton, "backButton")

        self.loadContent()

        self.backButton.clicked.connect(lambda: self.closeWindow(parent))

    def loadContent(self):
        dataPath = os.path.join(self.basePath, "src/main/resources/datasources/credits_and_sources.txt")

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r', encoding = "UTF-8") as textFile:
                    fileContents = textFile.read()

            self.contentBrowser.setText(fileContents)

        except Exception as e:
            errorMessage(f"Hiba: {e}")

    def closeWindow(self, parent):
        logger.info("Visszalépés az üdvözlő képernyőre!")
        parent.show()
        self.hide()
