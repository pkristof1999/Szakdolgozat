import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from src.main.python import welcomeScreen
from src.main.python.components.logger import *

if __name__ == "__main__":
    logger.info("Az alkalmazás elindult!")
    app = QApplication(sys.argv)
    iconPath = "../resources/icon/icon.ico"
    appIcon = QIcon(iconPath)
    app.setWindowIcon(appIcon)
    welcomeWindow = welcomeScreen.WelcomeUI()
    welcomeWindow.show()
    sys.exit(app.exec())
