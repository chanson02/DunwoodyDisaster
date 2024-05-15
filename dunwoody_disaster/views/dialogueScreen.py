from PySide6.QtWidgets import (
    QWidget,
    QStackedLayout,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QSpacerItem, 
    QSizePolicy
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QKeyEvent, QPixmap, QFont
from dunwoody_disaster.CharacterFactory import Character
import dunwoody_disaster as DD
from dunwoody_disaster import AUDIO
from typing import Callable
import json
import pygame


# Dialogue screen between boss and users
class DialogueScreen(QWidget):
    def __init__(self, char1: Character, char2: Character):
        """
        A screen to show two characters having a conversation
        :param char1: The character to show on the left side
        :param char2: The character to show on the right side

        :example:
            dls = DialogueScreen(p1, p2)
            dls.set_dialogue(["Hi! I'm player 1"], ["Nice to meet you, I'm player 2"])
            dls.onComplete(callback)
        """

        super().__init__()
        self.char1 = char1  # Player character
        self.char2 = char2  # Boss character

        self.current_dialogue = ""
        self.char_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.type_text)

        self.char1_img = QLabel()
        self.char1_img.setPixmap(
            QPixmap(self.char1.image()).scaled(500, 500, Qt.KeepAspectRatio)
        )
        self.char1_img.setAlignment(Qt.AlignCenter)

        self.char2_img = QLabel()
        self.char2_img.setPixmap(
            QPixmap(self.char2.image()).scaled(500, 500, Qt.KeepAspectRatio)
        )
        self.char2_img.setAlignment(Qt.AlignCenter)

        self.char1_dialogue = QLabel()
        self.char2_dialogue = QLabel()

        self.dialogue_stack = QStackedLayout()

        self.init_ui()
        self.loadDialogue()
        self.initSound()
        DD.clickable(self).connect(self.next_dialogue)
        self._callback = DD.unimplemented

    def keyPressEvent(self, event: QKeyEvent):
        k = event.key()
        if k == Qt.Key.Key_Enter or k == Qt.Key.Key_Return:
            self.next_dialogue()
        return

    def set_dialogue(self, char1: list[str], char2: list[str]):
        self._char1_dialogue = char1
        self._char2_dialogue = char2
        self._index = 0
        self.next_dialogue()

    def onComplete(self, callback: Callable):
        self._callback = callback

    def loadDialogue(self):
        path = f"{DD.BASE_PATH}/dialogues/{self.char2.name}.json"
        try:
            with open(path, "r") as f:
                dialogue = json.load(f)
        except FileNotFoundError:
            print(f"Dialogue file {path} not found")
            return

        try:
            lines = dialogue[self.char1.name]
        except KeyError:
            print(
                f"Dialogue file {path} has no dialogue for character {self.char1.name}"
            )
            return

        self.set_dialogue(lines["protagonist_lines"], lines["antagonist_lines"])
        return

    def init_ui(self):
        dialogue_font = QFont(
            "Times New Roman", 16, QFont.Bold
        )  # Example: "Times New Roman", size 16, bold
        self.char1_dialogue.setFont(dialogue_font)
        self.char2_dialogue.setFont(dialogue_font)

        main_layout = QVBoxLayout(self)

        char1_group = QGroupBox()
        char2_group = QGroupBox()

        char1_group.setStyleSheet("QGroupBox { border: None; }")
        char2_group.setStyleSheet("QGroupBox { border: None; }")

        char1_layout = QVBoxLayout()
        char2_layout = QVBoxLayout()

        char1_name_label = QLabel(self.char1.name)
        char2_name_label = QLabel(self.char2.name)
        char1_name_label.setAlignment(Qt.AlignCenter)
        char2_name_label.setAlignment(Qt.AlignCenter)
        char1_name_label.setFont(QFont("Blood Crow", 24, QFont.Bold))
        char2_name_label.setFont(QFont("Blood Crow", 24, QFont.Bold))

        self.char1_img = QLabel()
        self.char1_img.setPixmap(
            QPixmap(self.char1.image()).scaledToHeight(450)
        )
        self.char1_img.setAlignment(Qt.AlignCenter)

        self.char2_img = QLabel()
        self.char2_img.setPixmap(
            QPixmap(self.char2.image()).scaledToHeight(450)
        )
        self.char2_img.setAlignment(Qt.AlignCenter)

        self.char1_dialogue = QLabel()
        self.char2_dialogue = QLabel()

        self.char1_dialogue.setAlignment(Qt.AlignCenter)
        self.char2_dialogue.setAlignment(Qt.AlignCenter)

        # Apply styles to dialogue QLabel widgets
        dialogue_style = """
        QLabel {
            background-color: #000000;
            border: 2px solid #444444;
            border-radius: 10px;
            padding: 10px;
            font-size: 20px;
            font-family: "JMH Typewriter";
        }
        """
        self.char1_dialogue.setStyleSheet(dialogue_style)
        self.char2_dialogue.setStyleSheet(dialogue_style)
        self.char1_dialogue.setWordWrap(True)
        self.char2_dialogue.setWordWrap(True)

        char1_layout.addWidget(char1_name_label)
        char1_layout.addWidget(self.char1_img)
        char1_layout.addWidget(self.char1_dialogue)
        char2_layout.addWidget(char2_name_label)
        char2_layout.addWidget(self.char2_img)
        char2_layout.addWidget(self.char2_dialogue)

        char1_group.setLayout(char1_layout)
        char2_group.setLayout(char2_layout)

        characters_layout = QHBoxLayout()
        characters_layout.addWidget(char1_group)
        characters_layout.addWidget(char2_group)

        main_layout.addLayout(characters_layout)
        main_layout.addItem(QSpacerItem(0, 40, QSizePolicy.Fixed, QSizePolicy.Fixed))

    def initSound(self):
        pygame.mixer.init()
        self.TypeWriterSound = pygame.mixer.Sound(AUDIO["TypeWriterSound"])
        self.TypeWriterSound.set_volume(0.9)

    def next_dialogue(self):
        if self.timer.isActive():
            self.timer.stop()
            if self.current_speaker == 0:
                self.char1_dialogue.setText(self.current_dialogue)
            else:
                self.char2_dialogue.setText(self.current_dialogue)
            return

        index = self._index // 2
        char = self._index % 2
        self.current_speaker = char

        try:
            if char == 0:
                self.current_dialogue = self._char1_dialogue[index]
                self.char1_dialogue.clear()
            else:
                self.current_dialogue = self._char2_dialogue[index]
                self.char2_dialogue.clear()

            self.char_index = 0
            self.timer.start(50)  # Adjust speed as needed
        except IndexError:
            self.deleteLater()
            if self._callback:
                self._callback()

        self._index += 1

    def type_text(self):
        if self.char_index < len(self.current_dialogue):
            # Play sound with each character
            if (
                not pygame.mixer.get_busy()
            ):  # Check if the sound is not currently playing
                self.TypeWriterSound.stop()  # Ensure any currently playing sound is stopped
                self.TypeWriterSound.play()

            if self.current_speaker == 0:
                self.char1_dialogue.setText(
                    self.char1_dialogue.text() + self.current_dialogue[self.char_index]
                )
            else:
                self.char2_dialogue.setText(
                    self.char2_dialogue.text() + self.current_dialogue[self.char_index]
                )
            self.char_index += 1
        else:
            self.timer.stop()
