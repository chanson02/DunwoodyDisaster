from typing import Sequence
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QWidget,
    QVBoxLayout,
    QGroupBox,
)
import dunwoody_disaster as DD
from dunwoody_disaster.views.action_selector import ActionSelector
from dunwoody_disaster import Item
from typing import Optional


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

        weapons_widget = self.createInventory("Weapons", weapons)
        armor_widget = self.createInventory("Armor", armors)

        layout.addWidget(weapons_widget, 0, 0)
        layout.addWidget(armor_widget, 0, 1)
        self.setLayout(layout)

    def selectItem(self, item: Optional[Item.Item]):
        if type(item) is Item.Weapon:
            if item == self.selector.attack:
                item = None
            self.selector.setAttack(item)
        elif type(item) is Item.Armor:
            if item == self.selector.defense:
                item = None
            self.selector.setDefense(item)
        return

    def selectItemLambda(self, item: Item.Item):
        return lambda: self.selectItem(item)

    def createInventory(self, label: str, items: Sequence[Item.Item]) -> QWidget:
        layout = QVBoxLayout()

        lbl = QLabel(label)
        lbl.setMinimumHeight(50)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: white; font-size: 50px;")
        layout.addWidget(lbl)

        item_layout = QVBoxLayout()
        for item in items:
            gbox = QGroupBox()
            container = QVBoxLayout()
            container.addWidget(item.widget())
            DD.clickable(gbox).connect(self.selectItemLambda(item))
            gbox.setLayout(container)
            item_layout.addWidget(gbox)
        item_layout.addItem(DD.expander(False, True, 0))

        scroll_area = DD.scroller(item_layout, False, True)
        layout.addWidget(scroll_area)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
