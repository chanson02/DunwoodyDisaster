import pygame
import json
import os  # Ensure you import os to use os.path.join for path construction

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtGui import QPixmap, QFont, QKeyEvent
from PySide6.QtCore import QTimer, Qt
from typing import Callable

from dunwoody_disaster import AUDIO
import dunwoody_disaster as DD
from dunwoody_disaster.CharacterFactory import Character


# Define a QWidget-based class to manage monologue display in a game
class MonologueWidget(QWidget):
    # Initialize the widget with a character object and a transition callback function
    def __init__(self, char: Character, event_id: str, transition_callback: Callable):
        super().__init__()
        self.char = (
            char  # Store reference to the character whose dialogue will be displayed
        )
        self.current_dialogue_index = (
            0  # Index to keep track of the current dialogue being displayed
        )
        self.char_index = 0  # Index to keep track of the current character being displayed in the typewriter effect
        self.transition_callback = (
            transition_callback  # Store the callback function for transition
        )
        self.event_id = event_id

        self.initUI()  # Setup the user interface components
        self.initSound()  # Setup sound components
        self.loadDialogue()  # Load dialogue data from files

    def initUI(self):
        # Create the main layout
        mainLayout = QGridLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)

        row = 0

        mainLayout.addItem(
            QSpacerItem(50, 30, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding), row, 0
        )
        row += 1

        # Configures the character image, making it larger and positioned to the left
        self.char_img = QLabel(self)
        self.char_img.setPixmap(
            QPixmap(self.char.image()).scaledToHeight(600)
        )  # Scale image
        self.char_img.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        mainLayout.addWidget(self.char_img, row, 1)

        # Create a layout for text and buttons on the right
        textLayout = QVBoxLayout()

        # Text edit to show dialogue
        self.dialogueText = QTextEdit(self)
        self.dialogueText.setFont(QFont("Arial", 14))
        self.dialogueText.setReadOnly(True)
        self.dialogueText.setMaximumHeight(800)  # Limit the height of the chatbox
        textLayout.addWidget(self.dialogueText)

        textLayout.addItem(QSpacerItem(0, 30, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # Button to move to the next dialogue
        self.nextButton = QPushButton("Next", self)
        self.nextButton.setStyleSheet("font-size: 24px;")
        self.nextButton.clicked.connect(self.display_next_dialogue)
        self.nextButton.setMaximumHeight(50)  # Limit the height of the button
        textLayout.addWidget(self.nextButton)

        mainLayout.addItem(
            QSpacerItem(50, 0, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 2
        )
        # Add textLayout to the mainLayout
        mainLayout.addLayout(textLayout, row, 3)
        row += 1

        mainLayout.addItem(
            QSpacerItem(50, 30, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding), row, 4
        )

        self.timer = QTimer(self)
        self.timer.timeout.connect(
            self.add_char
        )  # Timer to control the typewriter effect

    def initSound(self):
        pygame.mixer.init()
        self.typewriter_sound = pygame.mixer.Sound(AUDIO["TypeWriterSound"])
        self.typewriter_sound.set_volume(0.5)

    def stopAllSounds(self):
        pygame.mixer.stop()

    # Load dialogue data from a JSON file

    def loadDialogue(self):
        # Construct the file path more reliably
        path = os.path.join(
            DD.BASE_PATH, "monologues", self.char.name, f"{self.event_id}.json"
        )

        try:
            with open(path, "r") as f:
                data = json.load(f)

            # Assuming the JSON structure is { "Example":"victory": ["line1", "line2"] }
            character_monologue = data.get(self.char.name, {})
            victory_dialogue = character_monologue.get(
                "monologue", ["No victory dialogue found."]
            )
            self.set_dialogue(victory_dialogue)
        except FileNotFoundError:
            print(f"Dialogue file {path} not found")
            self.set_dialogue(["No dialogue file found."])
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {path}")
            self.set_dialogue(["Error in dialogue format."])

    # Add characters of the dialogue one by one to simulate typewriter effect
    def add_char(self):
        if self.char_index < len(self.current_text):
            self.dialogueText.insertPlainText(
                self.current_text[self.char_index]
            )  # Insert the next character
            self.char_index += 1  # Move to the next character
            if not pygame.mixer.get_busy():
                self.typewriter_sound.play()  # Play typewriter sound if not already playing
        else:
            self.timer.stop()  # Stop the timer if end of text is reached
            self.nextButton.setDisabled(False)  # Enable the 'Next' button

    # Display the next dialogue in the sequence
    def display_next_dialogue(self):
        self.stopAllSounds()  # Stop all playing sounds
        if self.current_dialogue_index < len(self._char_monologue):
            self.current_text = self._char_monologue[
                self.current_dialogue_index
            ]  # Get the current dialogue text
            self.char_index = 0  # Reset character index for typewriter effect
            self.dialogueText.clear()  # Clear the text box
            self.timer.start(50)  # Start the timer for typewriter effect
            self.nextButton.setDisabled(True)  # Disable the 'Next' button while typing
            self.current_dialogue_index += 1  # Increment the dialogue index
        else:
            self.transition_callback()  # Call the transition callback when all dialogues are shown

    def set_dialogue(self, dialogues):
        if not dialogues:
            dialogues = ["No dialogue available."]
        self._char_monologue = dialogues
        self.current_dialogue_index = 0
        self.display_next_dialogue()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.timer.stop()
            self.typewriter_sound.stop()
            self.dialogueText.setPlainText(self.current_text)
            self.display_next_dialogue()
            self.nextButton.setDisabled(False)
            event.accept()
        else:
            super().keyPressEvent(event)
