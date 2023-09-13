from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow


class RegisterAccountUI(QMainWindow):
    def __init__(self):
        super(RegisterAccountUI, self).__init__()
        loadUi("../resources/ui/registerAccount.ui", self)
