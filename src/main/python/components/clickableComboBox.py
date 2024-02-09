from PyQt6.QtWidgets import QLineEdit


class ClickableLineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.isOpen = False

    def mousePressEvent(self, event):
        if not self.isOpen:
            self.parent.showPopup()
            self.isOpen = True
        else:
            self.parent.hidePopup()
            self.isOpen = False
