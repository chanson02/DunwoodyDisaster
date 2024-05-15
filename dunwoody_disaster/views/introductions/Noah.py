from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QMouseEvent, QPixmap

from dunwoody_disaster.CharacterFactory import Character
from typing import Callable
import dunwoody_disaster as DD


class NoahIntroScreen(QWidget):
    def __init__(self, character: Character, transition_callback: Callable):
        super().__init__()
        self.character = character
        self.setStyleSheet('font-family: "Futura Bk BT";')
        self.text_styles = "font-size: 24px;"
        self._callback = transition_callback

        layout = QVBoxLayout()
        self.setLayout(layout)

        text = """
        Meet Noah, the, um, *Shuffles papers* something something something.
        Hmm I could have sworn I had my notes
        No matter, Noah is a student at Dunwoody.
        He doesn't get out much, not sure he even knows what the sun looks like.
        I think he said he's just gonna put some earbuds in and ignore everyone.
        Kinda mean if you ask me, but hey, who am I to judge?
        Also I lost my notes on him so I'm just gonna make stuff up.
        I was just gonna put the entire script of the Bee Movie here.
        But I think that's a bit too much.
        Oh Btw,
        He may or may not have just taken this
        start screen from a different programmer.
        Probably should give him credit
        Anyway, let's get started!
        """

        tb = self.text_box(" ".join(text.split()))
        layout.addLayout(tb)

        pic1 = QLabel()
        weaponPix = QPixmap(DD.ASSETS["Power Chord"])
        weaponPix = weaponPix.scaledToWidth(300)
        pic1.setPixmap(weaponPix)
        pic1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pic1.mousePressEvent = self.setCheat
        layout.addWidget(pic1)

        pic = QLabel()
        pic.setPixmap(character.image().scaledToWidth(500))
        pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(pic)

        text = """
        Use the mouse to select different classrooms.
        Press "Return" to enter the classroom.
        "-Cooper wuz here"
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

    def keyPressEvent(self, event: QKeyEvent):
        k = event.key()
        if k == Qt.Key.Key_Enter or k == Qt.Key.Key_Return:
            self._callback()
        return

    def setCheat(self, event: QMouseEvent):
        self.character.maxHealth = 10000
        self.character.health = self.character.maxHealth
        self.character.set_health(self.character.maxHealth)

    def text_box(self, text: str) -> QVBoxLayout:
        lbl = QLabel(text)
        lbl.setStyleSheet(self.text_styles)
        lbl.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(lbl)
        return layout
