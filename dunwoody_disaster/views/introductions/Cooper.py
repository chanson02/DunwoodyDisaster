from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QFont

from dunwoody_disaster.CharacterFactory import Character
from typing import Callable


class CooperIntroScreen(QWidget):
    def __init__(self, character: Character, transition_callback: Callable):
        super().__init__()
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

        pic = QLabel()
        pic.setPixmap(character.image().scaledToWidth(500))
        pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(pic, row, 1)

        text = """
        Meet Cooper, the {tbd} programmer!
        Even though he's not the best with his hands, he loves to build things.
        Especially keyboards and cars.
        Join him on his epic adventure through Dunwoody College of Techology
        where he will encounter many hardships on his path to a righteous Software Engineering degree.
        """

        tb = self.text_box(" ".join(text.split()))
        layout.addLayout(tb, row, 2)

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

        layout.addLayout(btn_lyt, row, 1, 1, 2)
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

    def text_box(self, text: str) -> QVBoxLayout:
        lbl = QLabel(text)
        lbl.setStyleSheet(self.text_styles)
        lbl.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(lbl)
        return layout
