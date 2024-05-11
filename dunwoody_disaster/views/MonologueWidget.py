import pygame
import json
from PySide6.QtWidgets import QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout
from PySide6.QtGui import QPixmap, QFont, QKeyEvent
from PySide6.QtCore import QTimer, Qt
from typing import Callable

from dunwoody_disaster import AUDIO
import dunwoody_disaster as DD
from dunwoody_disaster.CharacterFactory import Character


class MonologueWidget(QWidget):
    def __init__(self, char: Character, transition_callback: Callable):
        super().__init__()
        # Initialization of the widget, setting up character, dialogue management, and callbacks.
        self.char = char
        self.current_dialogue_index = 0
        self.char_index = 0
        self.transition_callback = transition_callback

        self.initUI()  # Set up the user interface elements.
        self.initSound()  # Initialize audio components.
        self.loadDialogue()  # Load character-specific dialogue from JSON files.

    def initUI(self):
        # Configures the layout, adds character image, dialogue text area, and navigation button.
        layout = QVBoxLayout(self)
        self.char_img = QLabel(self)
        self.char_img.setPixmap(QPixmap(self.char.image()))
        layout.addWidget(self.char_img)

        self.dialogueText = QTextEdit(self)
        self.dialogueText.setFont(QFont("Arial", 16))
        self.dialogueText.setReadOnly(True)
        layout.addWidget(self.dialogueText)

        self.nextButton = QPushButton("Next", self)
        self.nextButton.clicked.connect(self.display_next_dialogue)
        layout.addWidget(self.nextButton)

        self.timer = QTimer(self)
        self.timer.timeout.connect(
            self.add_char
        )  # Timer to control the typewriter effect.

    def initSound(self):
        # Initializes the sound system, loading and setting volume for typewriter sound.
        pygame.mixer.init()
        try:
            self.typewriter_sound = pygame.mixer.Sound(AUDIO["TypeWriterSound"])
        except KeyError:
            print("Audio key 'typewriter_click.wav' not found in AUDIO dictionary")
        self.typewriter_sound.set_volume(0.5)

    def stopAllSounds(self):
        # Stops all currently playing sounds.
        pygame.mixer.stop()

    def loadDialogue(self):
        # Loads and parses the character dialogue from a JSON file.
        path = f"{DD.BASE_PATH}/monologues/{self.char.name}.json"
        try:
            with open(path, "r") as f:
                self._char_monologue = json.load(f).get("victory", ["victory"])
        except FileNotFoundError:
            print(f"Dialogue file {path} not found")
            self._char_monologue = ["No dialogue found."]
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {path}")
            self._char_monologue = ["Error in dialogue format."]

        self.display_next_dialogue()  # Immediately begin displaying the dialogue.

    def add_char(self):
        # Adds characters one by one to the dialogue text box to simulate a typewriter effect.
        if self.char_index < len(self.current_text):
            self.dialogueText.insertPlainText(self.current_text[self.char_index])
            self.char_index += 1
            if not pygame.mixer.get_busy():
                self.typewriter_sound.play()
        else:
            self.timer.stop()
            self.nextButton.setDisabled(False)

    def display_next_dialogue(self):
        # Manages the display of dialogue pieces, controlling sound and UI components.
        self.stopAllSounds()
        if self.current_dialogue_index < len(self._char_monologue):
            self.current_text = self._char_monologue[self.current_dialogue_index]
            self.char_index = 0
            self.dialogueText.clear()
            self.timer.start(50)
            self.nextButton.setDisabled(True)
            self.current_dialogue_index += 1
        else:
            self.transition_callback()  # Trigger callback once all dialogues are displayed.

    def keyPressEvent(self, event: QKeyEvent):
        # Handling Enter or Return key press to quickly finish displaying current text
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.timer.stop()  # Stop the typewriter effect
            self.typewriter_sound.stop()  # Stop the typing sound, if playing
            self.dialogueText.setPlainText(
                self.current_text
            )  # Display the full text of the dialogue
            self.nextButton.setDisabled(False)  # Enable the Next button
            event.accept()  # Mark the event as handled
        else:
            super().keyPressEvent(
                event
            )  # Call the base class method to handle other key presses
