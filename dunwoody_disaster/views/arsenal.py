from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGridLayout, QLabel, QSizePolicy, QSpacerItem, QWidget
from dunwoody_disaster import ASSETS


class Arsenal(QWidget):
    """
    The arsenal is made up of two `inventory` widgets which display items
    """

    def __init__(self):
        super().__init__()
        self.imageAssets = {
            item: QPixmap(f"./assets/{item}.jpg")
            for item in ["sword", "spear", "shield", "gloves"]
        }

        self.setStyleSheet("background-color: black;")
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        weapons = [
            {"name": "sword", "image": ASSETS["sword"], "KEY": [20, 30, 10]},
            {"name": "spear", "image": ASSETS["spear"], "KEY": [30, 10, 20]},
        ]
        weapons_widget = self.create_inventory("Weapons", weapons)
        armor = [
            {"name": "shield", "image": ASSETS["shield"], "KEY": [30, 10, 20]},
            {"name": "gloves", "image": ASSETS["gloves"], "KEY": [10, 10, 10]},
        ]
        armor_widget = self.create_inventory("Armor", armor)

        layout.addWidget(weapons_widget, 0, 0)
        layout.addWidget(armor_widget, 0, 1)
        self.setLayout(layout)

    def spacer(self, height: int) -> QSpacerItem:
        return QSpacerItem(
            0, height, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )

    def create_inventory(self, label: str, items: list[dict]) -> QWidget:
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        row = 0

        lbl = QLabel(label)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: white; font-size: 24px;")
        layout.addWidget(lbl, row, 1)
        row += 1
        layout.addItem(self.spacer(10), row, 1)
        row += 1

        for item in items:
            name = QLabel(item["name"])
            name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name.setStyleSheet("color: white;")
            layout.addWidget(name, row, 1)
            row += 1

            layout.addItem(self.spacer(10), row, 1)
            row += 1

            image = QLabel("")
            image.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image.setPixmap(QPixmap(item["image"]).scaledToWidth(80))
            layout.addWidget(image, row, 1)
            row += 1

            layout.addItem(self.spacer(10), row, 1)
            row += 1

            properties = QLabel(
                f"H: {item['KEY'][0]}\nM: {item['KEY'][1]}\nMech: {item['KEY'][2]}"
            )
            properties.setAlignment(Qt.AlignmentFlag.AlignCenter)
            properties.setStyleSheet("color: white;")
            layout.addWidget(properties, row, 1)
            row += 1

            layout.addItem(self.spacer(40), row, 1)
            row += 1

        widget = QWidget()
        widget.setStyleSheet(
            "min-width: 125px; border-left: 1px solid green; border-right: 1px solid green"
        )
        widget.setLayout(layout)
        return widget
