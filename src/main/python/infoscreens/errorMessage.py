from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox

from src.main.python.components.logger import *


def errorMessage(message):
    logger.error(message)
    errorDialog = QMessageBox()
    errorDialog.setWindowIcon(QIcon("src/main/resources/icon/icon.ico"))
    errorDialog.setWindowTitle("Hiba!")
    errorDialog.setStyleSheet("""
                * {
                    background-color: whitesmoke;
                    font-size: 16px;
                    font-weight: bold;
                    color: grey;
                }

                QPushButton {
                    background-color: white;
                    min-width: 80px;
                    border: 2px solid #8f8f91;
                    border-radius: 10px;
                    color: grey;
                }

                QPushButton:hover {
                    background-color: rgb(120, 120, 220);
                    color: white;
                }
                """)
    errorDialog.setIcon(QMessageBox.Icon.Critical)
    errorDialog.setText(message)
    errorDialog.exec()
