from random import choice as randChoice
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
)
from dunwoody_disaster.views.arsenal import Arsenal
import dunwoody_disaster as DD
from dunwoody_disaster.CharacterFactory import CharacterFactory
from dunwoody_disaster.views.characterState import CharacterState
from dunwoody_disaster.views.action_selector import ActionSelector
from FightSequence import FightSequence


class FightScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.imageAssets = {
            item: QPixmap(DD.ASSETS[item])
            for item in ["sword", "spear", "shield", "gloves"]
        }

        self.userActionArray = []
        self.compActionArray = []
        punch = QMovie(DD.ASSETS["P1Attack1"])
        kick = QMovie(DD.ASSETS["P1Attack2"])
        defense = QMovie(DD.ASSETS["P1Defense"])
        self.actionArray = ["Punch", "Kick", "Defend"]
        self.damageArray = [10, 20, 0]
        self.player1PicArray = [punch, kick, defense]
        self.fightFlag = False
        self.timer = QTimer()

        self.setStyleSheet("background-color: black;")
        self.mainLayout = QGridLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        row = 0
        colm = 0

        self.mainLayout.addItem(
            QSpacerItem(30, 50, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed),
            row,
            0,
        )
        row += 1
        colm += 1

        self.p1_selector = ActionSelector()
        self.p2_selector = ActionSelector()
        self.P1Arsenal = Arsenal(self.p1_selector)
        self.mainLayout.addWidget(self.P1Arsenal, row, colm, 16, 1)

        colm += 1

        self.mainLayout.addItem(
            QSpacerItem(
                40,
                40,
                QSizePolicy.Policy.MinimumExpanding,
                QSizePolicy.Policy.MinimumExpanding,
            ),
            row,
            colm,
        )
        row += 1
        colm += 1

        ####################
        # This is the middle section of the screen ##############
        self.player1 = CharacterFactory.createTestChar()
        self.player2 = CharacterFactory.createTestChar()
        self.fightSequence = FightSequence(self.player1, self.player2)
        p1 = CharacterState(self.player1)
        p2 = CharacterState(self.player2)

        innerCol = colm
        rightCol = colm + 4
        self.mainLayout.addWidget(p1, row, innerCol, 1, 2)
        self.mainLayout.addWidget(p2, row, rightCol, 1, 2)
        row += 1

        self.mainLayout.addWidget(self.p1_selector, row, innerCol)
        self.mainLayout.addWidget(self.p2_selector, row, rightCol)
        row += 1

        self.mainLayout.addItem(
            DD.spacer(2),
            row,
            innerCol,
        )
        row += 1

        self.mainLayout.addItem(
            DD.spacer(40),
            row,
            innerCol,
        )
        row += 1

        self.fight_Btn = QPushButton("FIGHT!")
        self.fight_Btn.setStyleSheet(
            """border-radius: 25px;
                                        min-width: 150px;
                                        height: 50px;
                                        background-color: green;
                                        color: white;
                                        font-size: 36px;"""
        )
        self.mainLayout.addWidget(self.fight_Btn, row, innerCol + 3)
        self.fight_Btn.clicked.connect(self.SetFightFlag)
        row += 1

        colm = rightCol + 3

        self.mainLayout.addItem(
            QSpacerItem(
                40,
                40,
                QSizePolicy.Policy.MinimumExpanding,
                QSizePolicy.Policy.MinimumExpanding,
            ),
            row,
            rightCol + 3,
        )
        colm += 1

        #############################################################
        self.P2Arsenal = Arsenal(self.p2_selector)
        self.mainLayout.addWidget(self.P2Arsenal, 1, colm, 16, 1)

        colm += 1
        self.mainLayout.addItem(
            QSpacerItem(30, 50, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed),
            row,
            colm,
        )

        self.timer.start(2000)
        self.timer.timeout.connect(self.Fight)

    def SetFightFlag(self):
        self.fightFlag = True

    def AddToQueue(self, action):
        if not len(self.userActionArray) >= 3:
            self.userActionArray.append(action)
            self.compActionArray.append(randChoice(self.actionArray))
            self.player1Lineup_Lbl.setText(
                "Action Lineup: " + str(self.userActionArray)
            )
        if len(self.userActionArray) == 3:
            self.attack1_Btn.setEnabled(False)
            self.attack2_Btn.setEnabled(False)
            self.defend_Btn.setEnabled(False)
            self.fight_Btn.setEnabled(True)

    def Fight(self):
        if self.fightFlag:
            self.fight_Btn.setEnabled(False)

            self.player1, self.player2 = self.fightSequence.Fight(
                self.p1_selector.attack, self.p2_selector.attack,
                self.p1_selector.defense, self.p2_selector.defense
            )
            self.player1.set_health(self.player1.curHealth)
            self.player1.set_magic(self.player1.curMagic)
            self.player1.set_stamina(self.player1.curStamina)

            self.player2.set_health(self.player2.curHealth)
            self.player2.set_magic(self.player2.curMagic)
            self.player2.set_stamina(self.player2.curStamina)

            print("health label text", self.player1.health_lbl.text())
            # self.player1Health_Lbl.setText("Health Meter: " + str(self.userHealthMeter))
            # self.player2Health_Lbl.setText("Health Meter: " + str(self.compHealthMeter))

            # self.compActionArray.pop(0)
            # self.userActionArray.pop(0)
            # if len(self.userActionArray) == 0:
            #     self.fightFlag = False
            #     self.player1Lineup_Lbl.setText(
            #         "Action Lineup: " + str(self.userActionArray)
            #     )
            self.fightFlag = False
            self.fight_Btn.setEnabled(True)

            # self.attack1_Btn.setEnabled(True)
            # self.attack2_Btn.setEnabled(True)
            # self.defend_Btn.setEnabled(True)
