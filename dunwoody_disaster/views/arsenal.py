from typing import Sequence
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QWidget,
    QPushButton,
)
import dunwoody_disaster as DD
from dunwoody_disaster.views.action_selector import ActionSelector
from dunwoody_disaster import Item


class Arsenal(QWidget):
    """
    The arsenal is made up of two `inventory` widgets which display items
    """

    def __init__(self, selector: ActionSelector):
        super().__init__()
        self.selector = selector
        self.imageAssets = {
            item: QPixmap(f"./assets/{item}.jpg")
            for item in ["sword", "spear", "shield", "gloves"]
        }

        self.setStyleSheet("background-color: black;")
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        weapons_widget = self.create_inventory("Weapons", Item.weapons)
        armor_widget = self.create_inventory("Armor", Item.armors)

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

    def create_inventory(self, label: str, items: Sequence[Item.Weapon | Item.Armor]) -> QWidget:
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        row = 0

        lbl = QLabel(label)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: white; font-size: 24px;")
        layout.addWidget(lbl, row, 1)
        row += 1
        layout.addItem(DD.spacer(10), row, 1)
        row += 1

        for item in items:
            name = QLabel(item.name)
            name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name.setStyleSheet("color: white;")
            layout.addWidget(name, row, 1)
            row += 1

            layout.addItem(DD.spacer(10), row, 1)
            row += 1

            image = QPixmap(item.image).scaledToWidth(80)
            btn = QPushButton()
            btn.setIcon(image)
            btn.setIconSize(image.size())
            btn.clicked.connect(self.select_item_lambda(item))
            layout.addWidget(btn, row, 1)
            row += 1

            layout.addItem(DD.spacer(10), row, 1)
            row += 1

            # TODO: Clean up these properties
            properties = QLabel(str(item))
            properties.setAlignment(Qt.AlignmentFlag.AlignCenter)
            properties.setStyleSheet("color: white;")
            layout.addWidget(properties, row, 1)
            row += 1

            layout.addItem(DD.spacer(40), row, 1)
            row += 1

        widget = QWidget()
        widget.setStyleSheet(
            "min-width: 125px; border-left: 1px solid green; border-right: 1px solid green"
        )
        widget.setLayout(layout)
        return widget
