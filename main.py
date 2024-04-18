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
        self.setStyleSheet("background-color: #2f2f2f;")

        self.player1 = CharacterFactory.createTestChar()
        self.testChar = CharacterFactory.createTestChar()
        #Enemies
        self.courtChar = CharacterFactory.createTestChar()
        self.lectChar = CharacterFactory.createTestChar()
        self.phyLabChar = CharacterFactory.createTestChar()
        self.sciLabChar = CharacterFactory.createTestChar()


        self.startMenu = StartMenu()
        self.startMenu.startButton.clicked.connect(self.showMapScreen)
        self.mapScreen = MapScreen(self.EnterFight)
        self.fightScreen = FightScreen(self.player1, self.testChar)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.startMenu)
        self.stack.addWidget(self.mapScreen)
        self.stack.addWidget(self.fightScreen)

        # Set the stacked widget as the central widget of the main window
        self.setCentralWidget(self.stack)

    def showMapScreen(self):
        self.stack.setCurrentIndex(1)
    
    """
    Change fight screen character objects. Call init UI to redraw based on the character objects. Enter fight screen by pointing stack at fight screen. 
    This will need to be changed to set the proper opponent per setting.
    """
    def EnterFight(self):
        self.stack.setCurrentIndex(2)
        self.player1 = self.player1
        self.player2 = self.courtChar

 
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


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
