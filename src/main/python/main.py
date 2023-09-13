import sys
import welcomeScreen
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = welcomeScreen.WelcomeUI()
    window.show()
    window.registerButtonClick()
    sys.exit(app.exec())
