import sys
import welcomeScreen

from PyQt6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcomeWindow = welcomeScreen.WelcomeUI()
    welcomeWindow.show()
    sys.exit(app.exec())
