from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow


class SettingsWindowUI(QMainWindow):
    def __init__(self):
        super(SettingsWindowUI, self).__init__()
        loadUi("../resources/ui/default/settingsWindow.ui", self)
