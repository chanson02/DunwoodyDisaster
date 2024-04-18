"""
The entry point for the game
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from dunwoody_disaster.CharacterFactory import CharacterFactory

from dunwoody_disaster.FightSequence import FightSequence
from dunwoody_disaster.views.victoryScreen import VictoryScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokemon-like Game")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2f2f2f;")

        player1 = CharacterFactory.createTestChar()
        player2 = CharacterFactory.createTestChar()
        test_fight_controller = FightSequence(player1, player2)
        self.setCentralWidget(VictoryScreen(test_fight_controller))


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
