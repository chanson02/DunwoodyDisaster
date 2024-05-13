import pygame
import json
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
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
    def __init__(self, char: Character, transition_callback: Callable):
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

        self.initUI()  # Setup the user interface components
        self.initSound()  # Setup sound components
        self.loadDialogue()  # Load dialogue data from files

    def initUI(self):
        # Create the main layout
        mainLayout = QHBoxLayout(self)

        # Configures the character image, making it larger and positioned to the left
        self.char_img = QLabel(self)
        self.char_img.setPixmap(
            QPixmap(self.char.image()).scaled(800, 800, Qt.KeepAspectRatio)
        )  # Scale image
        self.char_img.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        mainLayout.addWidget(self.char_img)

        # Create a layout for text and buttons on the right
        textLayout = QVBoxLayout()

        # Text edit to show dialogue
        self.dialogueText = QTextEdit(self)
        self.dialogueText.setFont(QFont("Arial", 14))
        self.dialogueText.setReadOnly(True)
        self.dialogueText.setMaximumHeight(800)  # Limit the height of the chatbox
        textLayout.addWidget(self.dialogueText)

        # Button to move to the next dialogue
        self.nextButton = QPushButton("Next", self)
        self.nextButton.clicked.connect(self.display_next_dialogue)
        self.nextButton.setMaximumHeight(50)  # Limit the height of the button
        textLayout.addWidget(self.nextButton)

        # Add textLayout to the mainLayout
        mainLayout.addLayout(textLayout, 1)

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
        path = f"{DD.BASE_PATH}/monologues/{self.char.name}.json"  # Construct the file path
        try:
            with open(path, "r") as f:
                data = json.load(f)  # Load the JSON data from the file
            dialogues = data.get(self.char.name, {})  # Get dialogues for the character
            victory_dialogue = dialogues.get(
                "victory", ["No victory dialogue found."]
            )  # Get victory dialogues or default message
            self.set_dialogue(victory_dialogue)  # Set the loaded dialogue for display
        except FileNotFoundError:
            print(f"Dialogue file {path} not found")  # Handle file not found error
            self.set_dialogue(["No dialogue file found."])  # Set default error message
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {path}")  # Handle JSON decoding error
            self.set_dialogue(
                ["Error in dialogue format."]
            )  # Set default error message

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
