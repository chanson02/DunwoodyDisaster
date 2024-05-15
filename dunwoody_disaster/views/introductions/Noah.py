from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QSizePolicy,
    QSpacerItem,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QMouseEvent, QPixmap, QFont

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

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        row = 0

        layout.addItem(
            QSpacerItem(50, 30, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding), row, 0
        )
        row += 1

        pic1 = QLabel()
        weaponPix = QPixmap(DD.ASSETS["Power Chord"])
        weaponPix = weaponPix.scaledToWidth(300)
        pic1.setPixmap(weaponPix)
        pic1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pic1.mousePressEvent = self.setCheat
        layout.addWidget(pic1, row, 2)
        row += 1

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
        layout.addLayout(tb, row, 2)

        pic = QLabel()
        pic.setPixmap(character.image().scaledToWidth(500))
        pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(pic, row, 1)
        row += 1

        layout.addItem(
            QSpacerItem(0, 30, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding), row, 1
        )
        row += 1

        btn_lyt = QGridLayout()
        btn_lyt.setContentsMargins(0, 0, 0, 0)
        btn_lyt.setSpacing(0)

        btn_lyt.addItem(
            QSpacerItem(50, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed), 0, 0
        )

        btn = QPushButton("Start")
        btn.setFont(QFont("blood crow", 36))
        btn.setStyleSheet("font-size: 18px;")
        btn.clicked.connect(self._callback)
        btn_lyt.addWidget(btn, 0, 1)

        btn_lyt.addItem(
            QSpacerItem(50, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed), 0, 2
        )

        layout.addLayout(btn_lyt, row, 2)
        row += 1

        layout.addItem(
            QSpacerItem(50, 50, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding), row, 3
        )

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
