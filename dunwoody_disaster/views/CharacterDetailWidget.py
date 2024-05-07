import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QTextEdit,
    QHBoxLayout,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont


class CharacterDetailWidget(QWidget):

    def __init__(self, character):
        super().__init__()
        self.character = character
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        # Image setup
        self.imageLabel = QLabel(self)
        pixmap = QPixmap(self.character.image()).scaled(
            500, 600, Qt.AspectRatioMode.KeepAspectRatio
        )
        self.imageLabel.setPixmap(pixmap)
        layout.addWidget(self.imageLabel)

        # Text edit for description with typewriter effect
        self.backgroundEdit = QTextEdit(self)
        background_description = QFont("JMH Typewriter", 12)
        self.backgroundEdit.setFont(background_description)
        self.backgroundEdit.setReadOnly(True)
        layout.addWidget(self.backgroundEdit)

        self.setLayout(layout)

        # Timer setup for typewriter effect
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.add_char)
        self.char_index = 0
        self.character_description = getattr(
            self.character, "description", "No description available."
        )
        self.timer.start(50)  # Adjust interval for typing speed

    def add_char(self):
        if self.char_index < len(self.character_description):
            current_text = self.backgroundEdit.toPlainText()
            current_text += self.character_description[self.char_index]
            self.backgroundEdit.setText(current_text)
            self.char_index += 1
        else:
            self.timer.stop()  # Stop the timer if the text is complete
