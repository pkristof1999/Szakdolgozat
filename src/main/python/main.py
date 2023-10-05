import sys
import welcomeScreen

from PyQt6.QtWidgets import QApplication

from src.main.python.components.logger import *


if __name__ == "__main__":
    logger.info("Az alkalmazás elindult!")
    app = QApplication(sys.argv)
    welcomeWindow = welcomeScreen.WelcomeUI()
    welcomeWindow.show()
    sys.exit(app.exec())
