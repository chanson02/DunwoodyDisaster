from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)
from dunwoody_disaster.views.arsenal import Arsenal
import dunwoody_disaster as DD
from dunwoody_disaster.views.characterState import CharacterState
from dunwoody_disaster.views.action_selector import ActionSelector
from dunwoody_disaster.views.AnimationWidget import AnimationWidget
# from dunwoody_disaster.animations.idle import IdleAnimation
from dunwoody_disaster.animations.RoomAnimation import RoomAnimation
from dunwoody_disaster.animations.idle import IdleComponent
from dunwoody_disaster.animations.basic_attack import AttackAnimation


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # avoid circular import
    from dunwoody_disaster.FightSequence import FightSequence


class FightScreen(QWidget):
    def __init__(self, controller: "FightSequence", background: str):
        super().__init__()
        self.controller = controller
        self.player1 = self.controller.player
        self.player2 = self.controller.enemy
        self.background = background

        self.p1_selector = ActionSelector(self.player1)
        self.p2_selector = ActionSelector(self.player2)
        self.p2_selector.hide()
        self.p2_selector.selectRandom()

        self._winCallback = DD.unimplemented
        self._loseCallback = DD.unimplemented
        self.fightFlag = False
        self.doneFlag = False
        self.fight_Btn = QPushButton("FIGHT!")

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        row = 0

        layout.addItem(
            QSpacerItem(50, 50, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 0
        )
        row += 1

        arsenal = Arsenal(self.p1_selector, self.player1.weapons, self.player1.defenses)
        layout.addWidget(arsenal, row, 1)

        layout.addItem(
            QSpacerItem(5, 5, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed), row, 2
        )

        layout.addLayout(self.center_layout(), row, 3)

        layout.addItem(
            QSpacerItem(5, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed), row, 4
        )

        arsenal = Arsenal(self.p2_selector, self.player2.weapons, self.player2.defenses)
        layout.addWidget(arsenal, row, 5)

        row += 1

        layout.addItem(
            QSpacerItem(50, 50, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 6
        )

    def center_layout(self) -> QGridLayout:
        p1 = CharacterState(self.player1)
        p2 = CharacterState(self.player2)
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        row = 0
        layout.addItem(
            QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding), row, 0
        )
        row += 1
        # row, column, rowSpan, columnSpan
        layout.addWidget(p1, row, 0)
        layout.addItem(DD.expander(True, False, 150), 0, 1)
        layout.addWidget(p2, row, 2)
        row += 1

        layout.addItem(QSpacerItem(0, 30, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 0)
        row += 1

        self.animation = RoomAnimation(self.background, self.player1.image_path, self.player2.image_path)
        self.animation_Object = AnimationWidget(self.animation)
        layout.addWidget(self.animation_Object, row, 0, 0, 3)
        row += 1

        layout.addItem(QSpacerItem(0, 30, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 0)
        row += 1

        layout.addWidget(self.p1_selector, row, 0)
        layout.addWidget(self.p2_selector, row, 2)
        row += 1

        layout.addItem(QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 0)
        row += 1

        btnLayout = QGridLayout()
        btnLayout.setSpacing(0)
        btnLayout.setContentsMargins(0, 0, 0, 0)
        btnLayout.addItem(DD.expander(True, False, 25), 0, 0)
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
        btnLayout.addWidget(self.fight_Btn, 0, 1)
        btnLayout.addItem(DD.expander(True, False, 25), 0, 2)
        layout.addLayout(btnLayout, row, 0, 1, 3)
        row += 1

        layout.addItem(
            QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding), row, 0
        )

        return layout

    def fightClicked(self):
        if not self.p1_selector.ready():
            print("You must select 2 actions to fight!")
            return

        self.controller.takeTurn(self.p1_selector, self.p2_selector)
