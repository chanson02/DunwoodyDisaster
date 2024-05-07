import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class CharacterDetailWidget(QWidget):
    def __init__(self, character):
        super().__init__()
        self.character = character
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.imageLabel = QLabel(self)
        pixmap = QPixmap(self.character.image()).scaled(300, 400, Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(pixmap)
        layout.addWidget(self.imageLabel)

        self.backgroundEdit = QTextEdit(self)
        # Use getattr to safely access the description attribute, defaulting to an empty string if not found
        character_description = getattr(
            self.character, "description", "No description available."
        )
        self.backgroundEdit.setText(
            self.character.description
        )  # Assuming each character has a 'description' attribute
        self.backgroundEdit.setReadOnly(True)
        layout.addWidget(self.backgroundEdit)

        self.setLayout(layout)
