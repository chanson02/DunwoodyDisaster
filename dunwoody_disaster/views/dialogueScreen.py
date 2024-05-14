from PySide6.QtWidgets import (
    QWidget,
    QStackedLayout,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QGroupBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QPixmap, QFont
from dunwoody_disaster.CharacterFactory import Character
import dunwoody_disaster as DD
from typing import Callable
import json


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
        main_layout = QVBoxLayout(self)

        # Create group boxes for each character
        char1_group = QGroupBox()
        char2_group = QGroupBox()

        # Create vertical layouts for each character's image and dialogue
        char1_layout = QVBoxLayout()
        char2_layout = QVBoxLayout()

        # Labels to display character names
        char1_name_label = QLabel(self.char1.name)
        char2_name_label = QLabel(self.char2.name)
        char1_name_label.setAlignment(Qt.AlignCenter)
        char2_name_label.setAlignment(Qt.AlignCenter)
        char1_name_label.setFont(QFont("Blood Crow", 14, QFont.Bold))
        char2_name_label.setFont(QFont("Blood Crow", 14, QFont.Bold))

        # Set font size for dialogue text
        dialogue_font = QFont("JMH Typewriter", 12)
        dialogue_font.setPointSize(18)  # Larger text size
        self.char1_dialogue.setFont(dialogue_font)
        self.char2_dialogue.setFont(dialogue_font)
        self.char1_dialogue.setWordWrap(True)
        self.char2_dialogue.setWordWrap(True)

        # Adjust size and properties of dialogue labels
        self.char1_dialogue.setFixedHeight(
            250
        )  # Half the height of the character image
        self.char2_dialogue.setFixedHeight(250)
        self.char1_dialogue.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.char2_dialogue.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        # Add widgets to layouts
        char1_layout.addWidget(char1_name_label)
        char1_layout.addWidget(self.char1_img)
        char1_layout.addWidget(self.char1_dialogue)
        char2_layout.addWidget(char2_name_label)
        char2_layout.addWidget(self.char2_img)
        char2_layout.addWidget(self.char2_dialogue)

        # Set layouts to group boxes
        char1_group.setLayout(char1_layout)
        char2_group.setLayout(char2_layout)

        # Horizontal layout to hold both character group boxes
        characters_layout = QHBoxLayout()
        characters_layout.addWidget(char1_group)
        characters_layout.addWidget(char2_group)

        main_layout.addLayout(characters_layout)

    def next_dialogue(self):
        index = self._index // 2
        char = self._index % 2

        try:
            if char == 0:
                self.char1_dialogue.setText(self._char1_dialogue[index])
            else:
                self.char2_dialogue.setText(self._char2_dialogue[index])
        except IndexError:
            # There is no more dialogue
            self.deleteLater()
            self._callback()

        self.dialogue_stack.setCurrentIndex(char)
        self._index += 1
        return
