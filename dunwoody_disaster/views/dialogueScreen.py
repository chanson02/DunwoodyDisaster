from PySide6.QtWidgets import (
    QWidget,
    QStackedLayout,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QGroupBox,
)
from dunwoody_disaster.CharacterFactory import Character
import dunwoody_disaster as DD
from typing import Callable


class DialogueScreen(QWidget):
    def __init__(self, char1: Character, char2: Character):
        """
        A screen to show two characters having a conversation
        :param char1: The character to show on the left side
        :param char2: The character to show on the right side
        """
        super().__init__()
        self._index = 0
        self.char1 = char1
        self.char2 = char2

        self._char1_dialogue = []
        self._char2_dialogue = []

        self.char1_img = QLabel("")
        self.char1_img.setPixmap(self.char1.image())
        self.char2_img = QLabel("")
        self.char2_img.setPixmap(self.char2.image())
        self.char1_dialogue = QLabel("")
        self.char2_dialogue = QLabel("")

        self.init_ui()
        DD.clickable(self).connect(self.next_dialogue)
        self._callback = DD.unimplemented

    def set_dialogue(self, char1: list[str], char2: list[str]):
        self._char1_dialogue = char1
        self._char2_dialogue = char2
        self._index = 0
        self.next_dialogue()

    def onComplete(self, callback: Callable):
        self._callback = callback

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        player_layout = QHBoxLayout()
        layout.addLayout(player_layout)
        player_layout.addWidget(self.char1_img)
        player_layout.addWidget(self.char2_img)

        self.dialogue_stack = QStackedLayout()
        layout.addLayout(self.dialogue_stack)

        # Player 1 dialogue box
        player1_dialogue_box = QGroupBox(self.char1.name)
        container = QHBoxLayout()
        container.addWidget(self.char1_dialogue)
        player1_dialogue_box.setLayout(container)
        self.dialogue_stack.addWidget(player1_dialogue_box)

        # Player 2 dialogue box
        player2_dialogue_box = QGroupBox(self.char2.name)
        container = QHBoxLayout()
        container.addWidget(self.char2_dialogue)
        player2_dialogue_box.setLayout(container)
        self.dialogue_stack.addWidget(player2_dialogue_box)

        # self.next_dialogue()

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
