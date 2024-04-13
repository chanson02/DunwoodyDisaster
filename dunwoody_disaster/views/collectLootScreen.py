from typing import Sequence
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton,
    QHBoxLayout,
)
from dunwoody_disaster.CharacterFactory import Character
from dunwoody_disaster import Item
import dunwoody_disaster as DD

"""
what i'm working on:
I just made it so each character has a .inventory_capacity
I want to check if they can add an item to their inventory based on how much stamina it costs

the problem is that each time they toggle on or off an item, I want to enable/disable a checkbox
"""

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

        lbl = QLabel("Loot Screen")
        layout.addWidget(lbl)

        items_layout = QHBoxLayout()
        layout.addLayout(items_layout)

        self.boxes: dict[QCheckBox, Item.Item] = {}
        for item in self.items:
            widget, box = self.create_inventory_slot(item)
            items_layout.addWidget(widget)
            self.boxes[box] = item

        btn = QPushButton("Confirm")
        btn.clicked.connect(self.confirm)
        layout.addWidget(btn)

        self.setLayout(layout)

    def create_inventory_slot(self, item: Item.Item) -> tuple[QWidget, QCheckBox]:
        layout = QVBoxLayout()
        layout.addWidget(item.widget())

        cb = QCheckBox()
        cbl = QVBoxLayout()
        cbl.addWidget(cb)
        cbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(cbl)

        def callback():
            self.select_item(cb)

        def widget_click():
            cb.setChecked(not cb.isChecked())
            callback()

        widget = QWidget()
        widget.setLayout(layout)
        DD.clickable(widget).connect(widget_click)
        cb.clicked.connect(callback)
        return widget, cb

    def select_item(self, selected: QCheckBox):
        if not selected.isEnabled():
            return

        selected_items = []
        unselected_boxes = []
        for checkbox, item in self.boxes.items():
            if checkbox.checkState() is Qt.CheckState.Checked:
                checkbox.setEnabled(True)
                selected_items.append(item)

        print(selected_items)

        return

    """
    def create_checkbox(self, item: Item.Item) -> tuple[QWidget, QCheckBox]:
        layout = QVBoxLayout()

        cb_layout = QVBoxLayout()
        cb = QCheckBox()
        cb_layout.addWidget(cb)

        def toggle_box():
            if cb.isEnabled():
                cb.setChecked(not cb.isChecked())

        item_widget = item.widget()
        DD.clickable(item_widget).connect(toggle_box)

        layout.addWidget(item_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cb_layout.addWidget(cb)
        cb_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(cb_layout)

        widget = QWidget()
        widget.setLayout(layout)
        return widget, cb
    """

    def confirm(self):
        for cb, item in zip(self.boxes, self.items):
            cb.setEnabled(False)
            if cb.isChecked():
                self.player.add_item(item)

        self.deleteLater()
