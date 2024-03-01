import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from src.main.python import welcomeScreen
from src.main.python.components.logger import *

if getattr(sys, 'frozen', False):
    basePath = sys._MEIPASS
else:
    basePath = os.path.abspath(".")


if __name__ == "__main__":
    logger.info("Az alkalmazás elindult!")
    app = QApplication(sys.argv)
    iconPath = basePath + "src/resources/icon/icon.ico"
    appIcon = QIcon(iconPath)
    app.setWindowIcon(appIcon)
    welcomeWindow = welcomeScreen.WelcomeUI(basePath)
    welcomeWindow.show()
    sys.exit(app.exec())
