"""
The entry point for the game
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from dunwoody_disaster.views.fightScreen import FightScreen
from dunwoody_disaster.views.collectLootScreen import CollectLootScreen
from dunwoody_disaster.CharacterFactory import CharacterFactory
from dunwoody_disaster import Item


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokemon-like Game")
        self.setGeometry(100, 100, 800, 600)

        player1 = CharacterFactory.createTestChar()
        player2 = CharacterFactory.createTestChar()
        if 1 == 2:  # this is here to clear lint warnings
            self.setCentralWidget(FightScreen(player1, player2))
        items = Item.weapons + Item.armors
        self.setCentralWidget(CollectLootScreen(player1, items))


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
