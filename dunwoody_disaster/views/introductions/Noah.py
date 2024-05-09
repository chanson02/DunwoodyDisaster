from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

from dunwoody_disaster.CharacterFactory import Character
from typing import Callable


class NoahIntroScreen(QWidget):
    def __init__(self, character: Character, transition_callback: Callable):
        super().__init__()
        self.text_styles = "font-size: 24px;"
        self._callback = transition_callback

        layout = QVBoxLayout()
        self.setLayout(layout)

        text = """
        Meet Cooper, the {tbd} programmer!
        Even though he's not the best with his hands, he loves to build things.
        Especially keyboards and cars.
        Join him on his epic adventure through Dunwoody College of Techology
        where he will encounter many hardships on his path to a righteous Software Engineering degree.
        """

        tb = self.text_box(" ".join(text.split()))
        layout.addLayout(tb)

        pic = QLabel()
        pic.setPixmap(character.image().scaledToWidth(500))
        pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(pic)

        text = """
        Use the mouse to select different classrooms.
        Press "Return" to enter the classroom.
        Click through the dialogue to learn about your opponent before battle!
        Defeat enemies by outsmarting them in programming challenges.
        Learn from your teachers as you beat their classes.
        """
        frmt = (
            " ".join([t for t in text.split(" ") if t != ""])
            .strip()
            .replace("\n ", "\n")
        )
        tb = self.text_box(frmt)
        tb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(tb)

        btn = QPushButton("Start")
        btn.clicked.connect(self._callback)
        layout.addWidget(btn)

        return

    def text_box(self, text: str) -> QVBoxLayout:
        lbl = QLabel(text)
        lbl.setStyleSheet(self.text_styles)
        lbl.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(lbl)
        return layout
