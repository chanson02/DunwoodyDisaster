from typing import Sequence
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton, QHBoxLayout
from dunwoody_disaster.CharacterFactory import Character
from dunwoody_disaster import Item


class CollectLootScreen(QWidget):
    def __init__(self, player: Character, available: Sequence[Item.Item]):
        """
        :param player: The player that is selecting an item.
        :param available: A list of items the player has access to select.
        :return: Creates a UI where a user can select which item(s)? they want to add to their inventory.
        """
        super().__init__()
        self.player = player
        self.items = available

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel('Loot Screen')
        layout.addWidget(lbl)

        items_layout = QHBoxLayout()
        layout.addLayout(items_layout)

        self.boxes = []
        for item in self.items:
            widget, box = self.create_checkbox(item)
            items_layout.addWidget(widget)
            self.boxes.append(box)

        btn = QPushButton('Confirm')
        btn.clicked.connect(self.confirm)
        layout.addWidget(btn)

        self.setLayout(layout)

    def create_checkbox(self, item: Item.Item) -> tuple[QWidget, QCheckBox]:
        layout = QVBoxLayout()
        layout.addWidget(item.widget())
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cb = QCheckBox()
        layout.addWidget(cb)

        widget = QWidget()
        widget.setLayout(layout)
        return widget, cb

    def confirm(self):
        selected = []
        for cb, item in zip(self.boxes, self.items):
            if cb.isChecked():
                selected.append(item)

        print('you selected', selected)
