import sys
import registerAccount
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QApplication


class WelcomeUI(QMainWindow):
    def __init__(self):
        super(WelcomeUI, self).__init__()
        loadUi("../resources/ui/welcomeScreen.ui", self)
        self.registerButton.click.connect(registerAccount.showUI())


def showUI():
    app = QApplication(sys.argv)
    window = WelcomeUI()
    window.show()
    sys.exit(app.exec())
