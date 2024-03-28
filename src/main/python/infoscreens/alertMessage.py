from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox
from src.main.python.components.logger import *


def alertMessage(message, highContrast = False):
    logger.info(message)
    alertDialog = QMessageBox()
    alertDialog.setWindowIcon(QIcon(os.path.join("", "src/main/resources/icon/icon.ico")))
    alertDialog.setWindowTitle("Figyelem!")
    if highContrast:
        alertDialog.setStyleSheet("""
                            * {
                                background-color: black;
                                font-size: 16px;
                                font-weight: bold;
                                color: white;
                            }

                            QPushButton {
                                background-color: rgb(50, 50, 50);
                                min-width: 80px;
                                border: 2px solid yellow;
                                border-radius: 10px;
                                color: white;
                            }

                            QPushButton:hover {
                                background-color: rgb(20, 20, 20);
	                            color: yellow;
                            }
                            """)
    else:
        alertDialog.setStyleSheet("""
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
    alertDialog.setIcon(QMessageBox.Icon.Warning)
    alertDialog.setText(message)
    alertDialog.exec()
