from PySide6.QtCore import QTimer, Qt

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLayout
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
        self.setStyleSheet('border: 1px solid green;')

        self.init_ui()

    def init_ui(self):
        p1 = CharacterState(self.player1)
        p2 = CharacterState(self.player2)

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        layout.addItem(DD.expander(True, False, 0))

        arsenal = Arsenal(self.p1_selector, self.player1.weapons, self.player1.defenses)
        layout.addWidget(arsenal)

        layout.addItem(DD.expander(True, False))
        # layout.addLayout(self.center_layout(), stretch=1)
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

        fight_btn = QPushButton("FIGHT!")
        fight_btn.setStyleSheet("""
                                border-radius: 25px;
                                min-width: 150px;
                                height: 50px;
                                background-color: green;
                                color: white;
                                font-size: 36px;
                                """)
        layout.addWidget(fight_btn, CHAR_STATE_ROWS + 2, 2, 1, 5, Qt.AlignmentFlag.AlignCenter)

        return layout


    # def SetFightFlag(self):
    #     if self.CanFight(self.p1_selector) and self.CanFight(self.p2_selector):
    #         self.fightFlag = True
    #     else:
    #         print("You must select 2 actions to fight!")
    #
    # def CanFight(self, actionSelector: ActionSelector):
    #     return (actionSelector.attack and actionSelector.defense) is not None
    #
    # def Fight(self):
    #     if self.fightFlag:
    #         self.fight_Btn.setEnabled(False)
    #         self.player1, self.player2 = self.fightSequence.Fight(
    #             self.p1_selector,
    #             self.p2_selector,
    #         )
    #         self.player1.set_health(self.player1.curHealth)
    #         self.player1.set_magic(self.player1.curMagic)
    #         self.player1.set_stamina(self.player1.curStamina)
    #
    #         self.player2.set_health(self.player2.curHealth)
    #         self.player2.set_magic(self.player2.curMagic)
    #         self.player2.set_stamina(self.player2.curStamina)
    #         if self.player1.curHealth <= 0 or self.player2.curHealth <= 0:
    #             self.doneFlag = True
    #             self.timer.stop()
    #             if self.player1.curHealth == 0:
    #                 print("Player 2 Wins!")
    #             else:
    #                 self.onWin()
    #         self.fightFlag = False
    #         self.fight_Btn.setEnabled(True)
    #         self.fightFlag = False
    #         self.fight_Btn.setEnabled(True)
    #
    # def onWin(self):
    #     vc = VictoryScreen(self.fightSequence)
    #     self.stacked_layout.addWidget(vc)
    #     self.stacked_layout.setCurrentWidget(vc)
