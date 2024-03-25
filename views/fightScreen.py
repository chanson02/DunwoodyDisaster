import sys
from random import choice as randChoice
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QMovie, QColor
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QWidget,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
)
from meter import Meter

# from arsenal import Arsenal


class FightScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.imageDir = "C:/classGame/"

        self.userActionArray = []
        self.compActionArray = []
        self.imgDict = {
            "sword": QPixmap(self.imageDir + "sword.jpg"),
            "spear": QPixmap(self.imageDir + "spear.jpg"),
            "shield": QPixmap(self.imageDir + "shield.jpg"),
            "gloves": QPixmap(self.imageDir + "gloves.jpg"),
        }
        punch = QMovie(self.imageDir + "P1Attack1.gif")
        kick = QMovie(self.imageDir + "P1Attack2.gif")
        defense = QMovie(self.imageDir + "P1Defense.gif")
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

        # self = QWidget()
        self.setStyleSheet("background-color: black;")
        self.mainLayout = QGridLayout(spacing=0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        row = 0
        colm = 0
        self.mainLayout.addItem(
            QSpacerItem(30, 50, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 0
        )
        row += 1
        colm += 1

        #############################################################
        self.P1WeaponLayout = QGridLayout(spacing=0)
        self.P1WeaponLayout.setContentsMargins(0, 0, 0, 0)
        self.P1WeaponWgt = QWidget()
        self.P1WeaponWgt.setStyleSheet(
            "border-left: 1px solid green; min-width: 125px;"
        )
        self.P1WeaponWgt.setLayout(self.P1WeaponLayout)

        arsRow = 0

        self.P1Weapon_Lbl = QLabel("Weapons")
        self.P1Weapon_Lbl.setAlignment(Qt.AlignCenter)
        self.P1Weapon_Lbl.setStyleSheet("color: white; font-size: 24px;")
        self.P1WeaponLayout.addWidget(self.P1Weapon_Lbl, arsRow, 1)
        arsRow += 1

        self.P1WeaponLayout.addItem(
            QSpacerItem(0, 30, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
        )
        arsRow += 1

        for key in self.P1WeaponArray:

            self.P1_weapon1_Lbl1 = QLabel(key)
            self.P1_weapon1_Lbl1.setAlignment(Qt.AlignCenter)
            self.P1_weapon1_Lbl1.setStyleSheet("color: white;")
            self.P1WeaponLayout.addWidget(self.P1_weapon1_Lbl1, arsRow, 1)
            arsRow += 1

            self.P1WeaponLayout.addItem(
                QSpacerItem(0, 10, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
            )
            arsRow += 1

            self.P1_weapon1_Lbl2 = QLabel("")
            self.P1_weapon1_Lbl2.setAlignment(Qt.AlignCenter)
            self.P1_weapon1_Lbl2.setPixmap(self.imgDict[key].scaledToWidth(80))
            self.P1WeaponLayout.addWidget(self.P1_weapon1_Lbl2, arsRow, 1)
            arsRow += 1

            self.P1WeaponLayout.addItem(
                QSpacerItem(0, 10, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
            )
            arsRow += 1

            self.P1_weapon1_Lbl3 = QLabel(
                "H: "
                + str(self.P1WeaponArray[key][0])
                + "\nM: "
                + str(self.P1WeaponArray[key][1])
                + "\nMech: "
                + str(self.P1WeaponArray[key][2])
            )
            self.P1_weapon1_Lbl3.setAlignment(Qt.AlignCenter)
            self.P1_weapon1_Lbl3.setStyleSheet("color: white;")
            self.P1WeaponLayout.addWidget(self.P1_weapon1_Lbl3, arsRow, 1)
            arsRow += 1

            self.P1WeaponLayout.addItem(
                QSpacerItem(0, 40, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
            )
            arsRow += 1
        self.P1WeaponLayout.addItem(
            QSpacerItem(0, 40, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding),
            arsRow,
            1,
        )

        #############################################################

        # self.P1weaponArsenal = Arsenal('Weapon', self.P1WeaponArray)
        self.mainLayout.addWidget(self.P1WeaponWgt, row, colm, 16, 1)
        colm += 1

        #############################################################

        self.P1defenseLayout = QGridLayout(spacing=0)
        self.P1defenseLayout.setContentsMargins(0, 0, 0, 0)
        self.P1defenseWgt = QWidget()
        self.P1defenseWgt.setStyleSheet(
            """border-left: 1px solid green;
            border-right: 1px solid green;
            min-width: 125px;"""
        )
        self.P1defenseWgt.setLayout(self.P1defenseLayout)

        arsRow = 0

        self.P1defense_Lbl = QLabel("Armor")
        self.P1defense_Lbl.setAlignment(Qt.AlignCenter)
        self.P1defense_Lbl.setStyleSheet("color: white; font-size: 24px;")
        self.P1defenseLayout.addWidget(self.P1defense_Lbl, arsRow, 1)
        arsRow += 1

        self.P1defenseLayout.addItem(
            QSpacerItem(0, 30, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
        )
        arsRow += 1

        for key in self.P1DefenseArray:

            self.P1_armor1_Lbl1 = QLabel(key)
            self.P1_armor1_Lbl1.setAlignment(Qt.AlignCenter)
            self.P1_armor1_Lbl1.setStyleSheet("color: white;")
            self.P1defenseLayout.addWidget(self.P1_armor1_Lbl1, arsRow, 1)
            arsRow += 1

            self.P1defenseLayout.addItem(
                QSpacerItem(0, 10, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
            )
            arsRow += 1

            self.P1_armor1_Lbl2 = QLabel("")
            self.P1_armor1_Lbl2.setAlignment(Qt.AlignCenter)
            self.P1_armor1_Lbl2.setPixmap(self.imgDict[key].scaledToWidth(80))
            self.P1defenseLayout.addWidget(self.P1_armor1_Lbl2, arsRow, 1)
            arsRow += 1

            self.P1defenseLayout.addItem(
                QSpacerItem(0, 10, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
            )
            arsRow += 1

            self.P1_armor1_Lbl3 = QLabel(
                "H: "
                + str(self.P1DefenseArray[key][0])
                + "\nM: "
                + str(self.P1DefenseArray[key][1])
                + "\nMech: "
                + str(self.P1DefenseArray[key][2])
            )
            self.P1_armor1_Lbl3.setAlignment(Qt.AlignCenter)
            self.P1_armor1_Lbl3.setStyleSheet("color: white;")
            self.P1defenseLayout.addWidget(self.P1_armor1_Lbl3, arsRow, 1)
            arsRow += 1

            self.P1defenseLayout.addItem(
                QSpacerItem(0, 40, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
            )
            arsRow += 1
        self.P1defenseLayout.addItem(
            QSpacerItem(0, 40, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding),
            arsRow,
            1,
        )

        #############################################################

        # self.P1defenseArsenal = Arsenal('Defense', self.P1DefenseArray)
        self.mainLayout.addWidget(self.P1defenseWgt, row, colm, 16, 1)
        colm += 1

        self.mainLayout.addItem(
            QSpacerItem(
                40, 40, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
            ),
            row,
            colm,
        )
        row += 1
        colm += 1

        innerCol = colm
        rightCol = colm + 4
        self.player1_Lbl = QLabel("Player 1")
        self.player1_Lbl.setStyleSheet("color: white; font-size: 30px;")
        self.mainLayout.addWidget(self.player1_Lbl, row, innerCol, 1, 3)

        self.player2_Lbl = QLabel("Player 2")
        self.player2_Lbl.setStyleSheet("color: white; font-size: 30px;")
        self.mainLayout.addWidget(self.player2_Lbl, row, rightCol, 1, 3)
        row += 1

        self.mainLayout.addItem(
            QSpacerItem(0, 30, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 1
        )
        row += 1

        self.player1_meters = {
            "health": Meter(QColor(255, 0, 0), 100),
            "mechanical": Meter(QColor(50, 50, 50), 100),
            "magic": Meter(QColor(200, 0, 200), 100),
        }

        self.player2_meters = {
            "health": Meter(QColor(255, 0, 0), 100),
            "mechanical": Meter(QColor(50, 50, 50), 100),
            "magic": Meter(QColor(200, 0, 200), 100),
        }

        self.player1Health_Lbl = QLabel("Health Meter: " + str(self.P1HealthMeter))
        self.player1Health_Lbl.setStyleSheet("color: white;")
        self.mainLayout.addWidget(self.player1Health_Lbl, row, innerCol)

        self.player1_healthMeter = self.player1_meters["health"]
        self.mainLayout.addWidget(self.player1_healthMeter, row, innerCol + 1, 1, 2)

        self.player2Health_Lbl = QLabel("Health Meter: " + str(self.P2HealthMeter))
        self.player2Health_Lbl.setStyleSheet("color: white;")
        self.mainLayout.addWidget(self.player2Health_Lbl, row, rightCol)

        self.player2_healthMeter = self.player2_meters["health"]
        self.mainLayout.addWidget(self.player2_healthMeter, row, rightCol + 1, 1, 2)
        row += 1

        self.mainLayout.addItem(
            QSpacerItem(0, 10, QSizePolicy.Fixed, QSizePolicy.Fixed), row, innerCol
        )
        row += 1

        self.player1Magic_Lbl = QLabel("Magic Meter: " + str(self.P1MagicMeter))
        self.player1Magic_Lbl.setStyleSheet("color: white;")
        self.mainLayout.addWidget(self.player1Magic_Lbl, row, innerCol)

        self.player1_magicMeter = self.player1_meters["magic"]
        self.mainLayout.addWidget(self.player1_magicMeter, row, innerCol + 1, 1, 2)

        self.player2Magic_Lbl = QLabel("Magic Meter: " + str(self.P2MagicMeter))
        self.player2Magic_Lbl.setStyleSheet("color: white;")
        self.mainLayout.addWidget(self.player2Magic_Lbl, row, rightCol)

        self.player2_magicMeter = self.player2_meters["magic"]
        self.mainLayout.addWidget(self.player2_magicMeter, row, rightCol + 1, 1, 2)
        row += 1

        self.mainLayout.addItem(
            QSpacerItem(0, 10, QSizePolicy.Fixed, QSizePolicy.Fixed), row, innerCol
        )
        row += 1

        self.player1Mech_Lbl = QLabel("Mechanical Meter: " + str(self.P1MechMeter))
        self.player1Mech_Lbl.setStyleSheet("color: white;")
        self.mainLayout.addWidget(self.player1Mech_Lbl, row, innerCol)

        self.player1_mechMeter = self.player1_meters["mechanical"]
        self.mainLayout.addWidget(self.player1_mechMeter, row, innerCol + 1, 1, 2)

        self.player2Mech_Lbl = QLabel("Mechanical Meter: " + str(self.P2MechMeter))
        self.player2Mech_Lbl.setStyleSheet("color: white;")
        self.mainLayout.addWidget(self.player2Mech_Lbl, row, rightCol)

        self.player2_mechMeter = self.player2_meters["mechanical"]
        self.mainLayout.addWidget(self.player2_mechMeter, row, rightCol + 1, 1, 2)
        row += 1

        self.mainLayout.addItem(
            QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Fixed), row, innerCol
        )
        row += 1

        self.player1_Pic = QLabel("")
        self.player1_Pic.setAlignment(Qt.AlignCenter)
        self.player1_Pic.setStyleSheet("min-width: 380px;")
        self.player1_Pic.setPixmap(QPixmap(self.imageDir + "ready.jpg"))
        self.mainLayout.addWidget(self.player1_Pic, row, innerCol, 1, 3)

        self.mainLayout.addItem(
            QSpacerItem(30, 0, QSizePolicy.Fixed, QSizePolicy.Fixed), row, innerCol + 3
        )

        self.player2_Pic = QLabel("")
        self.player2_Pic.setAlignment(Qt.AlignCenter)
        self.player2_Pic.setStyleSheet("min-width: 380px;")
        self.player2_Pic.setPixmap(QPixmap(self.imageDir + "ready.jpg"))
        self.mainLayout.addWidget(self.player2_Pic, row, rightCol, 1, 3)
        row += 1

        self.mainLayout.addItem(
            QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Fixed), row, innerCol
        )
        row += 1

        self.P1Weapon_Pic = QLabel("")
        self.P1Weapon_Pic.setPixmap(
            QPixmap(self.imageDir + "sword.jpg").scaledToWidth(50)
        )
        self.mainLayout.addWidget(self.P1Weapon_Pic, row, innerCol)

        self.P1Defense_Pic = QLabel("")
        self.P1Defense_Pic.setPixmap(
            QPixmap(self.imageDir + "shield.jpg").scaledToWidth(50)
        )
        self.mainLayout.addWidget(self.P1Defense_Pic, row, innerCol + 1)

        self.P2Weapon_Pic = QLabel("")
        self.P2Weapon_Pic.setPixmap(
            QPixmap(self.imageDir + "spear.jpg").scaledToWidth(50)
        )
        self.mainLayout.addWidget(self.P2Weapon_Pic, row, rightCol)

        self.P2Defense_Pic = QLabel("")
        self.P2Defense_Pic.setPixmap(
            QPixmap(self.imageDir + "gloves.jpg").scaledToWidth(50)
        )
        self.mainLayout.addWidget(self.P2Defense_Pic, row, rightCol + 1)

        # self.defend_Btn = QPushButton("Defend")
        # self.defend_Btn.setStyleSheet('''border-radius: 15px;
        #                               min-width: 100px;
        #                               height: 32px;
        #                               background-color: blue;''')
        # self.mainLayout.addWidget(self.defend_Btn, row, innerCol+2)
        # self.defend_Btn.clicked.connect(lambda: self.AddToQueue('Defend'))
        row += 1

        self.mainLayout.addItem(
            QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Fixed), row, innerCol
        )
        row += 1

        # self.player1Lineup_Lbl = QLabel("Action Lineup: " +
        #                                   str(self.userActionArray))
        # self.player1Lineup_Lbl.setStyleSheet("color: white;")
        # self.mainLayout.addWidget(self.player1Lineup_Lbl,
        #                            row, innerCol, 1, 3)

        # self.player2Lineup_Lbl = QLabel("Action Lineup: " +
        #                                   str(self.compActionArray))
        # self.player2Lineup_Lbl.setStyleSheet("color: white;")
        # self.mainLayout.addWidget(self.player2Lineup_Lbl,
        #                           row, rightCol, 1, 3)
        row += 1

        self.mainLayout.addItem(
            QSpacerItem(0, 40, QSizePolicy.Fixed, QSizePolicy.Fixed), row, innerCol
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
                40, 40, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
            ),
            row,
            rightCol + 3,
        )
        colm += 1

        #############################################################
        self.P2WeaponLayout = QGridLayout(spacing=0)
        self.P2WeaponLayout.setContentsMargins(0, 0, 0, 0)
        self.P2weaponArsenal = QWidget()
        self.P2weaponArsenal.setStyleSheet(
            "border-left: 1px solid green; min-width: 125px;"
        )
        self.P2weaponArsenal.setLayout(self.P2WeaponLayout)

        arsRow = 0

        self.P2Weapon_Lbl = QLabel("Weapons")
        self.P2Weapon_Lbl.setAlignment(Qt.AlignCenter)
        self.P2Weapon_Lbl.setStyleSheet("color: white; font-size: 24px;")
        self.P2WeaponLayout.addWidget(self.P2Weapon_Lbl, arsRow, 1)
        arsRow += 1

        self.P2WeaponLayout.addItem(
            QSpacerItem(0, 30, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
        )
        arsRow += 1

        for key in self.P1WeaponArray:

            self.P2_weapon1_Lbl1 = QLabel(key)
            self.P2_weapon1_Lbl1.setAlignment(Qt.AlignCenter)
            self.P2_weapon1_Lbl1.setStyleSheet("color: white;")
            self.P2WeaponLayout.addWidget(self.P2_weapon1_Lbl1, arsRow, 1)
            arsRow += 1

            self.P2WeaponLayout.addItem(
                QSpacerItem(0, 10, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
            )
            arsRow += 1

            self.P2_weapon1_Lbl2 = QLabel("")
            self.P2_weapon1_Lbl2.setAlignment(Qt.AlignCenter)
            self.P2_weapon1_Lbl2.setPixmap(self.imgDict[key].scaledToWidth(80))
            self.P2WeaponLayout.addWidget(self.P2_weapon1_Lbl2, arsRow, 1)
            arsRow += 1

            self.P2WeaponLayout.addItem(
                QSpacerItem(0, 10, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
            )
            arsRow += 1

            self.P2_weapon1_Lbl3 = QLabel(
                "H: "
                + str(self.P2WeaponArray[key][0])
                + "\nM: "
                + str(self.P2WeaponArray[key][1])
                + "\nMech: "
                + str(self.P2WeaponArray[key][2])
            )
            self.P2_weapon1_Lbl3.setAlignment(Qt.AlignCenter)
            self.P2_weapon1_Lbl3.setStyleSheet("color: white;")
            self.P2WeaponLayout.addWidget(self.P2_weapon1_Lbl3, arsRow, 1)
            arsRow += 1

            self.P2WeaponLayout.addItem(
                QSpacerItem(0, 40, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
            )
            arsRow += 1
        self.P2WeaponLayout.addItem(
            QSpacerItem(0, 40, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding),
            arsRow,
            1,
        )

        #################################################################

        # self.P2weaponArsenal = Arsenal('Weapon', self.P1WeaponArray)
        self.mainLayout.addWidget(self.P2weaponArsenal, 1, colm, 16, 1)
        colm += 1

        #################################################################

        self.P2defenseLayout = QGridLayout(spacing=0)
        self.P2defenseLayout.setContentsMargins(0, 0, 0, 0)
        self.P2defenseArsenal = QWidget()
        self.P2defenseArsenal.setStyleSheet(
            """border-left: 1px solid green;
                                            border-right: 1px solid green;
                                            min-width: 125px;"""
        )
        self.P2defenseArsenal.setLayout(self.P2defenseLayout)

        arsRow = 0

        self.P2defense_Lbl = QLabel("Armor")
        self.P2defense_Lbl.setAlignment(Qt.AlignCenter)
        self.P2defense_Lbl.setStyleSheet("color: white; font-size: 24px;")
        self.P2defenseLayout.addWidget(self.P2defense_Lbl, arsRow, 1)
        arsRow += 1

        self.P2defenseLayout.addItem(
            QSpacerItem(0, 30, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
        )
        arsRow += 1

        for key in self.P1DefenseArray:

            self.P2_armor1_Lbl1 = QLabel(key)
            self.P2_armor1_Lbl1.setAlignment(Qt.AlignCenter)
            self.P2_armor1_Lbl1.setStyleSheet("color: white;")
            self.P2defenseLayout.addWidget(self.P2_armor1_Lbl1, arsRow, 1)
            arsRow += 1

            self.P2defenseLayout.addItem(
                QSpacerItem(0, 10, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
            )
            arsRow += 1

            self.P2_armor1_Lbl2 = QLabel("")
            self.P2_armor1_Lbl2.setAlignment(Qt.AlignCenter)
            self.P2_armor1_Lbl2.setPixmap(self.imgDict[key].scaledToWidth(80))
            self.P2defenseLayout.addWidget(self.P2_armor1_Lbl2, arsRow, 1)
            arsRow += 1

            self.P2defenseLayout.addItem(
                QSpacerItem(0, 10, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
            )
            arsRow += 1

            self.P2_armor1_Lbl3 = QLabel(
                "H: "
                + str(self.P2DefenseArray[key][0])
                + "\nM: "
                + str(self.P2DefenseArray[key][1])
                + "\nMech: "
                + str(self.P2DefenseArray[key][2])
            )
            self.P2_armor1_Lbl3.setAlignment(Qt.AlignCenter)
            self.P2_armor1_Lbl3.setStyleSheet("color: white;")
            self.P2defenseLayout.addWidget(self.P2_armor1_Lbl3, arsRow, 1)
            arsRow += 1

            self.P2defenseLayout.addItem(
                QSpacerItem(0, 40, QSizePolicy.Fixed, QSizePolicy.Fixed), arsRow, 1
            )
            arsRow += 1
        self.P2defenseLayout.addItem(
            QSpacerItem(0, 40, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding),
            arsRow,
            1,
        )

        ##################################################################

        # self.P2defenseArsenal = Arsenal('Defense', self.P1DefenseArray)
        self.mainLayout.addWidget(self.P2defenseArsenal, 1, colm, 16, 1)
        colm += 1

        self.mainLayout.addItem(
            QSpacerItem(30, 50, QSizePolicy.Fixed, QSizePolicy.Fixed), row, colm
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
