from typing import Sequence
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

        checkboxes = QVBoxLayout()
        self.boxes = []
        for item in self.items:
            items_layout.addWidget(item.widget())
            box = QCheckBox(item.name)
            self.boxes.append(box)
            checkboxes.addWidget(box)

        layout.addLayout(checkboxes)

        btn = QPushButton('Confirm')
        btn.clicked.connect(self.confirm)
        layout.addWidget(btn)

        self.setLayout(layout)

    def confirm(self):
        selected = []
        for cb, item in zip(self.boxes, self.items):
            if cb.isChecked():
                selected.append(item)

        print('you selected', selected)
