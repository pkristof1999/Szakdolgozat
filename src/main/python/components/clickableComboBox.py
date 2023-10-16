from PyQt6.QtWidgets import QLineEdit


class ClickableLineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def mousePressEvent(self, event):
        self.parent.showPopup()
