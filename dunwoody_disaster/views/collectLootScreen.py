from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from dunwoody_disaster.CharacterFactory import Character
from dunwoody_disaster import Item


class CollectLootScreen(QWidget):
    def __init__(self, player: Character, available: list[Item.Item]):
        """
        :param player: The player that is selecting an item.
        :param available: A list of items the player has access to select.
        :return: Creates a UI where a user can select which item(s)? they want to add to their inventory.
        """
        super().__init__()
        self.player = player
        self.items = available

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel('Loot screen'))
        self.setLayout(layout)
