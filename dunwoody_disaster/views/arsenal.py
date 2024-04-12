from typing import Sequence
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGridLayout, QLabel, QWidget, QPushButton, QScrollArea
import dunwoody_disaster as DD
from dunwoody_disaster.views.action_selector import ActionSelector
from dunwoody_disaster import Item


class Arsenal(QWidget):
    """
    The arsenal is made up of two `inventory` widgets which display items
    """

    def __init__(
        self,
        selector: ActionSelector,
        weapons: list[Item.Weapon],
        armors: list[Item.Armor],
    ):
        super().__init__()
        self.selector = selector
        self.setStyleSheet("background-color: black;")
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        weapons_widget = self.create_inventory("Weapons", weapons)
        armor_widget = self.create_inventory("Armor", armors)

        layout.addWidget(weapons_widget, 0, 0)
        layout.addWidget(armor_widget, 0, 1)
        self.setLayout(layout)

    def select_item(self, item: Item.Item):
        if type(item) is Item.Weapon:
            self.selector.set_attack(item)
        elif type(item) is Item.Armor:
            self.selector.set_defense(item)
        return

    def select_item_lambda(self, item: Item.Item):
        return lambda: self.select_item(item)

    def create_inventory(self, label: str, items: Sequence[Item.Item]) -> QWidget:
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        row = 1

        lbl = QLabel(label)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: white; font-size: 24px;")
        layout.addWidget(lbl, row, 1)
        row += 1

        for item in items:
            item_widget = item.widget()
            DD.clickable(item_widget).connect(self.select_item_lambda(item))
            layout.addWidget(item_widget, row, 1)
            row += 1

        widget = QWidget()
        widget.setLayout(layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("min-width: 125px;")
        scroll_area.setWidget(widget)
        return scroll_area
