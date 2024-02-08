from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QMainWindow
from PyQt6.uic import loadUi

from src.main.python.components.logger import *
from src.main.python.infoscreens.errorMessage import errorMessage
from src.main.python.learninggame import learnWindow


class ChooseLearningUI(QMainWindow):
    def __init__(self, username, parent, theme):
        try:
            if username is None or username == "":
                raise Exception("Hiba: Felhasználó nem található!")

            self.username = username
            default = "default"

            super(ChooseLearningUI, self).__init__()

            self.theme = theme
            self.setWindowIcon(QIcon("../resources/icon/icon.ico"))
            loadUi(f"../resources/ui/{self.theme}/{self.theme}ChooseLearning.ui", self)

            self.setFixedSize(self.size())

            self.parent = parent

            self.selfReplicating = self.findChild(QPushButton, "selfReplicating")
            self.deceptive = self.findChild(QPushButton, "deceptive")
            self.nuisance = self.findChild(QPushButton, "nuisance")
            self.concealing = self.findChild(QPushButton, "concealing")
            self.informationTheft = self.findChild(QPushButton, "informationTheft")
            self.networkBased = self.findChild(QPushButton, "networkBased")
            self.deliveryMechanism = self.findChild(QPushButton, "deliveryMechanism")
            self.evading = self.findChild(QPushButton, "evading")
            self.psychologicalBased = self.findChild(QPushButton, "psychologicalBased")
            self.otherTargeted = self.findChild(QPushButton, "otherTargeted")
            self.backButton = self.findChild(QPushButton, "backButton")

            self.learnScreen = None

            self.selfReplicating.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson = "Önsokszorosító kártevők",
                                             nameOfData = "selfrecplicating"
                                             )
            )

            self.deceptive.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson = "Megtévesztő kártevők",
                                             nameOfData="deceptive"
                                             )
            )

            self.nuisance.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson = "Zavaró kártevők",
                                             nameOfData="nuisance"
                                             )
            )

            self.concealing.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson = "Rejtőzködő kártevők",
                                             nameOfData="concealing"
                                             )
            )

            self.informationTheft.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson="Adatlopó kártevők",
                                             nameOfData="informationtheft"
                                             )
            )

            self.networkBased.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson="Hálózati kártevők",
                                             nameOfData="networkbased"
                                             )
            )

            self.deliveryMechanism.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson="Terjedésre specializált kártevők",
                                             nameOfData="deliverymechanism"
                                             )
            )

            self.evading.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson="Észleléselkerülő kártevők",
                                             nameOfData="evading"
                                             )
            )

            self.psychologicalBased.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson="Pszichológiai kártevők",
                                             nameOfData="psychologicalbased"
                                             )
            )

            self.otherTargeted.clicked.connect(
                lambda: self.openLearnWindow(username,
                                             parent,
                                             typeOfLesson="Egyéb célpontú kártevők",
                                             nameOfData="othertargeted"
                                             )
            )

            self.backButton.clicked.connect(self.close)

        except Exception as e:
            errorMessage(e)
            self.hide()

    def openLearnWindow(self, username, parent, typeOfLesson, nameOfData):
        if not self.learnScreen:
            self.learnScreen = learnWindow.LearnWindowUI(self, username, parent, typeOfLesson, nameOfData, self.theme)
        else:
            self.learnScreen = None
            self.learnScreen = learnWindow.LearnWindowUI(self, username, parent, typeOfLesson, nameOfData, self.theme)

        logger.info(f"{typeOfLesson} lecke megnyitása!")
        self.learnScreen.show()
        self.hide()
        self.parent.hide()
