import pygame
from PySide6.QtWidgets import QWidget, QLabel, QTextEdit, QHBoxLayout, QPushButton
from PySide6.QtGui import QPixmap, QFont, QIcon, QKeyEvent
from PySide6.QtCore import Qt, QTimer

from dunwoody_disaster import ASSETS, AUDIO


class CharacterDetailWidget(QWidget):

    def __init__(self, character, transition_callback):
        super().__init__()
        self.character = character
        self.transition_callback = transition_callback
        self.initUI()
        self.initSound()

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
        background_description = QFont("JMH Typewriter", 20)
        self.backgroundEdit.setFont(background_description)
        self.backgroundEdit.setReadOnly(True)
        layout.addWidget(self.backgroundEdit)

        # Button to transition to map screen
        self.mapButton = QPushButton("Go to Map")
        self.mapButton.setIcon(QIcon(ASSETS["SSL Certificate"]))
        self.mapButton.clicked.connect(self.transition_callback)
        self.mapButton.setDisabled(True)
        layout.addWidget(self.mapButton)

        self.setLayout(layout)

        # Timer setup for typewriter effect
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.add_char)
        self.char_index = 0
        self.character_description = getattr(
            self.character, "description", "No description available."
        )
        self.timer.start(50)

    def initSound(self):
        pygame.mixer.init()
        self.TypeWriterSound = pygame.mixer.Sound(AUDIO["TypeWriterSound"])
        self.TypeWriterSound.set_volume(0.9)

    def add_char(self):
        if self.char_index < len(self.character_description):
            current_text = self.backgroundEdit.toPlainText()
            current_text += self.character_description[self.char_index]
            self.backgroundEdit.setText(current_text)
            self.char_index += 1
            # Play sound with each character
            if (
                not pygame.mixer.get_busy()
            ):  # Check if the sound is not currently playing
                self.TypeWriterSound.stop()  # Ensure any currently playing sound is stopped
                self.TypeWriterSound.play()
        else:
            self.timer.stop()  # Stop the timer if the text is complete
            self.mapButton.setDisabled(False)  # Enable the button when typing is done

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.timer.stop()  # Stop the typing effect
            self.TypeWriterSound.stop()  # Stop the typing sound
            self.backgroundEdit.setText(
                self.character_description
            )  # Set the complete text
            self.mapButton.setDisabled(False)  # Enable the button immediately
            event.accept()  # Mark the event as handled
        else:
            super().keyPressEvent(
                event
            )  # Call the base class method to handle other key presses
