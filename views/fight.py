from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout
from PySide6.QtGui import QColor
from views.meter import Meter


class FightScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.attack_button = QPushButton('Attack')
        self.defend_button = QPushButton('Defend')

        self.lay_out = self.create_layout()
        self.setLayout(self.lay_out)

    def create_layout(self) -> QGridLayout:
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        color = QColor(0, 255, 0)
        layout.addWidget(self.attack_button, 0, 0)
        layout.addWidget(self.defend_button, 0, 1)
        layout.addWidget(Meter(color), 1, 1)
        return layout
