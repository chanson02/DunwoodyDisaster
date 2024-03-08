"""
I'm thinking something like this
https://miro.medium.com/v2/resize:fit:469/1*baExuvv8c4jybSXRoYbj9A.jpeg
"""

from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel
from PySide6.QtGui import QColor
from views.meter import Meter


class FightScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.attack_button = QPushButton("Attack")
        self.defend_button = QPushButton("Defend")

        self.lay_out = self.create_layout()
        self.setLayout(self.lay_out)

    def create_layout(self) -> QGridLayout:
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.player_label = QLabel()
        self.player_meters = {
            "health": Meter(QColor(255, 0, 0), 100),
            "mechanical": Meter(QColor(50, 50, 50), 100),
            "magic": Meter(QColor(200, 0, 200), 100),
        }

        layout.addWidget(self.attack_button, 0, 0)
        layout.addWidget(self.defend_button, 0, 1)
        layout.addLayout(
                self.create_meter_layout(self.player_meters),
                1, 0, 1, 4
                )
        return layout

    def create_meter_layout(self, meters: dict) -> QGridLayout:
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Health"), 0, 0)
        layout.addWidget(QLabel("Mechanical"), 1, 0)
        layout.addWidget(QLabel("Magic"), 2, 0)

        layout.addWidget(meters["health"], 0, 1, 1, 3)
        layout.addWidget(meters["mechanical"], 1, 1, 1, 3)
        layout.addWidget(meters["magic"], 2, 1, 1, 3)

        return layout
