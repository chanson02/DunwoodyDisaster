from typing import Sequence
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QWidget, QScrollArea, QVBoxLayout, QGroupBox
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
        layout = QVBoxLayout()

        lbl = QLabel(label)
        lbl.setMinimumHeight(50)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet('color: white; font-size: 50px;')
        layout.addWidget(lbl)

        item_layout = QVBoxLayout()
        for item in items:
            gbox = QGroupBox()
            container = QVBoxLayout()
            container.addWidget(item.widget())
            DD.clickable(gbox).connect(self.select_item_lambda(item))
            gbox.setLayout(container)
            item_layout.addWidget(gbox)
        item_layout.addItem(DD.expander(False, True, 0))

        scroll_area = DD.scroller(item_layout, False, True)
        layout.addWidget(scroll_area)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
