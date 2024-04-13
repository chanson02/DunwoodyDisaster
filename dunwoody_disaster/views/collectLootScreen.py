from typing import Sequence
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton,
    QHBoxLayout,
    QScrollArea
)
from dunwoody_disaster.CharacterFactory import Character
from dunwoody_disaster import Item
import dunwoody_disaster as DD
from dunwoody_disaster.views.meter import Meter


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

        self.capacity = Meter(QColor("red"), 0)
        layout.addWidget(self.capacity)

        new_items = QHBoxLayout()
        layout.addLayout(new_items)

        self.boxes: dict[QCheckBox, Item.Item] = {}
        for item in self.items:
            widget, box = self.create_inventory_slot(item)
            new_items.addWidget(widget)
            self.boxes[box] = item

        scroll_area = QScrollArea()
        old_items = QHBoxLayout()
        item_container = QWidget()
        item_container.setLayout(old_items)
        scroll_area.setWidget(item_container)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        box = None
        for item in self.player.get_items():
            widget, box = self.create_inventory_slot(item)
            old_items.addWidget(widget)
            old_items.addSpacing(10)
            self.boxes[box] = item
            box.setChecked(True)
        if box is not None:
            self.select_item(box)

        btn = QPushButton("Confirm")
        btn.clicked.connect(self.confirm)
        layout.addWidget(btn)

        self.setLayout(layout)
        return

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
            if not cb.isEnabled():
                return

            cb.setChecked(not cb.isChecked())
            callback()
            return

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
            else:
                unselected_boxes.append(checkbox)

        total_inventory = sum(item.serialize()["stamina"] for item in selected_items)
        remaining = self.player.inventory_capacity - total_inventory
        self.capacity.setPercentage(
            (total_inventory / self.player.inventory_capacity) * 100
        )

        for box in unselected_boxes:
            if self.boxes[box].serialize()["stamina"] > remaining:
                box.setEnabled(False)
            else:
                box.setEnabled(True)

        return

    def confirm(self):
        for cb, item in zip(self.boxes, self.items):
            cb.setEnabled(False)
            if cb.isChecked():
                self.player.add_item(item)

        self.deleteLater()
