from typing import Callable
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from dunwoody_disaster.FightSequence import FightSequence
from dunwoody_disaster.views.collectLootScreen import CollectLootScreen
import dunwoody_disaster as DD


class VictoryScreen(QWidget):
    def __init__(self, fight_controller: FightSequence):
        super().__init__()
        self._callback = DD.unimplemented

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        lbl = QLabel(f"Congratulations {fight_controller.player.name}! You Win!")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        pic = QLabel("")
        pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pic.setStyleSheet("min-width: 380px;")
        pic.setPixmap(fight_controller.player.image().scaledToWidth(300))
        layout.addWidget(pic)

        lbl = QLabel("Manage your inventory: ")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        loot_screen = CollectLootScreen(
            fight_controller.player, fight_controller.enemy.get_items()
        )
        loot_screen.set_callback(self.loot_selected_event)
        layout.addWidget(loot_screen)

    def set_callback(self, callback: Callable):
        self._callback = callback

    def loot_selected_event(self):
        self.deleteLater()
        self._callback()
