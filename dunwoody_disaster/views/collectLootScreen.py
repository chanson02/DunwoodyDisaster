from typing import Sequence, Callable
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton,
    QHBoxLayout,
    QGroupBox,
    QLayout
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
        self._callback = DD.unimplemented
        self.player = player
        self.items = available
        self.boxes: dict[QCheckBox, Item.Item] = {}

        self.capacity = Meter(QColor("white"), 0)
        self.capacity.setEndColor(QColor("red"))
        self.capacity.setStyleSheet("min-height: 50px;")

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        layout.addLayout(self.capacity_meter())

        # Loot that was dropped
        drops = QGroupBox("Loot Dropped")
        loot = QHBoxLayout()
        drops.setLayout(DD.layout(DD.scroller(loot, True, False)))
        layout.addWidget(drops)

        for item in self.items:
            widget, box = self.create_inventory_slot(item)
            loot.addWidget(widget)
            self.boxes[box] = item

        # Loot that was already in inventory
        inventory_box = QGroupBox("Inventory")
        inventory = QHBoxLayout()
        inventory_box.setLayout(DD.layout(DD.scroller(inventory, True, False)))
        layout.addWidget(inventory_box)

        box = None
        for item in self.player.get_items():
            widget, box = self.create_inventory_slot(item)
            inventory.addWidget(widget)
            self.boxes[box] = item
            box.setChecked(True)
        if box is not None:
            self.select_item(box)

        # Confirm button
        btn = QPushButton("Confirm")
        btn.clicked.connect(self.confirmClicked)
        layout.addWidget(btn)

        return

    def capacity_meter(self) -> QLayout:
        layout = QHBoxLayout()
        lbl = QLabel("Inventory capacity used: ")
        lbl.setFixedWidth(200)
        layout.addWidget(lbl)
        layout.addWidget(self.capacity)
        return layout

    def unset_callback(self):
        raise Exception("Callback never assigned")

    def set_callback(self, callback: Callable):
        """
        Call this function when the loot has been confirmed
        """
        self._callback = callback

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

    def confirmClicked(self):
        self.player.clear_items()
        for box, item in self.boxes.items():
            box.setEnabled(False)
            if box.checkState() is Qt.CheckState.Checked:
                self.player.add_item(item)

        self.deleteLater()
        self._callback()
