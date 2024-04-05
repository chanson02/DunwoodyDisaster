from random import choice as randChoice
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QMovie, QColor
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
)
from dunwoody_disaster.views.meter import Meter
from dunwoody_disaster.views.arsenal import Arsenal
from dunwoody_disaster import ASSETS
from dunwoody_disaster.CharacterFactory import Character, CharacterFactory
from dunwoody_disaster.views.characterState import CharacterState


class FightScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.imageAssets = {
            item: QPixmap(ASSETS[item])
            for item in ["sword", "spear", "shield", "gloves"]
        }

        self.userActionArray = []
        self.compActionArray = []
        punch = QMovie(ASSETS["P1Attack1"])
        kick = QMovie(ASSETS["P1Attack2"])
        defense = QMovie(ASSETS["P1Defense"])
        self.actionArray = ["Punch", "Kick", "Defend"]
        self.damageArray = [10, 20, 0]
        self.player1PicArray = [punch, kick, defense]
        self.P1WeaponArray = {"sword": [20, 30, 10], "spear": [30, 10, 20]}
        self.P1DefenseArray = {"shield": [30, 10, 20], "gloves": [10, 10, 10]}
        self.P2WeaponArray = {"sword": [20, 30, 10], "spear": [30, 10, 20]}
        self.P2DefenseArray = {"shield": [30, 10, 20], "gloves": [10, 10, 10]}
        self.P1HealthMeter = 100
        self.P2HealthMeter = 100
        self.P1MagicMeter = 100
        self.P2MagicMeter = 100
        self.P1MechMeter = 100
        self.P2MechMeter = 100
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

        self.P1Arsenal = Arsenal()
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
        player1 = CharacterFactory.createTestChar()
        player2 = CharacterFactory.createTestChar()
        p1 = CharacterState(player1)
        p2 = CharacterState(player2)

        innerCol = colm
        rightCol = colm + 4
        self.mainLayout.addWidget(p1, row, innerCol, 1, 2)
        self.mainLayout.addWidget(p2, row, rightCol, 1, 2)
        row += 1

        self.mainLayout.addWidget(self.action_selector('sword', 'shield'), row, innerCol)
        self.mainLayout.addWidget(self.action_selector('spear', 'gloves'), row, rightCol)
        row += 1

        self.mainLayout.addItem(
            QSpacerItem(0, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed),
            row,
            innerCol,
        )
        row += 1

        self.mainLayout.addItem(
            QSpacerItem(0, 40, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed),
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
        self.P2Arsenal = Arsenal()
        self.mainLayout.addWidget(self.P2Arsenal, 1, colm, 16, 1)

        colm += 1
        self.mainLayout.addItem(
            QSpacerItem(30, 50, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed),
            row,
            colm,
        )

        self.timer.start(2000)
        self.timer.timeout.connect(self.Fight)

    def action_selector(self, attack: str, defence: str) -> QWidget:
        widget = QWidget()
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        attack_pic = QLabel("")
        attack_pic.setPixmap(QPixmap(ASSETS[attack]).scaledToWidth(50))
        defend_pic = QLabel("")
        defend_pic.setPixmap(QPixmap(ASSETS[defence]).scaledToWidth(50))

        layout.addWidget(attack_pic, 0, 0)
        layout.addWidget(defend_pic, 0, 1)
        widget.setLayout(layout)

        return widget

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

            userActionIndex = self.actionArray.index(self.userActionArray[0])
            compActionIndex = self.actionArray.index(self.compActionArray[0])

            p1ActionGif = self.player1PicArray[userActionIndex]
            p2ActionGif = self.player1PicArray[compActionIndex]
            self.player1_Pic.setMovie(p1ActionGif)
            p1ActionGif.start()
            self.player2_Pic.setMovie(p2ActionGif)
            p2ActionGif.start()

            if (
                self.compActionArray[0] == "Defense"
                and self.userActionArray[0] == "Defense"
            ):
                pass
            else:
                if self.userActionArray[0] == "Defense":
                    self.compHealthMeter -= 5
                else:
                    self.compHealthMeter -= self.damageArray[userActionIndex]
                if self.userActionArray[0] == "Defense":
                    self.userHealthMeter -= 5
                else:
                    self.userHealthMeter -= self.damageArray[compActionIndex]
            self.player1Health_Lbl.setText("Health Meter: " + str(self.userHealthMeter))
            self.player2Health_Lbl.setText("Health Meter: " + str(self.compHealthMeter))

            self.compActionArray.pop(0)
            self.userActionArray.pop(0)
            if len(self.userActionArray) == 0:
                self.fightFlag = False
                self.player1Lineup_Lbl.setText(
                    "Action Lineup: " + str(self.userActionArray)
                )
                self.attack1_Btn.setEnabled(True)
                self.attack2_Btn.setEnabled(True)
                self.defend_Btn.setEnabled(True)
