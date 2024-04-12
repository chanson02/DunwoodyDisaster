"""
The entry point for the game
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from dunwoody_disaster.views.fightScreen import FightScreen
from dunwoody_disaster.views.collectLootScreen import CollectLootScreen
from dunwoody_disaster.CharacterFactory import CharacterFactory
from dunwoody_disaster import Item

from dunwoody_disaster.views.StartMenu import StartMenu
from dunwoody_disaster.views.MapScreen import MapScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dunwoody-Disaster")
        # self.setGeometry(100, 100, 800, 600)

<<<<<<< HEAD
        self.startMenu = StartMenu()
        self.startMenu.startButton.clicked.connect(self.showMapScreen)
        self.mapScreen = MapScreen()
        self.fightScreen = FightScreen()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.startMenu)
        self.stack.addWidget(self.mapScreen)
        self.stack.addWidget(self.fightScreen)

        # Set the stacked widget as the central widget of the main window
        self.setCentralWidget(self.stack)

    def showMapScreen(self):
        self.stack.setCurrentIndex(1)

    """
    TODO: Make sure this works
    def exitGame(self):
        reply = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )  # Ask for confirmation before exiting
        if reply == QMessageBox.Yes:
            self.close()  # Close the window if the user confirms
    """
=======
        player1 = CharacterFactory.createTestChar()
        player2 = CharacterFactory.createTestChar()
        if 1 == 2:  # this is here to clear lint warnings
            self.setCentralWidget(FightScreen(player1, player2))
        else:
            items = Item.weapons + Item.armors
            self.setCentralWidget(CollectLootScreen(player1, items))
>>>>>>> origin/28-inventory-system


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
