from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QGridLayout, QLabel, QSizePolicy, QSpacerItem, QWidget, QPushButton
import dunwoody_disaster as DD


class Arsenal(QWidget):
    """
    The arsenal is made up of two `inventory` widgets which display items
    """

    def __init__(self, selector):
        super().__init__()
        self.selector = selector
        self.imageAssets = {
            item: QPixmap(f"./assets/{item}.jpg")
            for item in ["sword", "spear", "shield", "gloves"]
        }

        self.setStyleSheet("background-color: black;")
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        weapons = [
            {"name": "sword", "image": DD.ASSETS["sword"], "KEY": [20, 30, 10]},
            {"name": "spear", "image": DD.ASSETS["spear"], "KEY": [30, 10, 20]},
        ]
        weapons_widget = self.create_inventory("Weapons", weapons)
        armor = [
            {"name": "shield", "image": DD.ASSETS["shield"], "KEY": [30, 10, 20]},
            {"name": "gloves", "image": DD.ASSETS["gloves"], "KEY": [10, 10, 10]},
        ]
        armor_widget = self.create_inventory("Armor", armor)

        layout.addWidget(weapons_widget, 0, 0)
        layout.addWidget(armor_widget, 0, 1)
        self.setLayout(layout)

    def select_item(self, item: dict, attack: bool):
        if attack:
            self.selector.set_attack(item)
        else:
            self.selector.set_defense(item)
        return

    def select_item_lambda(self, item: dict, attack: bool):
        return lambda: self.select_item(item, attack)

    def create_inventory(self, label: str, items: list[dict]) -> QWidget:
        attacking = False
        if label == 'Weapons':
            attacking = True
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
            name = QLabel(item["name"])
            name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name.setStyleSheet("color: white;")
            layout.addWidget(name, row, 1)
            row += 1

            layout.addItem(DD.spacer(10), row, 1)
            row += 1

            image = QPixmap(item['image']).scaledToWidth(80)
            btn = QPushButton()
            btn.setIcon(image)
            btn.setIconSize(image.size())
            btn.clicked.connect(self.select_item_lambda(item, attacking))
            layout.addWidget(btn, row, 1)
            row += 1

            layout.addItem(DD.spacer(10), row, 1)
            row += 1

            properties = QLabel(
                f"H: {item['KEY'][0]}\nM: {item['KEY'][1]}\nMech: {item['KEY'][2]}"
            )
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
