import sys
import json

from PyQt6 import QtCore
from PyQt6.QtCore import QEventLoop
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QMainWindow, QApplication, QWidget
from PyQt6.uic import loadUi

from src.main.python import resultsWindow
from src.main.python import settingsWindow
from src.main.python import guestSettingsWindow
from src.main.python import loginScreen
from src.main.python import welcomeScreen
from src.main.python.components.logger import *
from src.main.python.infoscreens.errorMessage import errorMessage
from src.main.python.infoscreens import gameModeInfo
from src.main.python.infoscreens import areYouSure
from src.main.python.learninggame import chooseLearning
from src.main.python.quizgame import quizWindow
from src.main.python.emailgame import emailWindow


class MainWindowUI(QMainWindow):
    def __init__(self, basePath, username):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            self.username = username
            self.basePath = basePath
            self.theme = self.getUserTheme(username)

            super(MainWindowUI, self).__init__()

            self.setWindowIcon(QIcon(os.path.join(self.basePath, "src/main/resources/icon/icon.ico")))
            loadUi(os.path.join(self.basePath, f"src/main/resources/ui/{self.theme}/{self.theme}MainWindow.ui"), self)

            self.setFixedSize(self.size())

            self.profilePicture = self.findChild(QFrame, "profilePicture")
            self.usernameLabel = self.findChild(QLabel, "usernameLabel")
            self.resultsButton = self.findChild(QPushButton, "resultsButton")
            self.settingsButton = self.findChild(QPushButton, "settingsButton")
            self.logOutButton = self.findChild(QPushButton, "logOutButton")
            self.exitButton = self.findChild(QPushButton, "exitButton")

            self.usernameLabel.setText(f"Üdv, {username}!")

            self.learningGameButton = self.findChild(QPushButton, "learningGameButton")
            self.quizGameButton = self.findChild(QPushButton, "quizGameButton")
            self.emailGameButton = self.findChild(QPushButton, "emailGameButton")

            self.resultsScreen = None
            self.settingsScreen = None
            self.guestSettingsScreen = None
            self.loginWindow = None
            self.infoWindow = None
            self.chooseLearningWindow = None
            self.quizWindow = None
            self.emailWindow = None
            self.welcomeWindow = None
            self.questionWindow = None

            self.resultsButton.clicked.connect(self.openResults)
            self.settingsButton.clicked.connect(lambda: self.openSettings(username))
            self.logOutButton.clicked.connect(lambda: self.logOut(username))
            self.exitButton.clicked.connect(self.exitWindowWithExitButton)

            self.learningGameInfo = "Ebben a módban kártevőtípusokról tanulhatsz. " + \
                                    "Minden témakör tartalmaz interaktív anyagokat tanuláshoz,melyekhez tartoznak kérdések is. " + \
                                    "Ha ezekre helyes a válasz, akkor kitűző kapható. " + \
                                    "Ha minden témakör válaszaira külön-külön 5 percen belül helyes válaszok kerülnek megadásra, erre is kitűző szerezhető!"

            self.quizGameInfo = "Ebben a módban a tanult tudást lehet tesztelni kvíz formájában! " + \
                                "Tíz darab kérdésre kell válaszolni, minden kérdésre 30 másodperc idő jár. " + \
                                "Ha minden kérdésre helyes a válasz, akkor kitűző kapható. " + \
                                "Ha minden válasz helyes, és a tíz kérdést megválaszolod 2 perc alatt, kitűző szerezhető!"

            self.emailGameInfo = "Ebben a módban egy tíz levélből álló postafiókot kell átnézni! " + \
                                 "Minden email-t jelölni kell, amely alkalmaz kártékony rutint!" + \
                                 "Ha minden levél helyesen van megjelölve, akkor kitűző kapható. " + \
                                 "Ha minden megadott válasz helyes 5 percen belül, kitűző szerezhető!"

            self.learningGameButton.clicked.connect(
                lambda: self.openQuestionWindow(self.learningGameInfo,
                                                self.handleLearningGameOpen,
                                                username
                                                )
            )

            self.quizGameButton.clicked.connect(
                lambda: self.openQuestionWindow(self.quizGameInfo,
                                                self.handleQuizGameOpen,
                                                username
                                                )
            )

            self.emailGameButton.clicked.connect(
                lambda: self.openQuestionWindow(self.emailGameInfo,
                                                self.handleEmailGameOpen,
                                                username
                                                )
            )

            self.label = QLabel(self.profilePicture)

            self.imagePath = self.getImagePath(username)
            self.loadImage(self.imagePath)

            self.logOutResult = False
            self.exitResult = False

            self.closeEvent = self.exitWindow

        except Exception as e:
            errorMessage(e)
            self.hide()

    def getImagePath(self, username):
        if username != "Vendég":
            dataPath = os.path.join(self.basePath, "userdata/profiles/profiles.json")
        else:
            dataPath = os.path.join(self.basePath, "userdata/profiles/guestProfile.json")

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r', encoding = "UTF-8") as jsonFile:
                    fileContents = jsonFile.read()
                    existingAccounts = json.loads(fileContents)
                    if "avatar" in existingAccounts[username]["ProfilePicturePath"]:
                        return os.path.join(self.basePath, existingAccounts[username]["ProfilePicturePath"])
                    else:
                        return os.path.join(self.basePath, existingAccounts[username]["ProfilePicturePath"])

        except Exception as e:
            errorMessage(f"Hiba: {e}")

    def loadImage(self, imagePath):
        try:
            pixmap = QPixmap(imagePath)

            if not os.path.exists(imagePath):
                raise Exception("A megadott kép nem található!")

            frameSize = self.profilePicture.size()
            pixmap = pixmap.scaled(frameSize, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                   QtCore.Qt.TransformationMode.SmoothTransformation)

            self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.label.setGeometry(self.profilePicture.rect())
            self.label.setPixmap(pixmap)

        except Exception as e:
            logger.error(f"Hiba: {e}")

    def getUserTheme(self, username):
        if username != "Vendég":
            dataPath = os.path.join(self.basePath, "userdata/profiles/profiles.json")
        else:
            dataPath = os.path.join(self.basePath, "userdata/profiles/guestProfile.json")

        try:
            if os.path.exists(dataPath):
                with open(dataPath, 'r', encoding = "UTF-8") as jsonFile:
                    fileContents = jsonFile.read()
                    existingAccounts = json.loads(fileContents)

                return existingAccounts[username]["Theme"]

        except Exception as e:
            errorMessage(f"Hiba: {e}")

    def openResults(self):
        if not self.resultsScreen:
            self.resultsScreen = resultsWindow.ResultsUI(self.basePath, self, self.username, self.theme)

        self.resultsScreen.loadUserAchievements(self.username)
        self.resultsScreen.show()
        self.settingsScreen = None

    def openSettings(self, username):
        if username == "Vendég":
            if not self.guestSettingsScreen:
                self.guestSettingsScreen = guestSettingsWindow.GuestSettingsWindowUI(
                    self.basePath, self, username, self.theme
                )
            self.guestSettingsScreen.show()
            self.guestSettingsScreen = None
        else:
            if not self.settingsScreen:
                self.settingsScreen = settingsWindow.SettingsWindowUI(self.basePath, self, username, self.theme)
            self.settingsScreen.show()
            self.settingsScreen = None

    def openQuestionWindow(self, info, handler, username=None):
        self.infoWindow = None
        if not self.infoWindow:
            self.infoWindow = gameModeInfo.GameModeInfoUI(self.basePath, info, self.theme)

        if username is not None:
            self.infoWindow.finished.connect(lambda result: handler(result, username))
        else:
            self.infoWindow.finished.connect(handler)

        self.infoWindow.show()

    def handleLearningGameOpen(self, result, username):
        if result == "Yes":
            self.closeOpenWindows()
            self.openLearningGame(username)

    def handleQuizGameOpen(self, result, username):
        if result == "Yes":
            self.closeOpenWindows()
            self.openQuizGame(username)

    def handleEmailGameOpen(self, result, username):
        if result == "Yes":
            self.closeOpenWindows()
            self.openEmailGame(username)

    def openLearningGame(self, username):
        self.chooseLearningWindow = None
        if not self.chooseLearningWindow:
            self.chooseLearningWindow = chooseLearning.ChooseLearningUI(self.basePath, username, self, self.theme)
        self.chooseLearningWindow.show()
        logger.info("Tanulós játékmódhoz az anyagválasztó megnyitása!")

    def openQuizGame(self, username):
        self.quizWindow = None
        if not self.quizWindow:
            self.quizWindow = quizWindow.QuizWindowUI(self.basePath, username, self, self.theme)
        self.quizWindow.show()
        self.hide()
        logger.info("Kvíz játékmód megnyitása!")

    def openEmailGame(self, username):
        self.emailWindow = None
        if not self.emailWindow:
            self.emailWindow = emailWindow.EmailWindowUI(self.basePath, username, self, self.theme)
        self.emailWindow.show()
        self.hide()
        logger.info("Email játékmód megnyitása!")

    def logOut(self, username):
        self.logOutResult = False
        if self.username == "Vendég":
            self.openLogOutExitWindow("Biztosan kijelentkezik?\n"
                                      "Eredményei törlődnek!",
                                      self.handleLogOutButton,)
        else:
            self.openLogOutExitWindow("Biztosan kijelentkezik?",
                                      self.handleLogOutButton)

        loop = QEventLoop(self.questionWindow)
        self.questionWindow.finished.connect(loop.quit)

        loop.exec()

        if self.logOutResult:
            self.closeOpenWindows()

            if username == "Vendég":
                if not self.welcomeWindow:
                    self.welcomeWindow = welcomeScreen.WelcomeUI(self.basePath)
                self.welcomeWindow.show()
            else:
                if not self.loginWindow:
                    self.loginWindow = loginScreen.LoginScreenUI(self.basePath)
                self.loginWindow.show()

            logger.info("Sikeres kijelentkezés!")
            logger.info("Bejelentkezési képernyő megnyitásra került!")

            self.hide()

    def refreshWindow(self):
        for window in QApplication.topLevelWidgets():
            if isinstance(window, QMainWindow):
                window.deleteLater()

        newMainWindow = MainWindowUI(self.basePath, self.username)
        newMainWindow.show()

    def closeOpenWindows(self):
        openWindows = QApplication.topLevelWidgets()
        for scene in openWindows:
            if scene.windowTitle() != "Főképernyő":
                scene.hide()

    def exitWindow(self, event, thread1=None, terminateThread1=None, thread2=None, terminateThread2=None):
        if not self.exitResult:
            if self.username == "Vendég":
                self.openLogOutExitWindow("Biztosan kilép az alkalmazásból?\n"
                                          "Eredményei törlődnek!",
                                          self.handleExitButton)
            else:
                self.openLogOutExitWindow("Biztosan kilép az alkalmazásból?",
                                          self.handleExitButton)

            loop = QEventLoop(self.questionWindow)
            self.questionWindow.finished.connect(loop.quit)

            loop.exec()

        if self.exitResult:
            if thread1 is not None:
                terminateThread1.set()
                thread1.join()
            if thread2 is not None:
                terminateThread2.set()
                thread2.join()
            logger.info("Kilépés az alkalmazásból!")
            for window in QApplication.topLevelWidgets():
                window.close()
            event.accept()
        else:
            event.ignore()

    def exitWindowWithExitButton(self):
        if not self.exitResult:
            if self.username == "Vendég":
                self.openLogOutExitWindow("Biztosan kilép az alkalmazásból?\n"
                                          "Eredményei törlődnek!",
                                          self.handleExitButton)
            else:
                self.openLogOutExitWindow("Biztosan kilép az alkalmazásból?",
                                          self.handleExitButton)

            loop = QEventLoop(self.questionWindow)
            self.questionWindow.finished.connect(loop.quit)

            loop.exec()

        if self.exitResult:
            logger.info("Kilépés az alkalmazásból!")
            sys.exit()

    def openLogOutExitWindow(self, info, handler):
        self.questionWindow = None
        if not self.questionWindow:
            self.questionWindow = areYouSure.AreYouSureUI(self.basePath, info, self.theme)

        self.questionWindow.finished.connect(handler)
        self.questionWindow.show()

    def handleLogOutButton(self, result):
        if result == "Yes":
            self.logOutResult = True

    def handleExitButton(self, result):
        if result == "Yes":
            self.exitResult = True
