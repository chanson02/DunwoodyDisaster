from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QHBoxLayout,
)
from dunwoody_disaster.views.arsenal import Arsenal
import dunwoody_disaster as DD
from dunwoody_disaster.views.characterState import CharacterState
from dunwoody_disaster.views.action_selector import ActionSelector

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    # avoid circular import
    from dunwoody_disaster.FightSequence import FightSequence


class FightScreen(QWidget):
    def __init__(self, controller: "FightSequence"):
        super().__init__()
        self.controller = controller
        self.player1 = self.controller.player
        self.player2 = self.controller.enemy

        self.p1_selector = ActionSelector(self.player1)
        self.p2_selector = ActionSelector(self.player2)
        self.p2_selector.selectRandom()

        self._winCallback = DD.unimplemented
        self._loseCallback = DD.unimplemented
        self.fightFlag = False
        self.doneFlag = False
        self.fight_Btn = QPushButton("FIGHT!")

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        layout.addItem(DD.expander(True, False, 0))

        arsenal = Arsenal(self.p1_selector, self.player1.weapons, self.player1.defenses)
        layout.addWidget(arsenal)

        layout.addItem(DD.expander(True, False))
        layout.addLayout(self.center_layout())
        layout.addItem(DD.expander(True, False))

        arsenal = Arsenal(self.p2_selector, self.player2.weapons, self.player2.defenses)
        layout.addWidget(arsenal)
        layout.addItem(DD.expander(True, False, 0))

    def center_layout(self) -> QGridLayout:
        p1 = CharacterState(self.player1)
        p2 = CharacterState(self.player2)
        layout = QGridLayout()
        CHAR_STATE_ROWS = 16

        # row, column, rowSpan, columnSpan
        layout.addWidget(p1, 0, 0, CHAR_STATE_ROWS, 4)
        layout.addWidget(self.p1_selector, CHAR_STATE_ROWS + 1, 0, 1, 4)

        layout.addItem(DD.expander(True, False, 25), 0, 4, CHAR_STATE_ROWS + 1, 1)

        layout.addWidget(p2, 0, 5, CHAR_STATE_ROWS, 4)
        layout.addWidget(self.p2_selector, CHAR_STATE_ROWS + 1, 5, 1, 4)

        self.fight_Btn.setStyleSheet(
            """
                                border-radius: 25px;
                                min-width: 150px;
                                height: 50px;
                                background-color: green;
                                color: white;
                                font-size: 36px;
                                """
        )
        self.fight_Btn.clicked.connect(self.fightClicked)
        layout.addWidget(
            self.fight_Btn, CHAR_STATE_ROWS + 2, 2, 1, 5, Qt.AlignmentFlag.AlignCenter
        )

        return layout

    def fightClicked(self):
        if not self.p1_selector.ready():
            print("You must select 2 actions to fight!")
            return

        self.controller.takeTurn(self.p1_selector, self.p2_selector)
