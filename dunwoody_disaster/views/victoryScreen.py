from typing import Callable
from PySide6.QtCore import Qt
from dunwoody_disaster.FightSequence import FightSequence
import dunwoody_disaster as DD
from dunwoody_disaster import Item
from dunwoody_disaster.views.meter import Meter
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QCheckBox,
    QPushButton,
    QHBoxLayout,
    QGroupBox,
    QSpacerItem,
    QSizePolicy,
    QVBoxLayout,
)


class VictoryScreen(QWidget):
    def __init__(self, fight_controller: FightSequence):
        super().__init__()
        self._callback = DD.unimplemented
        self.player = fight_controller.player
        self.items = fight_controller.enemy.get_items()
        self.boxes: dict[QCheckBox, Item.Item] = {}

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        row = 0
        layout.addItem(
            QSpacerItem(
                5, 5, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
            ),
            row,
            0,
        )
        row += 1

        lbl = QLabel(
            f"Congratulations {fight_controller.player.name}!\nYou defeated {fight_controller.enemy.name}!\nCollect your loot."
        )
        lbl.setStyleSheet("font-size: 20px; font-weight: 600; color: red;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl, row, 1)

        layout.addItem(
            QSpacerItem(250, 0, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 2
        )

        lbl = QLabel("LOOT!")
        lbl.setStyleSheet("font-size: 18px; color: white;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl, row, 3)
        row += 1

        layout.addItem(QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 1)
        row += 1

        pic = QLabel("")
        pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pic.setStyleSheet("min-width: 300px;")
        pic.setPixmap(fight_controller.player.image().scaledToWidth(300))
        layout.addWidget(pic, row, 1)

        drops = QGroupBox("Loot Dropped")
        drops.setStyleSheet("border: 1px solid red; color: white;")
        loot = QHBoxLayout()
        scroller = DD.scroller(loot, True, False)
        scroller.setStyleSheet("border: none;")
        drops.setLayout(DD.layout(scroller))
        layout.addWidget(drops, row, 3)

        for item in self.items:
            widget, box = self.create_inventory_slot(item)
            loot.addWidget(widget)
            self.boxes[box] = item

        row += 1

        # layout.addItem(QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 1)
        # row += 1

        # lbl = QLabel("Manage your inventory: ")
        # lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(lbl, row, 1)
        # row += 1

        layout.addItem(QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 1)
        row += 1

        cap_Layout = QGridLayout()
        cap_Layout.setSpacing(0)
        cap_Layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel("Inventory capacity: ")
        lbl.setStyleSheet("font-size: 16px;")
        cap_Layout.addWidget(lbl, 0, 0)

        self.capacity = Meter(QColor("white"), 0)
        self.capacity.animated = False
        self.capacity.setEndColor(QColor("red"))
        self.capacity.setMinimumHeight(25)
        cap_Layout.addWidget(self.capacity, 0, 1)
        row += 1

        layout.addLayout(cap_Layout, row, 1)
        row += 1

        layout.addItem(QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 1)
        row += 1

        inventory_box = QGroupBox("Inventory")
        inventory_box.setStyleSheet("border: 1px solid red; color: white;")
        inventory = QHBoxLayout()
        scroller = DD.scroller(inventory, True, False)
        scroller.setStyleSheet("border: none;")
        inventory_box.setLayout(DD.layout(scroller))
        layout.addWidget(inventory_box, row, 1)
        row += 1

        box = None
        for item in self.player.get_items():
            widget, box = self.create_inventory_slot(item)
            inventory.addWidget(widget)
            self.boxes[box] = item
            box.setChecked(True)
        if box is not None:
            self.select_item(box)

        layout.addItem(
            QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding), row, 1
        )
        row += 1

        btn = QPushButton("Continue")
        btn.setStyleSheet("font-size: 14px; font-weight: 600; background-color: gray;")
        btn.clicked.connect(self.confirmClicked)
        layout.addWidget(btn, row, 2)
        row += 1

        layout.addItem(
            QSpacerItem(
                5, 5, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
            ),
            row,
            4,
        )

    def onClose(self, callback: Callable):
        self._callback = callback

    def loot_selected_event(self):
        self.deleteLater()
        self._callback()

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
        self.loot_selected_event()
