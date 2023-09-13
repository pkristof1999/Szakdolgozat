import sys
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QApplication


class RegisterAccountUI(QMainWindow):
    def __init__(self):
        super(RegisterAccountUI, self).__init__()
        loadUi("../resources/ui/registerAccount.ui", self)


def showUI():
    app = QApplication(sys.argv)
    window = RegisterAccountUI()
    window.show()
    sys.exit(app.exec())