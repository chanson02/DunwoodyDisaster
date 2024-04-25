from PySide6.QtCore import QTimer

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
    QStackedLayout,
)
from dunwoody_disaster.views.arsenal import Arsenal
import dunwoody_disaster as DD
from dunwoody_disaster.CharacterFactory import Character
from dunwoody_disaster.views.characterState import CharacterState
from dunwoody_disaster.views.action_selector import ActionSelector
from dunwoody_disaster.FightSequence import FightSequence
from dunwoody_disaster.views.victoryScreen import VictoryScreen


class FightScreen(QWidget):
    def __init__(self, player1: Character, player2: Character):
        super().__init__()
        self.player1 = player1
        self.player2 = player2
        self.fightSequence = FightSequence(self.player1, self.player2)

        self.p1_selector = ActionSelector()
        self.p2_selector = ActionSelector()

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        row = 0
        colm = 0

        layout.addItem(
                QSpacerItem(30, 50, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed),
                #QSpacerItem(30, 50, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding),
                row,
                colm,
                )
        colm += 1

        arsenal = Arsenal(self.p1_selector, self.player1.weapons, self.player1.defenses)
        col_size = 2
        layout.addWidget(arsenal, row, colm, 1, col_size)
        colm += col_size

        layout.addItem(
                DD.expander(True, False),
                row,
                colm
                )
        colm += 1

        col_size = 4
        p1 = CharacterState(self.player1)
        p2 = CharacterState(self.player2)
        layout.addWidget(p1, row, colm, 1, col_size)
        layout.addWidget(self.p1_selector, row+1, colm)
        colm += col_size

        layout.addItem(DD.expander(True, False), row, colm)
        colm += 1

        layout.addWidget(p2, row, colm, 1, col_size)
        layout.addWidget(self.p2_selector, row+1, colm)
        colm += col_size

        layout.addItem(
                DD.expander(True, False),
                row,
                colm
                )
        colm += 1

        arsenal = Arsenal(self.p2_selector, self.player2.weapons, self.player2.defenses)
        col_size = 2
        layout.addWidget(arsenal, row, colm, 1, col_size)
        colm += col_size

        layout.addItem(
                QSpacerItem(30, 50, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed),
                row,
                colm,
                )
        colm += 1

        row += 3
        max_cols = colm
        colm = 0
        fight_btn = QPushButton("FIGHT!")
        fight_btn.setStyleSheet("""
                                border-radius: 25px;
                                min-width: 150px;
                                height: 50px;
                                background-color: green;
                                color: white;
                                font-size: 36px;
                                """)
        #fight_btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(fight_btn, row, max_cols // 2 - 1, 1, 3)

        layout.addItem(
                QSpacerItem(10, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.MinimumExpanding),
                row+1,
                colm
                )

